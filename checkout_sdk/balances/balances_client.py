from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.balances.balances import BalancesQuery
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client


class BalancesClient(Client):
    __BALANCES_PATH = 'balances'

    def __init__(self, api_client: ApiClient,
                 configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.OAUTH)

    def retrieve_entity_balances(self, entity_id: str, balances_query: BalancesQuery):
        return self._api_client.get(self.build_path(self.__BALANCES_PATH, entity_id), self._sdk_authorization(),
                                    balances_query)
