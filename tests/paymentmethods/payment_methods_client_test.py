import pytest

from tests._assertions import assert_api_call
from checkout_sdk.paymentmethods.payment_methods_client import PaymentMethodsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return PaymentMethodsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestPaymentMethodsClient:

    def test_get_available_payment_methods(self, mocker, client: PaymentMethodsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_available_payment_methods('pc_test_123456') == 'response'
        assert_api_call(mock, 'payment-methods')
        # The client wraps the str into a query filter internally; verify the wrapping.
        assert mock.call_args.args[2].processing_channel_id == 'pc_test_123456'
