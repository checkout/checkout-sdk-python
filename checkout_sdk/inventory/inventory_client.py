from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.inventory.inventory import InventoryAdjustmentRequest, InventoryReservationRequest, \
    InventorySetLevelsRequest, InventorySetProductRequest, InventoryLevelsQuery


class InventoryClient(Client):
    __INVENTORY_PATH = 'inventory'
    __ADJUSTMENTS_PATH = 'adjustments'
    __RESERVATIONS_PATH = 'reservations'
    __COMMIT_PATH = 'commit'
    __RELEASE_PATH = 'release'
    __PRODUCT_PATH = 'product'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.OAUTH)

    def adjust_inventory(self, inventory_adjustment_request: InventoryAdjustmentRequest,
                         idempotency_key: str = None):
        """Apply a signed adjustment to a variant's on-hand stock.

        Args:
            inventory_adjustment_request: The adjustment to apply.
            idempotency_key: Optional idempotency key (`Cko-Idempotency-Key`).
        Returns:
            ResponseWrapper with the resulting InventoryLevels data. 201 on first write, 200 on an
            idempotent replay (with a `Cache-Control` response header present only on replay).
        Raises:
            CheckoutApiException on 404/409/422. The API returns an `InventoryErrorResponse` body
            (`request_id`, `error_type`, `error_codes`, and on `insufficient_stock` conflicts also
            `variant_id` and `available`); this SDK surfaces it the same way as every other
            domain, through `CheckoutApiException.request_id` / `.error_type` / `.error_details`
            (the latter populated from the body's `error_codes`), not a dedicated typed class.
        """
        return self._api_client.post(self.build_path(self.__INVENTORY_PATH, self.__ADJUSTMENTS_PATH),
                                     self._sdk_authorization(),
                                     inventory_adjustment_request,
                                     idempotency_key)

    def create_inventory_reservation(self, inventory_reservation_request: InventoryReservationRequest,
                                     idempotency_key: str = None):
        """Create an atomic, multi-variant stock reservation (hold).

        Args:
            inventory_reservation_request: The reservation to create.
            idempotency_key: Optional idempotency key (`Cko-Idempotency-Key`).
        Returns:
            ResponseWrapper with the resulting InventoryReservation data. 201 on first write, 200 on
            an idempotent replay (with a `Cache-Control` response header present only on replay).
        Raises:
            CheckoutApiException on 404/409/422; see `adjust_inventory` for the error body shape
            and how this SDK surfaces it.
        """
        return self._api_client.post(self.build_path(self.__INVENTORY_PATH, self.__RESERVATIONS_PATH),
                                     self._sdk_authorization(),
                                     inventory_reservation_request,
                                     idempotency_key)

    def get_inventory_reservation(self, reservation_id: str):
        """Retrieve an inventory reservation by id.

        Args:
            reservation_id: The reservation identifier.
        Returns:
            ResponseWrapper with InventoryReservation data.
        Raises:
            CheckoutApiException on 404; see `adjust_inventory` for the error body shape and how
            this SDK surfaces it.
        """
        return self._api_client.get(
            self.build_path(self.__INVENTORY_PATH, self.__RESERVATIONS_PATH, reservation_id),
            self._sdk_authorization())

    def commit_inventory_reservation(self, reservation_id: str):
        """Commit a held inventory reservation, consuming the reserved stock.

        Args:
            reservation_id: The reservation identifier.
        Returns:
            ResponseWrapper with InventoryReservation data.
        Raises:
            CheckoutApiException on 404/409; see `adjust_inventory` for the error body shape and
            how this SDK surfaces it.
        """
        return self._api_client.post(
            self.build_path(self.__INVENTORY_PATH, self.__RESERVATIONS_PATH, reservation_id, self.__COMMIT_PATH),
            self._sdk_authorization())

    def release_inventory_reservation(self, reservation_id: str):
        """Release a held inventory reservation, returning the reserved stock.

        Args:
            reservation_id: The reservation identifier.
        Returns:
            ResponseWrapper with InventoryReservation data.
        Raises:
            CheckoutApiException on 404/409; see `adjust_inventory` for the error body shape and
            how this SDK surfaces it.
        """
        return self._api_client.post(
            self.build_path(self.__INVENTORY_PATH, self.__RESERVATIONS_PATH, reservation_id, self.__RELEASE_PATH),
            self._sdk_authorization())

    def get_inventory_levels(self, variant_id: str, inventory_levels_query: InventoryLevelsQuery = None):
        """Retrieve the current stock levels for a variant.

        Args:
            variant_id: The merchant-provided identifier for the variant.
            inventory_levels_query: Optional query parameters, e.g. `expand=product`.
        Returns:
            ResponseWrapper with InventoryLevels data.
        Raises:
            CheckoutApiException on 404; see `adjust_inventory` for the error body shape and how
            this SDK surfaces it.
        """
        return self._api_client.get(self.build_path(self.__INVENTORY_PATH, variant_id),
                                    self._sdk_authorization(),
                                    inventory_levels_query)

    def set_inventory_levels(self, variant_id: str, inventory_set_levels_request: InventorySetLevelsRequest):
        """Create or update the stock levels for a variant.

        Args:
            variant_id: The merchant-provided identifier for the variant.
            inventory_set_levels_request: The stock levels to set.
        Returns:
            ResponseWrapper with InventoryLevels data.
        Raises:
            CheckoutApiException on 404/422; see `adjust_inventory` for the error body shape and
            how this SDK surfaces it.
        """
        return self._api_client.put(self.build_path(self.__INVENTORY_PATH, variant_id),
                                    self._sdk_authorization(),
                                    inventory_set_levels_request)

    def get_inventory_product(self, variant_id: str):
        """Retrieve product knowledge (merchandising metadata) for a variant.

        Beta: this endpoint is marked Beta in the specification.

        Args:
            variant_id: The merchant-provided identifier for the variant.
        Returns:
            ResponseWrapper with InventoryProductKnowledge data.
        Raises:
            CheckoutApiException on 404; see `adjust_inventory` for the error body shape and how
            this SDK surfaces it.
        """
        return self._api_client.get(
            self.build_path(self.__INVENTORY_PATH, variant_id, self.__PRODUCT_PATH),
            self._sdk_authorization())

    def set_inventory_product(self, variant_id: str, inventory_set_product_request: InventorySetProductRequest):
        """Create or update product knowledge (merchandising metadata) for a variant.

        Beta: this endpoint is marked Beta in the specification.

        Args:
            variant_id: The merchant-provided identifier for the variant.
            inventory_set_product_request: The product knowledge to set.
        Returns:
            ResponseWrapper with InventoryProductKnowledge data.
        Raises:
            CheckoutApiException on 404/422; see `adjust_inventory` for the error body shape and
            how this SDK surfaces it.
        """
        return self._api_client.put(
            self.build_path(self.__INVENTORY_PATH, variant_id, self.__PRODUCT_PATH),
            self._sdk_authorization(),
            inventory_set_product_request)

    def delete_inventory_product(self, variant_id: str):
        """Delete product knowledge (merchandising metadata) for a variant.

        Beta: this endpoint is marked Beta in the specification.

        Args:
            variant_id: The merchant-provided identifier for the variant.
        Returns:
            ResponseWrapper with no body (204).
        Raises:
            CheckoutApiException on 404; see `adjust_inventory` for the error body shape and how
            this SDK surfaces it.
        """
        return self._api_client.delete(
            self.build_path(self.__INVENTORY_PATH, variant_id, self.__PRODUCT_PATH),
            self._sdk_authorization())
