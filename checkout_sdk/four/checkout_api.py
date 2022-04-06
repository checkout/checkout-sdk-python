from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.customers.customers_client_four import CustomersClient
from checkout_sdk.disputes.disputes_client import DisputesClient
from checkout_sdk.forex.forex_client import ForexClient
from checkout_sdk.four.checkout_four_apm_api import CheckoutApmApi
from checkout_sdk.instruments.instruments_four_client import InstrumentsClient
from checkout_sdk.marketplace.marketplace_client import MarketplaceClient
from checkout_sdk.payments.hosted.hosted_payments_client import HostedPaymentsClient
from checkout_sdk.payments.links.payments_client import PaymentsLinksClient
from checkout_sdk.payments.payments_client_four import PaymentsClient
from checkout_sdk.risk.risk_client import RiskClient
from checkout_sdk.sessions.sessions_client import SessionsClient
from checkout_sdk.tokens.tokens_client import TokensClient
from checkout_sdk.workflows.workflows_client import WorkflowsClient


def _base_api_client(configuration: CheckoutConfiguration) -> ApiClient:
    return ApiClient(configuration, configuration.environment.base_uri)


def _files_api_client(configuration: CheckoutConfiguration) -> ApiClient:
    return ApiClient(configuration, configuration.environment.files_uri)


def _transfers_api_client(configuration: CheckoutConfiguration) -> ApiClient:
    return ApiClient(configuration, configuration.environment.transfers_uri)


def _balances_api_client(configuration: CheckoutConfiguration) -> ApiClient:
    return ApiClient(configuration, configuration.environment.balances_uri)


class CheckoutApi(CheckoutApmApi):

    def __init__(self, configuration: CheckoutConfiguration):
        base_api_client = _base_api_client(configuration)
        super().__init__(base_api_client, configuration)
        self.tokens = TokensClient(api_client=base_api_client, configuration=configuration)
        self.customers = CustomersClient(api_client=base_api_client, configuration=configuration)
        self.instruments = InstrumentsClient(api_client=base_api_client, configuration=configuration)
        self.payments = PaymentsClient(api_client=base_api_client, configuration=configuration)
        self.sessions = SessionsClient(api_client=base_api_client, configuration=configuration)
        self.disputes = DisputesClient(api_client=base_api_client, configuration=configuration)
        self.forex = ForexClient(api_client=base_api_client, configuration=configuration)
        self.hosted_payments = HostedPaymentsClient(api_client=base_api_client, configuration=configuration)
        self.payments_links = PaymentsLinksClient(api_client=base_api_client, configuration=configuration)
        self.risk = RiskClient(api_client=base_api_client, configuration=configuration)
        self.workflows = WorkflowsClient(api_client=base_api_client, configuration=configuration)
        self.marketplace = MarketplaceClient(api_client=base_api_client,
                                             files_client=_files_api_client(configuration),
                                             transfers_client=_transfers_api_client(configuration),
                                             balances_client=_balances_api_client(configuration),
                                             configuration=configuration)
