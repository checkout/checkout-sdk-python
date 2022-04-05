import pytest

from checkout_sdk.customers.customers_client_four import CustomersClient
from checkout_sdk.customers.customers_four import CustomerRequest


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return CustomersClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestCustomersClient:

    def test_should_get_customer(self, mocker, client: CustomersClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get('customer_id') == 'response'

    def test_should_create_customer(self, mocker, client: CustomersClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create(CustomerRequest()) == 'response'

    def test_should_update_customer(self, mocker, client: CustomersClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        assert client.update('customer_id', CustomerRequest()) == 'response'

    def test_should_delete_customer(self, mocker, client: CustomersClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')
        assert client.delete('customer_id') == 'response'
