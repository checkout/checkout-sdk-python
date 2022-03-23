import pytest

from checkout_sdk.payments.hosted.hosted_payments import HostedPaymentsSessionRequest
from checkout_sdk.payments.hosted.hosted_payments_client import HostedPaymentsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return HostedPaymentsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestHostedPaymentsClient:

    def test_should_get_instrument(self, mocker, client: HostedPaymentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_hosted_payments_page_details('hosted_payment_id') == 'response'

    def test_should_create_instrument(self, mocker, client: HostedPaymentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_hosted_payments_page_session(HostedPaymentsSessionRequest()) == 'response'
