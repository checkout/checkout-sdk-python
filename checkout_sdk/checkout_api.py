from __future__ import absolute_import

from checkout_sdk.accounts.accounts_client import AccountsClient
from checkout_sdk.api_client import ApiClient
from checkout_sdk.balances.balances_client import BalancesClient
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.customers.customers_client import CustomersClient
from checkout_sdk.disputes.disputes_client import DisputesClient
from checkout_sdk.financial.financial_client import FinancialClient
from checkout_sdk.forex.forex_client import ForexClient
from checkout_sdk.checkout_apm_api import CheckoutApmApi
from checkout_sdk.instruments.instruments_client import InstrumentsClient
from checkout_sdk.issuing.issuing_client import IssuingClient
from checkout_sdk.payments.contexts.contexts_client import PaymentContextsClient
from checkout_sdk.payments.sessions.sessions_client import PaymentSessionsClient
from checkout_sdk.payments.hosted.hosted_payments_client import HostedPaymentsClient
from checkout_sdk.payments.links.payments_client import PaymentsLinksClient
from checkout_sdk.payments.payments_client import PaymentsClient
from checkout_sdk.risk.risk_client import RiskClient
from checkout_sdk.sessions.sessions_client import SessionsClient
from checkout_sdk.tokens.tokens_client import TokensClient
from checkout_sdk.transfers.transfers_client import TransfersClient
from checkout_sdk.workflows.workflows_client import WorkflowsClient
from checkout_sdk.reports.reports_client import ReportsClient
from checkout_sdk.metadata.metadata_client import CardMetadataClient
from checkout_sdk.forward.forward_client import ForwardClient


def _base_api_client(configuration: CheckoutConfiguration) -> ApiClient:
    base_uri = configuration.environment.base_uri
    subdomain = configuration.environment_subdomain

    if subdomain is not None and subdomain.base_uri is not None:
        base_uri = subdomain.base_uri

    return ApiClient(configuration, base_uri)


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
        self.balances = BalancesClient(api_client=_balances_api_client(configuration), configuration=configuration)
        self.transfers = TransfersClient(api_client=_transfers_api_client(configuration), configuration=configuration)
        self.accounts = AccountsClient(api_client=base_api_client,
                                       files_client=_files_api_client(configuration),
                                       configuration=configuration)
        self.reports = ReportsClient(api_client=base_api_client, configuration=configuration)
        self.card_metadata = CardMetadataClient(api_client=base_api_client, configuration=configuration)
        self.financial = FinancialClient(api_client=base_api_client, configuration=configuration)
        self.issuing = IssuingClient(api_client=base_api_client, configuration=configuration)
        self.contexts = PaymentContextsClient(api_client=base_api_client, configuration=configuration)
        self.payment_sessions = PaymentSessionsClient(api_client=base_api_client, configuration=configuration)
        self.forward = ForwardClient(api_client=base_api_client, configuration=configuration)
