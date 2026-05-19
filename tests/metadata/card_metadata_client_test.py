import pytest

from tests._assertions import assert_api_call
from checkout_sdk.metadata.metadata import CardMetadataRequest
from checkout_sdk.metadata.metadata_client import CardMetadataClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return CardMetadataClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestCardMetadataClient:

    def test_should_request_card_metadata(self, mocker, client: CardMetadataClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = CardMetadataRequest()

        assert client.request_card_metadata(body) == 'response'
        assert_api_call(mock, 'metadata/card', body)
