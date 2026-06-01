import pytest

from tests._assertions import assert_api_call
from checkout_sdk.tokens.tokens import CardTokenRequest, ApplePayTokenRequest
from checkout_sdk.tokens.tokens_client import TokensClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return TokensClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestTokensClient:

    def test_should_request_token(self, mocker, client: TokensClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = CardTokenRequest()

        assert client.request_card_token(body) == 'response'
        assert_api_call(mock, 'tokens', body)

    def test_should_request_wallet_token(self, mocker, client: TokensClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = ApplePayTokenRequest()

        assert client.request_wallet_token(body) == 'response'
        assert_api_call(mock, 'tokens', body)

    def test_should_get_token_metadata(self, mocker, client: TokensClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_token_metadata('tok_123') == 'response'
        assert_api_call(mock, 'tokens/tok_123/metadata')
