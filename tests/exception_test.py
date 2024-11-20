import pytest
from unittest.mock import Mock
from checkout_sdk.exception import (
    CheckoutException,
    CheckoutArgumentException,
    CheckoutAuthorizationException,
    CheckoutApiException
)
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.utils import map_to_http_metadata


def test_checkout_exception():
    with pytest.raises(CheckoutException) as exc_info:
        raise CheckoutException("Test message")
    exception = exc_info.value
    assert str(exception) == "Test message"


def test_checkout_argument_exception():
    with pytest.raises(CheckoutArgumentException) as exc_info:
        raise CheckoutArgumentException("Argument error occurred")
    exception = exc_info.value
    assert str(exception) == "Argument error occurred"


def test_checkout_argument_exception_no_message():
    with pytest.raises(CheckoutArgumentException) as exc_info:
        raise CheckoutArgumentException()
    exception = exc_info.value
    assert str(exception) == ""


def test_checkout_authorization_exception():
    with pytest.raises(CheckoutAuthorizationException) as exc_info:
        raise CheckoutAuthorizationException("Authorization error occurred")
    exception = exc_info.value
    assert str(exception) == "Authorization error occurred"


def test_invalid_authorization():
    auth_type = Mock(spec=AuthorizationType)
    auth_type.name = "SECRET_KEY"
    with pytest.raises(CheckoutAuthorizationException) as exc_info:
        CheckoutAuthorizationException.invalid_authorization(auth_type)
    assert "SECRET_KEY authorization type" in str(exc_info.value)


def test_invalid_key():
    key_type = Mock(spec=AuthorizationType)
    key_type.name = "PUBLIC_KEY"
    with pytest.raises(CheckoutAuthorizationException) as exc_info:
        CheckoutAuthorizationException.invalid_key(key_type)
    assert "PUBLIC_KEY is required for this operation" in str(exc_info.value)


@pytest.mark.parametrize("auth_type_name", ["SECRET_KEY", "PUBLIC_KEY", "CUSTOM_KEY"])
def test_invalid_authorization_various_types(auth_type_name):
    auth_type = Mock(spec=AuthorizationType)
    auth_type.name = auth_type_name
    with pytest.raises(CheckoutAuthorizationException) as exc_info:
        CheckoutAuthorizationException.invalid_authorization(auth_type)
    assert f"{auth_type_name} authorization type" in str(exc_info.value)


def test_checkout_api_exception():
    response = Mock()
    response.status_code = 400
    response.text = '{"error_type": "request_invalid", "error_codes": ["invalid_field"]}'
    response.json.return_value = {
        "error_type": "request_invalid",
        "error_codes": ["invalid_field"]
    }

    with pytest.raises(CheckoutApiException) as exc_info:
        raise CheckoutApiException(response)
    exception = exc_info.value
    assert exception.http_metadata.status_code == 400
    assert exception.error_type == "request_invalid"
    assert exception.error_details == ["invalid_field"]


def test_checkout_api_exception_without_error_details():
    response = Mock()
    response.status_code = 500
    response.text = '{"message": "Internal Server Error"}'
    response.json.return_value = {
        "message": "Internal Server Error"
    }

    with pytest.raises(CheckoutApiException) as exc_info:
        raise CheckoutApiException(response)
    exception = exc_info.value
    assert exception.http_metadata.status_code == 500
    assert exception.error_type is None
    assert exception.error_details is None


def test_checkout_api_exception_empty_response():
    response = Mock()
    response.status_code = 404
    response.text = ''
    response.json.return_value = {}

    with pytest.raises(CheckoutApiException) as exc_info:
        raise CheckoutApiException(response)
    exception = exc_info.value
    assert exception.http_metadata.status_code == 404
    assert exception.error_type is None
    assert exception.error_details is None


def test_checkout_api_exception_non_json_response():
    response = Mock()
    response.status_code = 502
    response.text = 'Bad Gateway'
    response.json.side_effect = ValueError("No JSON object could be decoded")

    with pytest.raises(CheckoutApiException) as exc_info:
        raise CheckoutApiException(response)
    exception = exc_info.value
    assert exception.http_metadata.status_code == 502
    assert exception.error_type is None
    assert exception.error_details is None


@pytest.mark.parametrize("status_code", [400, 401, 403, 404, 500])
def test_checkout_api_exception_various_status_codes(status_code):
    response = Mock()
    response.status_code = status_code
    response.text = ''
    response.json.return_value = {}

    with pytest.raises(CheckoutApiException) as exc_info:
        raise CheckoutApiException(response)
    exception = exc_info.value
    assert exception.http_metadata.status_code == status_code


def test_map_to_http_metadata():
    response = Mock()
    response.status_code = 200
    response.headers = {'Content-Type': 'application/json'}

    metadata = map_to_http_metadata(response)
    assert metadata.status_code == 200
    assert metadata.headers == {'Content-Type': 'application/json'}


def test_checkout_api_exception_message():
    response = Mock()
    response.status_code = 400
    response.text = '{"error_type": "invalid_request", "error_codes": ["bad_request"]}'
    response.json.return_value = {
        "error_type": "invalid_request",
        "error_codes": ["bad_request"]
    }

    with pytest.raises(CheckoutApiException) as exc_info:
        raise CheckoutApiException(response)
    exception = exc_info.value
    expected_message = "The API response status code (400) does not indicate success."
    assert str(exception) == expected_message


def test_checkout_api_exception_no_response_text():
    response = Mock()
    response.status_code = 400
    response.text = None
    response.json.return_value = {}

    with pytest.raises(CheckoutApiException) as exc_info:
        raise CheckoutApiException(response)
    exception = exc_info.value
    assert exception.http_metadata.status_code == 400
    assert exception.error_type is None
    assert exception.error_details is None
