from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.networktokens.network_tokens import ProvisionNetworkTokenRequest, RequestCryptogramRequest, \
    DeleteNetworkTokenRequest


class NetworkTokensClient(Client):
    __NETWORK_TOKENS_PATH = 'network-tokens'
    __CRYPTOGRAMS_PATH = 'cryptograms'
    __DELETE_PATH = 'delete'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.OAUTH)

    def provision_network_token(self, provision_network_token_request: ProvisionNetworkTokenRequest):
        return self._api_client.post(self.__NETWORK_TOKENS_PATH,
                                     self._sdk_authorization(),
                                     provision_network_token_request)

    def get_network_token(self, network_token_id: str):
        return self._api_client.get(self.build_path(self.__NETWORK_TOKENS_PATH, network_token_id),
                                    self._sdk_authorization())

    def request_cryptogram(self, network_token_id: str,
                           request_cryptogram_request: RequestCryptogramRequest):
        return self._api_client.post(
            self.build_path(self.__NETWORK_TOKENS_PATH, network_token_id, self.__CRYPTOGRAMS_PATH),
            self._sdk_authorization(),
            request_cryptogram_request)

    def delete_network_token(self, network_token_id: str,
                             delete_network_token_request: DeleteNetworkTokenRequest):
        return self._api_client.patch(
            self.build_path(self.__NETWORK_TOKENS_PATH, network_token_id, self.__DELETE_PATH),
            self._sdk_authorization(),
            delete_network_token_request)
