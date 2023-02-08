from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.financial.financial import FinancialActionsQuery


class FinancialClient(Client):
    __FINANCIAL_ACTIONS_PATH = 'financial-actions'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def query(self, query: FinancialActionsQuery):
        return self._api_client.get(self.__FINANCIAL_ACTIONS_PATH, self._sdk_authorization(), query)
