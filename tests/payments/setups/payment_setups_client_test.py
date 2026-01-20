import pytest

from checkout_sdk.payments.setups.setups import PaymentSetupsRequest
from checkout_sdk.payments.setups.setups_client import PaymentSetupsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return PaymentSetupsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestPaymentSetupsClient:

    def test_should_create_payment_setup(self, mocker, client: PaymentSetupsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_payment_setup(PaymentSetupsRequest()) == 'response'

    def test_should_update_payment_setup(self, mocker, client: PaymentSetupsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        assert client.update_payment_setup('setup_id', PaymentSetupsRequest()) == 'response'

    def test_should_get_payment_setup(self, mocker, client: PaymentSetupsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_payment_setup('setup_id') == 'response'

    def test_should_confirm_payment_setup(self, mocker, client: PaymentSetupsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.confirm_payment_setup('setup_id', 'payment_method_option_id') == 'response'
