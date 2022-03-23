from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client


class IdealClient(Client):
    __IDEAL_EXTERNAL_PATH = 'ideal-external'
    __ISSUERS_PATH_PATH = 'issuers'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY)

    def get_info(self):
        return self._api_client.get(self.build_path(self.__IDEAL_EXTERNAL_PATH), self._sdk_authorization())

    def get_issuers(self):
        return self._api_client.get(self.build_path(self.__IDEAL_EXTERNAL_PATH, self.__ISSUERS_PATH_PATH),
                                    self._sdk_authorization())
