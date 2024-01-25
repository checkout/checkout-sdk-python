import pytest

from checkout_sdk.payments.sessions.sessions import PaymentSessionsRequest
from checkout_sdk.payments.sessions.sessions_client import PaymentSessionsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return PaymentSessionsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestPaymentSessionsClient:

    def test_should_create_payment_sessions(self, mocker, client: PaymentSessionsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_payment_sessions(PaymentSessionsRequest()) == 'response'
