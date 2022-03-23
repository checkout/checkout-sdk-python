import pytest

from checkout_sdk.tokens.tokens import CardTokenRequest, ApplePayTokenRequest
from checkout_sdk.tokens.tokens_client import TokensClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return TokensClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestTokensClient:

    def test_should_request_token(self, mocker, client: TokensClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.request_card_token(CardTokenRequest()) == 'response'

    def test_should_request_wallet_token(self, mocker, client: TokensClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.request_wallet_token(ApplePayTokenRequest()) == 'response'
