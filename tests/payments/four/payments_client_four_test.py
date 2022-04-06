import pytest

from checkout_sdk.common.common_four import AccountHolder
from checkout_sdk.payments.payments import RefundRequest, VoidRequest
from checkout_sdk.payments.payments_client_four import PaymentsClient
from checkout_sdk.payments.payments_four import PaymentRequest, PayoutRequest, CaptureRequest, AuthorizationRequest, \
    RequestProviderTokenSource


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return PaymentsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestPaymentsClient:

    def test_request_payment(self, mocker, client: PaymentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.request_payment(PaymentRequest()) == 'response'

    def test_request_payment_idempotency_key(self, mocker, client: PaymentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.request_payment(PaymentRequest(), 'idempotency_key') == 'response'

    def test_request_payout(self, mocker, client: PaymentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.request_payout(PayoutRequest()) == 'response'

    def test_request_payout_idempotency_key(self, mocker, client: PaymentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.request_payout(PayoutRequest(), 'idempotency_key') == 'response'

    def test_get_payment_details(self, mocker, client: PaymentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_payment_details('payment_id') == 'response'

    def test_get_payment_actions(self, mocker, client: PaymentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_payment_actions('payment_id') == 'response'

    def test_capture_payment(self, mocker, client: PaymentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.capture_payment('payment_id', CaptureRequest()) == 'response'

    def test_capture_payment_idempotency_key(self, mocker, client: PaymentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.capture_payment('payment_id', None, 'idempotency_key') == 'response'

    def test_refund_payment(self, mocker, client: PaymentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.refund_payment('payment_id', RefundRequest()) == 'response'

    def test_refund_payment_idempotency_key(self, mocker, client: PaymentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.refund_payment('payment_id', None, 'idempotency_key') == 'response'

    def test_void_payment(self, mocker, client: PaymentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.void_payment('payment_id', VoidRequest()) == 'response'

    def test_void_payment_idempotency_key(self, mocker, client: PaymentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.void_payment('payment_id', None, 'idempotency_key') == 'response'

    def test_increment_payment_authorization(self, mocker, client: PaymentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.increment_payment_authorization('payment_id', AuthorizationRequest()) == 'response'

    def test_increment_payment_authorization_idempotency_key(self, mocker, client: PaymentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.increment_payment_authorization('payment_id', AuthorizationRequest(),
                                                      'idempotency_key') == 'response'

    # sources
    def test_should_request_provider_token_source_payment(self, mocker, client: PaymentsClient):
        source = RequestProviderTokenSource()
        source.token = 'token'
        source.payment_method = 'method'
        source.account_holder = AccountHolder()

        request = PaymentRequest()
        request.source = source

        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.request_payment(request, 'idempotency_key') == 'response'
