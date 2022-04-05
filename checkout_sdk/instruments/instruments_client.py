from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.instruments.instruments import UpdateInstrumentRequest, CreateInstrumentRequest


class InstrumentsClient(Client):
    __INSTRUMENTS = 'instruments'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY)

    def get(self, instrument_id: str):
        return self._api_client.get(self.build_path(self.__INSTRUMENTS, instrument_id), self._sdk_authorization())

    def create(self, create_instrument_request: CreateInstrumentRequest):
        return self._api_client.post(self.__INSTRUMENTS, self._sdk_authorization(), create_instrument_request)

    def update(self, instrument_id: str, update_instrument_request: UpdateInstrumentRequest):
        return self._api_client.patch(
            self.build_path(self.__INSTRUMENTS, instrument_id),
            self._sdk_authorization(),
            update_instrument_request)

    def delete(self, instrument_id: str):
        return self._api_client.delete(self.build_path(self.__INSTRUMENTS, instrument_id), self._sdk_authorization())
