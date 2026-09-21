import pytest

from tests._assertions import assert_api_call
from checkout_sdk.inventory.inventory import InventoryAdjustmentRequest, InventoryReservationRequest, \
    InventoryReservationItem, InventorySetLevelsRequest, InventorySetProductRequest, InventoryLevelsQuery, \
    InventoryMoney, InventoryCondition
from checkout_sdk.inventory.inventory_client import InventoryClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return InventoryClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestInventoryClient:

    def test_adjust_inventory(self, mocker, client: InventoryClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = InventoryAdjustmentRequest()
        body.variant_id = 'var_123'
        body.delta = -5
        body.reason = 'damaged in warehouse'

        assert client.adjust_inventory(body) == 'response'
        assert_api_call(mock, 'inventory/adjustments', body)

    def test_adjust_inventory_idempotency_key(self, mocker, client: InventoryClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = InventoryAdjustmentRequest()

        assert client.adjust_inventory(body, 'idempotency_key') == 'response'
        args = mock.call_args.args
        assert args[3] == 'idempotency_key'

    def test_create_inventory_reservation(self, mocker, client: InventoryClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        item = InventoryReservationItem()
        item.variant_id = 'var_123'
        item.quantity = 2
        body = InventoryReservationRequest()
        body.owner_type = 'order'
        body.owner_reference = 'order_456'
        body.items = [item]

        assert client.create_inventory_reservation(body) == 'response'
        assert_api_call(mock, 'inventory/reservations', body)

    def test_create_inventory_reservation_idempotency_key(self, mocker, client: InventoryClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = InventoryReservationRequest()

        assert client.create_inventory_reservation(body, 'idempotency_key') == 'response'
        args = mock.call_args.args
        assert args[3] == 'idempotency_key'

    def test_get_inventory_reservation(self, mocker, client: InventoryClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_inventory_reservation('rsv_123') == 'response'
        assert_api_call(mock, 'inventory/reservations/rsv_123')

    def test_commit_inventory_reservation(self, mocker, client: InventoryClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.commit_inventory_reservation('rsv_123') == 'response'
        assert_api_call(mock, 'inventory/reservations/rsv_123/commit')

    def test_release_inventory_reservation(self, mocker, client: InventoryClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.release_inventory_reservation('rsv_123') == 'response'
        assert_api_call(mock, 'inventory/reservations/rsv_123/release')

    def test_get_inventory_levels(self, mocker, client: InventoryClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_inventory_levels('var_123') == 'response'
        assert_api_call(mock, 'inventory/var_123')

    def test_get_inventory_levels_with_expand(self, mocker, client: InventoryClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        query = InventoryLevelsQuery()
        query.expand = 'product'

        assert client.get_inventory_levels('var_123', query) == 'response'
        assert_api_call(mock, 'inventory/var_123', query)

    def test_set_inventory_levels(self, mocker, client: InventoryClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        body = InventorySetLevelsRequest()
        body.on_hand = 100

        assert client.set_inventory_levels('var_123', body) == 'response'
        assert_api_call(mock, 'inventory/var_123', body)

    def test_get_inventory_product(self, mocker, client: InventoryClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_inventory_product('var_123') == 'response'
        assert_api_call(mock, 'inventory/var_123/product')

    def test_set_inventory_product(self, mocker, client: InventoryClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        body = InventorySetProductRequest()
        body.title = 'Blue T-Shirt'
        body.description = 'A blue t-shirt'
        body.product_url = 'https://example.com/products/var_123'
        body.image_url = 'https://example.com/images/var_123.png'
        body.condition = InventoryCondition.NEW
        body.price = InventoryMoney()
        body.price.amount = 1999
        body.price.currency = 'USD'

        assert client.set_inventory_product('var_123', body) == 'response'
        assert_api_call(mock, 'inventory/var_123/product', body)

    def test_delete_inventory_product(self, mocker, client: InventoryClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')

        assert client.delete_inventory_product('var_123') == 'response'
        assert_api_call(mock, 'inventory/var_123/product')
