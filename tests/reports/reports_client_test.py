import pytest

from tests._assertions import assert_api_call
from checkout_sdk.reports.reports import ReportsQuery
from checkout_sdk.reports.reports_client import ReportsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return ReportsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestReportsClient:

    def test_should_get_all_reports(self, mocker, client: ReportsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        query = ReportsQuery()

        assert client.get_all_reports(query) == 'response'
        assert_api_call(mock, 'reports', query)

    def test_should_get_report_details(self, mocker, client: ReportsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_report_details('report_id') == 'response'
        assert_api_call(mock, 'reports/report_id')

    def test_should_get_report_file(self, mocker, client: ReportsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_report_file('report_id', 'file_id') == 'response'
        assert_api_call(mock, 'reports/report_id/files/file_id')
