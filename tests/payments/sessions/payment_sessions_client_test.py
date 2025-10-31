import pytest

from checkout_sdk.payments.sessions.sessions import (
    PaymentSessionsRequest, PaymentSessionWithPaymentRequest, SubmitPaymentSessionRequest
)
from checkout_sdk.payments.sessions.sessions_client import PaymentSessionsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return PaymentSessionsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestPaymentSessionsClient:

    def test_should_create_payment_sessions(self, mocker, client: PaymentSessionsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_payment_sessions(PaymentSessionsRequest()) == 'response'

    def test_should_create_payment_session_with_payment(self, mocker, client: PaymentSessionsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_payment_session_with_payment(PaymentSessionWithPaymentRequest()) == 'response'

    def test_should_submit_payment_session(self, mocker, client: PaymentSessionsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        session_id = 'ps_test_session_id'
        assert client.submit_payment_session(session_id, SubmitPaymentSessionRequest()) == 'response'
