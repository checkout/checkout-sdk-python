from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.common.common import QueryFilterDateRange
from checkout_sdk.reconciliation.reconciliation import ReconciliationQueryFilter


class ReconciliationClient(Client):
    __REPORTING_PATH = 'reporting'
    __PAYMENTS_PATH = 'payments'
    __DOWNLOAD_PATH = 'download'
    __STATEMENTS_PATH = 'statements'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY)

    def query_payments_report(self, query: ReconciliationQueryFilter):
        return self._api_client.get(self.build_path(self.__REPORTING_PATH, self.__PAYMENTS_PATH),
                                    self._sdk_authorization(),
                                    query)

    def single_payment_report(self, payment_id: str):
        return self._api_client.get(self.build_path(self.__REPORTING_PATH, self.__PAYMENTS_PATH, payment_id),
                                    self._sdk_authorization())

    def query_statements_report(self, query: QueryFilterDateRange):
        return self._api_client.get(self.build_path(self.__REPORTING_PATH, self.__STATEMENTS_PATH),
                                    self._sdk_authorization(),
                                    query)

    def retrieve_csv_payment_report(self, query: QueryFilterDateRange):
        return self._api_client.get(self.build_path(self.__REPORTING_PATH, self.__PAYMENTS_PATH, self.__DOWNLOAD_PATH),
                                    self._sdk_authorization(),
                                    query)

    def retrieve_csv_single_statement_report(self, statement_id: str):
        return self._api_client.get(
            self.build_path(self.__REPORTING_PATH, self.__STATEMENTS_PATH, statement_id, self.__PAYMENTS_PATH,
                            self.__DOWNLOAD_PATH),
            self._sdk_authorization())

    def retrieve_csv_statements_report(self, query: QueryFilterDateRange):
        return self._api_client.get(
            self.build_path(self.__REPORTING_PATH, self.__STATEMENTS_PATH, self.__DOWNLOAD_PATH),
            self._sdk_authorization(),
            query)
