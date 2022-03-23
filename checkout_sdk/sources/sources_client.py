from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.sources.sources import SepaSourceRequest


class SourcesClient(Client):

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY)

    def create_sepa_source(self, sepa_source_request: SepaSourceRequest):
        return self._api_client.post('sources', self._sdk_authorization(), sepa_source_request)
