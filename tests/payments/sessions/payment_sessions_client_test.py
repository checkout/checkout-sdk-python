import pytest

from tests._assertions import assert_api_call
from checkout_sdk.payments.sessions.sessions import (
    PaymentSessionsRequest, PaymentSessionWithPaymentRequest, SubmitPaymentSessionRequest
)
from checkout_sdk.payments.sessions.sessions_client import PaymentSessionsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return PaymentSessionsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestPaymentSessionsClient:

    def test_should_create_payment_sessions(self, mocker, client: PaymentSessionsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = PaymentSessionsRequest()

        assert client.create_payment_sessions(body) == 'response'
        assert_api_call(mock, 'payment-sessions', body)

    def test_should_create_payment_session_with_payment(self, mocker, client: PaymentSessionsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = PaymentSessionWithPaymentRequest()

        assert client.create_payment_session_with_payment(body) == 'response'
        assert_api_call(mock, 'payment-sessions/complete', body)

    def test_should_submit_payment_session(self, mocker, client: PaymentSessionsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = SubmitPaymentSessionRequest()

        assert client.submit_payment_session('ps_test_session_id', body) == 'response'
        assert_api_call(mock, 'payment-sessions/ps_test_session_id/submit', body)
