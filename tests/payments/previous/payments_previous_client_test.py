import pytest

from tests._assertions import assert_api_call
from checkout_sdk.payments.payments_previous import PaymentRequest, PayoutRequest, CaptureRequest
from checkout_sdk.payments.payments import RefundRequest, VoidRequest
from checkout_sdk.payments.payments_client_previous import PaymentsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return PaymentsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestPaymentsClient:

    def test_request_payment(self, mocker, client: PaymentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = PaymentRequest()

        assert client.request_payment(body) == 'response'
        assert_api_call(mock, 'payments', body)

    def test_request_payment_idempotency_key(self, mocker, client: PaymentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = PaymentRequest()

        assert client.request_payment(body, 'idempotency_key') == 'response'
        assert_api_call(mock, 'payments', body)

    def test_request_payout(self, mocker, client: PaymentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = PayoutRequest()

        assert client.request_payout(body) == 'response'
        assert_api_call(mock, 'payments', body)

    def test_request_payout_idempotency_key(self, mocker, client: PaymentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = PayoutRequest()

        assert client.request_payout(body, 'idempotency_key') == 'response'
        assert_api_call(mock, 'payments', body)

    def test_get_payment_details(self, mocker, client: PaymentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_payment_details('payment_id') == 'response'
        assert_api_call(mock, 'payments/payment_id')

    def test_get_payment_actions(self, mocker, client: PaymentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_payment_actions('payment_id') == 'response'
        assert_api_call(mock, 'payments/payment_id/actions')

    def test_capture_payment(self, mocker, client: PaymentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = CaptureRequest()

        assert client.capture_payment('payment_id', body) == 'response'
        assert_api_call(mock, 'payments/payment_id/captures', body)

    def test_capture_payment_idempotency_key(self, mocker, client: PaymentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.capture_payment('payment_id', None, 'idempotency_key') == 'response'
        mock.assert_called_once()
        args = mock.call_args.args
        assert args[0] == 'payments/payment_id/captures'

    def test_refund_payment(self, mocker, client: PaymentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = RefundRequest()

        assert client.refund_payment('payment_id', body) == 'response'
        assert_api_call(mock, 'payments/payment_id/refunds', body)

    def test_refund_payment_idempotency_key(self, mocker, client: PaymentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.refund_payment('payment_id', None, 'idempotency_key') == 'response'
        mock.assert_called_once()
        args = mock.call_args.args
        assert args[0] == 'payments/payment_id/refunds'

    def test_void_payment(self, mocker, client: PaymentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = VoidRequest()

        assert client.void_payment('payment_id', body) == 'response'
        assert_api_call(mock, 'payments/payment_id/voids', body)

    def test_void_payment_idempotency_key(self, mocker, client: PaymentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.void_payment('payment_id', None, 'idempotency_key') == 'response'
        mock.assert_called_once()
        args = mock.call_args.args
        assert args[0] == 'payments/payment_id/voids'
