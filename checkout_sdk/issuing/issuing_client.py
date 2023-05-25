from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.issuing.cardholders import CardholderRequest


class IssuingClient(Client):
    __ISSUING = 'issuing'
    __CARDHOLDERS = 'cardholders'
    __CARDS = 'cards'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def create_cardholder(self, cardholder_request: CardholderRequest):
        return self._api_client.post(self.build_path(self.__ISSUING, self.__CARDHOLDERS),
                                     self._sdk_authorization(),
                                     cardholder_request)

    def get_cardholder(self, cardholder_id: str):
        return self._api_client.get(self.build_path(self.__ISSUING, self.__CARDHOLDERS, cardholder_id),
                                    self._sdk_authorization())

    def get_cardholder_cards(self, cardholder_id: str):
        return self._api_client.get(self.build_path(self.__ISSUING, self.__CARDHOLDERS, cardholder_id, self.__CARDS),
                                    self._sdk_authorization())
