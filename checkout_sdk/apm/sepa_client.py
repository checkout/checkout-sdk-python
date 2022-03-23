from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client


class SepaClient(Client):
    __SEPA_MANDATES_PATH = 'sepa/mandates'
    __PPRO_PATH = 'ppro'
    __CANCEL_PATH = 'cancel'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY)

    def get_mandate(self, mandate_id: str):
        return self._api_client.get(self.build_path(self.__SEPA_MANDATES_PATH, mandate_id), self._sdk_authorization())

    def cancel_mandate(self, mandate_id: str):
        return self._api_client.post(self.build_path(self.__SEPA_MANDATES_PATH, mandate_id, self.__CANCEL_PATH),
                                     self._sdk_authorization())

    def get_mandate_via_ppro(self, mandate_id: str):
        return self._api_client.get(self.build_path(self.__PPRO_PATH, self.__SEPA_MANDATES_PATH, mandate_id),
                                    self._sdk_authorization())

    def cancel_mandate_via_ppro(self, mandate_id: str):
        return self._api_client.post(self.build_path(self.__PPRO_PATH, self.__SEPA_MANDATES_PATH, mandate_id,
                                                     self.__CANCEL_PATH), self._sdk_authorization())
