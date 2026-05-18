import pytest

from tests._assertions import assert_api_call
from checkout_sdk.sources.sources import SepaSourceRequest
from checkout_sdk.sources.sources_client import SourcesClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return SourcesClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestSourcesClient:

    def test_should_create_sepa_source(self, mocker, client: SourcesClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = SepaSourceRequest()

        assert client.create_sepa_source(body) == 'response'
        assert_api_call(mock, 'sources', body)
