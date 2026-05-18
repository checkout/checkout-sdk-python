import pytest

from tests._assertions import assert_api_call
from checkout_sdk.apm.klarna import CreditSessionRequest, OrderCaptureRequest
from checkout_sdk.apm.klarna_client import KlarnaClient
from checkout_sdk.payments.payments import VoidRequest


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return KlarnaClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


# Sandbox mock configuration → klarna_client uses 'klarna-external' base path.
class TestKlarnaClient:

    def test_should_create_credit_session(self, mocker, client: KlarnaClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = CreditSessionRequest()

        assert client.create_credit_session(body) == 'response'
        assert_api_call(mock, 'klarna-external/credit-sessions', body)

    def test_should_get_credit_session(self, mocker, client: KlarnaClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_credit_session('session_id') == 'response'
        assert_api_call(mock, 'klarna-external/credit-sessions/session_id')

    def test_capture_payment(self, mocker, client: KlarnaClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = OrderCaptureRequest()

        assert client.capture_payment('payment_id', body) == 'response'
        assert_api_call(mock, 'klarna-external/orders/payment_id/captures', body)

    def test_void_payment(self, mocker, client: KlarnaClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = VoidRequest()

        assert client.void_payment('payment_id', body) == 'response'
        assert_api_call(mock, 'klarna-external/orders/payment_id/voids', body)
