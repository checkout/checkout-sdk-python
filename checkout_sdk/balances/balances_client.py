from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.balances.balances import BalancesQuery
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client


class BalancesClient(Client):
    __BALANCES_PATH = 'balances'
    __ENTITIES_PATH = 'entities'
    __CURRENCY_ACCOUNTS_PATH = 'currency-accounts'
    __TOP_UP_INSTRUCTIONS_PATH = 'top-up-instructions'

    def __init__(self, api_client: ApiClient,
                 configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def retrieve_entity_balances(self, entity_id: str, balances_query: BalancesQuery):
        return self._api_client.get(self.build_path(self.__BALANCES_PATH, entity_id), self._sdk_authorization(),
                                    balances_query)

    def retrieve_top_up_instructions(self, entity_id: str, currency_account_id: str):
        return self._api_client.get(
            self.build_path(self.__ENTITIES_PATH, entity_id, self.__CURRENCY_ACCOUNTS_PATH, currency_account_id,
                            self.__TOP_UP_INSTRUCTIONS_PATH),
            self._sdk_authorization())
