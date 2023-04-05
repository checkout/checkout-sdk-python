from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.forex.forex import QuoteRequest, RatesQueryFilter


class ForexClient(Client):
    __FOREX_PATH = 'forex'
    __QUOTES_PATH = 'quotes'
    __RATES_PATH = 'rates'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.OAUTH)

    def request_quote(self, quote_request: QuoteRequest):
        return self._api_client.post(self.build_path(self.__FOREX_PATH, self.__QUOTES_PATH),
                                     self._sdk_authorization(), quote_request)

    def get_rates(self, rates_query: RatesQueryFilter):
        return self._api_client.get(self.build_path(self.__FOREX_PATH, self.__RATES_PATH),
                                    self._sdk_authorization(), rates_query)
