from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.tokens.tokens import WalletTokenRequest, CardTokenRequest


class TokensClient(Client):
    __TOKENS = 'tokens'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.PUBLIC_KEY)

    def request_card_token(self, request: CardTokenRequest):
        return self._api_client.post(self.__TOKENS, self._sdk_authorization(), request)

    def request_wallet_token(self, request: WalletTokenRequest):
        return self._api_client.post(self.__TOKENS, self._sdk_authorization(), request)
