from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.identities.amlscreening.amlscreening import AmlScreeningRequest


class AmlScreeningClient(Client):
    __AML_PATH = 'aml-verifications'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def create_aml_screening(self, request: AmlScreeningRequest):
        return self._api_client.post(self.__AML_PATH,
                                     self._sdk_authorization(),
                                     request)

    def get_aml_screening(self, aml_verification_id: str):
        return self._api_client.get(self.build_path(self.__AML_PATH, aml_verification_id),
                                    self._sdk_authorization())
