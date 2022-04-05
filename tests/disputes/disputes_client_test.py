import pytest

from checkout_sdk.disputes.disputes import DisputesQueryFilter, DisputeEvidenceRequest
from checkout_sdk.disputes.disputes_client import DisputesClient
from checkout_sdk.files.files import FileRequest


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return DisputesClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestDisputesClient:

    def test_should_query_dispute(self, mocker, client: DisputesClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.query(DisputesQueryFilter()) == 'response'

    def test_should_get_dispute_details(self, mocker, client: DisputesClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_dispute_details('dispute_id') == 'response'

    def test_should_accept_dispute(self, mocker, client: DisputesClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.accept('customer_id') == 'response'

    def test_should_put_evidence(self, mocker, client: DisputesClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        assert client.put_evidence('dispute_id', DisputeEvidenceRequest()) == 'response'

    def test_should_get_evidence(self, mocker, client: DisputesClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_evidence('dispute_id') == 'response'

    def test_should_submit_evidence(self, mocker, client: DisputesClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.submit_evidence('dispute_id') == 'response'

    def test_should_upload_file(self, mocker, client: DisputesClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.submit_file', return_value='response')
        assert client.upload_file(FileRequest()) == 'response'

    def test_should_get_file_details(self, mocker, client: DisputesClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_file_details('file_id') == 'response'
