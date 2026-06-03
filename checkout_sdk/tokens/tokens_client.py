from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.tokens.tokens import WalletTokenRequest, CardTokenRequest, CvvTokenRequest, PinTokenRequest


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

    def request_cvv_token(self, request: CvvTokenRequest):
        return self._api_client.post(self.__TOKENS, self._sdk_authorization(), request)

    def request_pin_token(self, request: PinTokenRequest):
        return self._api_client.post(self.__TOKENS, self._sdk_authorization(), request)

    def get_token_metadata(self, token_id: str):
        return self._api_client.get(
            self.build_path(self.__TOKENS, token_id, 'metadata'),
            self._sdk_authorization(AuthorizationType.SECRET_KEY_OR_OAUTH)
        )
