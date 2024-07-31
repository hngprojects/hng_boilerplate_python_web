import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch
from uuid_extensions import uuid7
from jose import JWTError
from datetime import datetime, timezone, timedelta

from main import app
from api.db.database import get_db
from api.v1.models.notifications import Notification
from api.v1.services.user import user_service
from api.v1.models.user import User
from api.v1.services.notification import NotificationCreate



# Mock database dependency
@pytest.fixture
def db_session_mock():
    db_session = MagicMock(spec=Session)
    return db_session


@pytest.fixture
def client(db_session_mock):
    app.dependency_overrides[get_db] = lambda: db_session_mock
    client = TestClient(app)
    yield client
    app.dependency_overrides = {}


# Mock user service dependency

user_id = uuid7()
notification_id = uuid7()
timezone_offset = -8.0
tzinfo = timezone(timedelta(hours=timezone_offset))
timeinfo = datetime.now(tzinfo)
created_at = timeinfo
updated_at = timeinfo
access_token = user_service.create_access_token(str(user_id))

# Create test user

user = User(
    id=user_id,
    email="testuser1@gmail.com",
    password=user_service.hash_password("Testpassword@123"),
    first_name="Test",
    last_name="User",
    is_active=False,
    created_at=created_at,
    updated_at=updated_at,
)

# Create test notification

notification = Notification(
    id=notification_id,
    user_id=user_id,
    title="Test notification",
    message="This is my test notification message",
    status="unread",
    created_at=created_at,
    updated_at=updated_at,
)


def test_mark_notification_as_read(client, db_session_mock):

    db_session_mock.query().filter().all.return_value = [user, notification]

    headers = {"authorization": f"Bearer {access_token}"}

    response = client.patch(f"/api/v1/notifications/{notification.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["success"] == True
    assert response.json()["status_code"] == 200
    assert response.json()["message"] == "Notifcation marked as read"


def test_mark_notification_as_read_unauthenticated_user(client, db_session_mock):
    # Create test notification

    db_session_mock.query().filter().all.return_value = [notification]

    response = client.patch(f"/api/v1/notifications/{notification.id}")

    assert response.status_code == 401
    assert response.json()["success"] == False
    assert response.json()["status_code"] == 401
    
    
# New test cases for send_notification endpoint
@pytest.fixture
def mock_dependencies():
    with patch('api.utils.dependencies.get_db') as mock_get_db, \
         patch('api.utils.dependencies.get_current_user') as mock_get_current_user, \
         patch('api.v1.services.notification.NotificationService.create_notification') as mock_create_notification:
        
        mock_db = MagicMock()
        mock_user = MagicMock(id=uuid7(), username='testuser')
        
        mock_get_db.return_value = mock_db
        mock_get_current_user.return_value = mock_user
        mock_create_notification.return_value = MagicMock(
            id=uuid7(),
            user_id=mock_user.id,
            title="Test Title",
            message="Test Message",
            created_at="2024-01-01T00:00:00"
        )
        
        yield mock_db, mock_user, mock_create_notification
        
        
        
def test_create_notification_success(client, mock_dependencies):
    mock_db, mock_user, mock_create_notification = mock_dependencies

    notification_data = {
        "title": "Test Title",
        "message": "Test Message"
    }
    
    # Generate a token using the actual method for creating a token
    access_token = user_service.create_access_token(str(mock_user.id))

    headers = {"authorization": f"Bearer {access_token}"}

    # Logging request data
    print(f"Sending request with data: {notification_data} and headers: {headers}")
    
    response = client.post("/api/v1/notifications/send", json=notification_data, headers=headers)
    
    # Logging response
    print(f"Response status code: {response.status_code}")
    print(f"Response data: {response.json()}")
    
    # Extract the response data for validation
    response_json = response.json()
    
    # Extract the date string from the response
    created_at_str = response_json["data"]["created_at"]

    assert response.status_code == 200
    assert response_json == {
        "success": True,
        "status_code": 200,
        "message": "Notification created successfully",
        "data": {
            "id": str(mock_create_notification.return_value.id),
            "user_id": str(mock_user.id),
            "title": "Test Title",
            "message": "Test Message",
            "created_at": "2024-01-01T00:00:00"  
        }
    }

    # Additionally, assert that the 'created_at' field in the response is in the correct ISO format
    assert created_at_str == "2024-01-01T00:00:00"
