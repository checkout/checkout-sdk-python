import pytest

from tests._assertions import assert_api_call
from checkout_sdk.disputes.disputes import DisputesQueryFilter, DisputeEvidenceRequest
from checkout_sdk.disputes.disputes_client import DisputesClient
from checkout_sdk.files.files import FileRequest


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return DisputesClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestDisputesClient:

    def test_should_query_dispute(self, mocker, client: DisputesClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        body = DisputesQueryFilter()

        assert client.query(body) == 'response'
        assert_api_call(mock, 'disputes', body)

    def test_should_get_dispute_details(self, mocker, client: DisputesClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_dispute_details('dispute_id') == 'response'
        assert_api_call(mock, 'disputes/dispute_id')

    def test_should_accept_dispute(self, mocker, client: DisputesClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.accept('customer_id') == 'response'
        assert_api_call(mock, 'disputes/customer_id/accept')

    def test_should_put_evidence(self, mocker, client: DisputesClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        body = DisputeEvidenceRequest()

        assert client.put_evidence('dispute_id', body) == 'response'
        assert_api_call(mock, 'disputes/dispute_id/evidence', body)

    def test_should_get_evidence(self, mocker, client: DisputesClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_evidence('dispute_id') == 'response'
        assert_api_call(mock, 'disputes/dispute_id/evidence')

    def test_should_submit_evidence(self, mocker, client: DisputesClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.submit_evidence('dispute_id') == 'response'
        assert_api_call(mock, 'disputes/dispute_id/evidence')

    def test_should_submit_arbitration_evidence(self, mocker, client: DisputesClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.submit_arbitration_evidence('dispute_id') == 'response'
        assert_api_call(mock, 'disputes/dispute_id/evidence/arbitration')

    def test_should_get_compiled_submitted_evidence(self, mocker, client: DisputesClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_compiled_submitted_evidence('dispute_id') == 'response'
        assert_api_call(mock, 'disputes/dispute_id/evidence/submitted')

    def test_should_get_compiled_submitted_arbitration_evidence(self, mocker, client: DisputesClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_compiled_submitted_arbitration_evidence('dispute_id') == 'response'
        assert_api_call(mock, 'disputes/dispute_id/evidence/arbitration/submitted')

    def test_should_upload_file(self, mocker, client: DisputesClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.submit_file', return_value='response')
        body = FileRequest()

        assert client.upload_file(body) == 'response'
        mock.assert_called_once()
        args = mock.call_args.args
        assert args[0] == 'files'
        assert args[2] is body

    def test_should_get_file_details(self, mocker, client: DisputesClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_file_details('file_id') == 'response'
        assert_api_call(mock, 'files/file_id')

    def test_should_get_dispute_scheme_files(self, mocker, client: DisputesClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_dispute_scheme_files('dispute_id') == 'response'
        assert_api_call(mock, 'disputes/dispute_id/schemefiles')
