from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.customers.customers_four import CustomerRequest


class CustomersClient(Client):
    __CUSTOMERS_PATH = 'customers'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def get(self, customer_id: str):
        return self._api_client.get(self.build_path(self.__CUSTOMERS_PATH, customer_id),
                                    self._sdk_authorization())

    def create(self, customer_request: CustomerRequest):
        return self._api_client.post(self.__CUSTOMERS_PATH,
                                     self._sdk_authorization(),
                                     customer_request)

    def update(self, customer_id: str, customer_request: CustomerRequest):
        return self._api_client.patch(self.build_path(self.__CUSTOMERS_PATH, customer_id),
                                      self._sdk_authorization(),
                                      customer_request)

    def delete(self, customer_id: str):
        return self._api_client.delete(self.build_path(self.__CUSTOMERS_PATH, customer_id),
                                       self._sdk_authorization())
