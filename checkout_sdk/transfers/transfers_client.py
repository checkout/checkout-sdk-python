from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.transfers.transfers import CreateTransferRequest


class TransfersClient(Client):
    __TRANSFERS_PATH = 'transfers'

    def __init__(self, api_client: ApiClient,
                 configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.OAUTH)

    def initiate_transfer_of_funds(self, create_transfer_request: CreateTransferRequest, idempotency_key: str = None):
        return self._api_client.post(self.__TRANSFERS_PATH, self._sdk_authorization(), create_transfer_request,
                                     idempotency_key)

    def retrieve_a_transfer(self, transfer_id):
        return self._api_client.get(self.build_path(self.__TRANSFERS_PATH, transfer_id),
                                    self._sdk_authorization())
