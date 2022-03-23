from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.files.files import FileRequest
from checkout_sdk.marketplace.marketplace import OnboardEntityRequest, MarketplacePaymentInstrument


class MarketplaceClient(Client):
    __MARKETPLACE_PATH = 'marketplace'
    __INSTRUMENTS_PATH = 'instruments'
    __ENTITIES_PATH = 'entities'
    __FILES_PATH = 'files'

    def __init__(self, api_client: ApiClient, files_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.OAUTH)
        self.__files_client = files_client

    def create_entity(self, onboard_entity_request: OnboardEntityRequest):
        return self._api_client.post(self.build_path(self.__MARKETPLACE_PATH, self.__ENTITIES_PATH),
                                     self._sdk_authorization(), onboard_entity_request)

    def get_entity(self, entity_id: str):
        return self._api_client.get(self.build_path(self.__MARKETPLACE_PATH, self.__ENTITIES_PATH, entity_id),
                                    self._sdk_authorization())

    def update_entity(self, entity_id: str, onboard_entity_request: OnboardEntityRequest):
        return self._api_client.put(self.build_path(self.__MARKETPLACE_PATH, self.__ENTITIES_PATH, entity_id),
                                    self._sdk_authorization(), onboard_entity_request)

    def create_payment_instrument(self, entity_id: str, marketplace_payment_instrument: MarketplacePaymentInstrument):
        return self._api_client.post(
            self.build_path(self.__MARKETPLACE_PATH, self.__ENTITIES_PATH, entity_id, self.__INSTRUMENTS_PATH),
            self._sdk_authorization(), marketplace_payment_instrument)

    def upload_file(self, file_request: FileRequest):
        return self.__files_client.submit_file(self.__FILES_PATH, self._sdk_authorization(), file_request,
                                               multipart_file='path')
