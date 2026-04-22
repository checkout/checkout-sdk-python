from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.forward.forward import ForwardRequest, SecretRequest, UpdateSecretRequest


class ForwardClient(Client):
    __FORWARD_PATH = 'forward'
    __SECRETS_PATH = 'secrets'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def forward_request(self, request: ForwardRequest):
        return self._api_client.post(self.__FORWARD_PATH, self._sdk_authorization(), request)

    def get(self, request_id: str):
        return self._api_client.get(self.build_path(self.__FORWARD_PATH, request_id), self._sdk_authorization())

    def create_secret(self, request: SecretRequest):
        return self._api_client.post(
            self.build_path(self.__FORWARD_PATH, self.__SECRETS_PATH),
            self._sdk_authorization(),
            request
        )

    def list_secrets(self):
        return self._api_client.get(
            self.build_path(self.__FORWARD_PATH, self.__SECRETS_PATH),
            self._sdk_authorization()
        )

    def update_secret(self, name: str, request: UpdateSecretRequest):
        return self._api_client.patch(
            self.build_path(self.__FORWARD_PATH, self.__SECRETS_PATH, name),
            self._sdk_authorization(),
            request
        )

    def delete_secret(self, name: str):
        return self._api_client.delete(
            self.build_path(self.__FORWARD_PATH, self.__SECRETS_PATH, name),
            self._sdk_authorization()
        )
