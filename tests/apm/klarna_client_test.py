import pytest

from checkout_sdk.apm.klarna import CreditSessionRequest, OrderCaptureRequest
from checkout_sdk.apm.klarna_client import KlarnaClient
from checkout_sdk.payments.payments import VoidRequest


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return KlarnaClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestKlarnaClient:

    def test_should_create_credit_session(self, mocker, client: KlarnaClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_credit_session(CreditSessionRequest()) == 'response'

    def test_should_get_credit_session(self, mocker, client: KlarnaClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_credit_session('session_id') == 'response'

    def test_capture_payment(self, mocker, client: KlarnaClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.capture_payment('payment_id', OrderCaptureRequest()) == 'response'

    def test_void_payment(self, mocker, client: KlarnaClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.void_payment('payment_id', VoidRequest()) == 'response'
