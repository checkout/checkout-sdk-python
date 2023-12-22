import pytest

from checkout_sdk.payments.contexts.contexts import PaymentContextsRequest
from checkout_sdk.payments.contexts.contexts_client import PaymentContextsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return PaymentContextsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestPaymentContextsClient:

    def test_should_create_payment_contexts(self, mocker, client: PaymentContextsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_payment_contexts(PaymentContextsRequest()) == 'response'

    def test_should_get_payment_context_details(self, mocker, client: PaymentContextsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_payment_context_details('payment_contexts_id') == 'response'
