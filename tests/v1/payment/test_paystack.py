import pytest
from uuid_extensions import uuid7
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from main import app
from fastapi import status
from api.db.database import get_db
from api.v1.models import User, Payment, BillingPlan
from api.v1.services.user import user_service
from api.v1.schemas.payment import PaymentDetail
from api.v1.routes.payment_paystack import pay_with_paystack

client = TestClient(app)

# Mock database
@pytest.fixture
def mock_db_session(mocker):
    db_session_mock = mocker.MagicMock(spec=Session)
    app.dependency_overrides[get_db] = lambda: db_session_mock
    return db_session_mock

# Test User
@pytest.fixture
def test_user():
    return User(
        id=str(uuid7()),
        email="testuser@gmail.com",
        password="hashedpassword",
        first_name="test",
        last_name="user",
        is_active=True,
    )


@pytest.fixture
def mock_request():
    return PaymentDetail(organization_id="se4", plan_id="1", billing_option="Monthly", full_name="helo", redirect_url="http://example.com/redirect")

@pytest.fixture
def mock_plan():
    return BillingPlan(id=1, price=float("100.00"), currency="USD")

@pytest.mark.asyncio
@patch("api.v1.routes.payment_paystack.settings")
@patch("api.v1.routes.payment_paystack.requests.post")
@patch("api.v1.routes.payment_paystack.check_model_existence")
@patch("api.v1.routes.payment_paystack.PaymentService")
@patch("api.v1.routes.payment_paystack.uuid7")
async def test_pay_with_paystack_success(
    mock_uuid7, 
    mock_payment_service, 
    mock_check_model, 
    mock_post, 
    mock_settings,
    mock_db_session, 
    test_user, 
    mock_request, 
    mock_plan
):
    # Setup mocks
    test_uuid = uuid7()
    mock_settings.PAYSTACK_SECRET = "test_secret_key"
    mock_uuid7.return_value = test_uuid
    mock_check_model.return_value = mock_plan
    mock_post.return_value.json.return_value = {"data": {"authorization_url": "http://payment.url"}}
    mock_payment_service_instance = mock_payment_service.return_value

    result = await pay_with_paystack(mock_request, test_user, mock_db_session)

    # Assertions
    assert result.status_code == status.HTTP_200_OK
   
    mock_post.assert_called_once_with(
        "https://api.paystack.co/transaction/initialize",
        json={
            "reference": str(test_uuid),
            "amount": 100.00,
            "callback_url": "http://example.com/redirect",
            "email": test_user.email
        },
        headers={"Authorization": "Bearer test_secret_key"}
    )

    # Check if payment details were saved correctly
    mock_payment_service_instance.create.assert_called_once_with(
        mock_db_session,
        {
            "user_id": test_user.id,
            "amount": 100.00,
            "currency": "USD",
            "status": "pending",
            "method": "card",
            "transaction_id": str(test_uuid)
        }
    )