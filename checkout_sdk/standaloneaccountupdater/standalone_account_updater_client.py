from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.standaloneaccountupdater.standalone_account_updater import GetUpdatedCardCredentialsRequest


class StandaloneAccountUpdaterClient(Client):
    __ACCOUNT_UPDATER_PATH = 'account-updater/cards'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.OAUTH)

    def get_updated_card_credentials(self, request: GetUpdatedCardCredentialsRequest):
        return self._api_client.post(self.__ACCOUNT_UPDATER_PATH,
                                     self._sdk_authorization(),
                                     request)
