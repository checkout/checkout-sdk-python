import pytest
from unittest.mock import Mock
from checkout_sdk.exception import (
    CheckoutException,
    CheckoutArgumentException,
    CheckoutAuthorizationException,
    CheckoutApiException
)
from checkout_sdk.authorization_type import AuthorizationType


def test_checkout_exception():
    with pytest.raises(CheckoutException):
        raise CheckoutException("Test message")


def test_checkout_argument_exception():
    with pytest.raises(CheckoutArgumentException):
        raise CheckoutArgumentException("Argument error occurred")


def test_checkout_authorization_exception():
    with pytest.raises(CheckoutAuthorizationException):
        raise CheckoutAuthorizationException("Authorization error occurred")


def test_invalid_authorization():
    auth_type = Mock(spec=AuthorizationType)
    auth_type.name = "SECRET_KEY"
    with pytest.raises(CheckoutAuthorizationException, match="SECRET_KEY authorization type"):
        CheckoutAuthorizationException.invalid_authorization(auth_type)


def test_invalid_key():
    key_type = Mock(spec=AuthorizationType)
    key_type.name = "PUBLIC_KEY"
    with pytest.raises(CheckoutAuthorizationException, match="PUBLIC_KEY is required for this operation"):
        CheckoutAuthorizationException.invalid_key(key_type)


def test_checkout_api_exception():
    response = Mock()
    response.status_code = 400
    response.text = '{"error_type": "request_invalid", "error_codes": ["invalid_field"]}'
    response.json.return_value = {
        "error_type": "request_invalid",
        "error_codes": ["invalid_field"]
    }

    exception_instance = CheckoutApiException(response)

    with pytest.raises(CheckoutApiException) as exc_info:
        raise exception_instance

    exception = exc_info.value
    assert exception.http_metadata.status_code == 400
    assert exception.error_type == "request_invalid"
    assert exception.error_details == ["invalid_field"]
