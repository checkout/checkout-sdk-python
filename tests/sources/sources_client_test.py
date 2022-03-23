import pytest

from checkout_sdk.sources.sources import SepaSourceRequest
from checkout_sdk.sources.sources_client import SourcesClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return SourcesClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestSourcesClient:

    def test_should_create_sepa_source(self, mocker, client: SourcesClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_sepa_source(SepaSourceRequest()) == 'response'
