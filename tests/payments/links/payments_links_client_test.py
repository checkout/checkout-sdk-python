import pytest

from tests._assertions import assert_api_call
from checkout_sdk.payments.links.payments_client import PaymentsLinksClient
from checkout_sdk.payments.links.payments_links import PaymentLinkRequest


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return PaymentsLinksClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestPaymentsLinksClient:

    def test_should_get_payment_link(self, mocker, client: PaymentsLinksClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_payment_link('payment_link_id') == 'response'
        assert_api_call(mock, 'payment-links/payment_link_id')

    def test_should_create_payment_link(self, mocker, client: PaymentsLinksClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = PaymentLinkRequest()

        assert client.create_payment_link(body) == 'response'
        assert_api_call(mock, 'payment-links', body)
