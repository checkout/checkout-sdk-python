from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.metadata.metadata import CardMetadataRequest


class CardMetadataClient(Client):
    __CARD_METADATA_PATH = 'metadata/card'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def request_card_metadata(self, card_metadata_request: CardMetadataRequest):
        return self._api_client.post(self.__CARD_METADATA_PATH, self._sdk_authorization(), card_metadata_request)
