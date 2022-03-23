import pytest

from checkout_sdk.payments.links.payments_client import PaymentsLinksClient
from checkout_sdk.payments.links.payments_links import PaymentLinkRequest


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return PaymentsLinksClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestHostedPaymentsClient:

    def test_should_get_instrument(self, mocker, client: PaymentsLinksClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_payment_link('payment_link_id') == 'response'

    def test_should_create_instrument(self, mocker, client: PaymentsLinksClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_payment_link(PaymentLinkRequest()) == 'response'
