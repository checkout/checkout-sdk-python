from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.checkout_apm_api import CheckoutApmApi
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.customers.customers_client import CustomersClient
from checkout_sdk.disputes.disputes_client import DisputesClient
from checkout_sdk.instruments.instruments_client import InstrumentsClient
from checkout_sdk.payments.hosted.hosted_payments_client import HostedPaymentsClient
from checkout_sdk.payments.links.payments_client import PaymentsLinksClient
from checkout_sdk.payments.payments_client import PaymentsClient
from checkout_sdk.risk.risk_client import RiskClient
from checkout_sdk.sources.sources_client import SourcesClient
from checkout_sdk.tokens.tokens_client import TokensClient


class CheckoutApi(CheckoutApmApi):

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client, configuration)
        self.tokens = TokensClient(api_client=api_client, configuration=configuration)
        self.sources = SourcesClient(api_client=api_client, configuration=configuration)
        self.customers = CustomersClient(api_client=api_client, configuration=configuration)
        self.instruments = InstrumentsClient(api_client=api_client, configuration=configuration)
        self.payments = PaymentsClient(api_client=api_client, configuration=configuration)
        self.disputes = DisputesClient(api_client=api_client, configuration=configuration)
        self.hosted_payments = HostedPaymentsClient(api_client=api_client, configuration=configuration)
        self.payments_links = PaymentsLinksClient(api_client=api_client, configuration=configuration)
        self.risk = RiskClient(api_client=api_client, configuration=configuration)
