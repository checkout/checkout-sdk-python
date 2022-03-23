from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.forex.forex import QuoteRequest


class ForexClient(Client):
    __FOREX_PATH = 'forex/quotes'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.OAUTH)

    def request_quote(self, quote_request: QuoteRequest):
        return self._api_client.post(self.__FOREX_PATH, self._sdk_authorization(), quote_request)
