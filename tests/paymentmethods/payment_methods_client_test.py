import pytest

from checkout_sdk.paymentmethods.payment_methods_client import PaymentMethodsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return PaymentMethodsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestPaymentMethodsClient:

    def test_get_available_payment_methods(self, mocker, client: PaymentMethodsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_available_payment_methods('pc_test_123456') == 'response'
