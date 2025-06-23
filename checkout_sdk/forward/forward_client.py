from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.forward.forward import ForwardRequest


class ForwardClient(Client):
    __FORWARD_PATH = 'forward'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def forward_request(self, request: ForwardRequest):
        return self._api_client.post(self.__FORWARD_PATH, self._sdk_authorization(), request)

    def get(self, request_id: str):
        return self._api_client.get(self.build_path(self.__FORWARD_PATH, request_id), self._sdk_authorization())
