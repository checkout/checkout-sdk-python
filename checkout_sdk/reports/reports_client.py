from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.reports.reports import ReportsQuery


class ReportsClient(Client):
    __REPORTS_PATH = 'reports'
    __FILES_PATH = 'files'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def get_all_reports(self, query: ReportsQuery):
        return self._api_client.get(self.__REPORTS_PATH, self._sdk_authorization(), query)

    def get_report_details(self, report_id: str):
        return self._api_client.get(self.build_path(self.__REPORTS_PATH, report_id), self._sdk_authorization())

    def get_report_file(self, report_id: str, file_id: str):
        return self._api_client.get(self.build_path(self.__REPORTS_PATH, report_id, self.__FILES_PATH, file_id),
                                    self._sdk_authorization())
