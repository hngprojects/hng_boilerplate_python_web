from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid_extensions import uuid7

from main import app
from api.db.database import get_db
from api.v1.services.user import user_service
from api.v1.models import User
from api.v1.models.organization import Organization

# Mock current user
def mock_get_current_user():
    return User(
        id=str(uuid7()),
        email="testuser@gmail.com",
        password=user_service.hash_password("Testpassword@123"),
        first_name='Test',
        last_name='User',
        is_active=True,
        is_super_admin=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

# Mock organization object
def mock_org():
    return Organization(
        id=str(uuid7()),
        company_name="Test Organization",
        company_email="testorg@example.com",
        industry="Tech",
        organization_type="Private",
        country="Country",
        state="State",
        address="Address",
        lga="LGA",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

@pytest.fixture
def db_session_mock():
    db_session = MagicMock(spec=Session)
    return db_session

@pytest.fixture
def client(db_session_mock):
    app.dependency_overrides[get_db] = lambda: db_session_mock
    yield TestClient(app)
    app.dependency_overrides = {}

@pytest.fixture
def mock_get_current_user_fixture():
    with patch("api.v1.services.user.user_service.get_current_user", return_value=mock_get_current_user()) as mock:
        yield mock

def test_get_organization_success(client, db_session_mock, mock_get_current_user_fixture):
    mock_organization = mock_org()
    db_session_mock.query().filter().first.return_value = mock_organization

    with patch("api.db.database.get_db", return_value=db_session_mock):
        response = client.get("/api/v1/organizations/1", headers={"Authorization": "Bearer testtoken"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["status_code"] == 200
        assert data["data"]["id"] == mock_organization.id
        assert data["data"]["company_name"] == mock_organization.company_name
        assert data["data"]["company_email"] == mock_organization.company_email

def test_get_organization_not_found(client, db_session_mock, mock_get_current_user_fixture):
    db_session_mock.query().filter().first.return_value = None

    with patch("api.db.database.get_db", return_value=db_session_mock):
        response = client.get("/api/v1/organizations/999", headers={"Authorization": "Bearer testtoken"})
        assert response.status_code == 404
        data = response.json()
        assert data["status"] == "error"
        assert data["status_code"] == 404
        assert data["message"] == "Organization not found"

def test_get_organization_invalid_id(client, db_session_mock, mock_get_current_user_fixture):
    with patch("api.db.database.get_db", return_value=db_session_mock):
        response = client.get("/api/v1/organizations/abc", headers={"Authorization": "Bearer testtoken"})
        assert response.status_code == 422  # Unprocessable Entity due to validation error
