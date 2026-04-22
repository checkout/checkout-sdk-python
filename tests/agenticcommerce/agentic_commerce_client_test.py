import pytest

from checkout_sdk.agenticcommerce.agentic_commerce_client import AgenticCommerceClient
from checkout_sdk.agenticcommerce.agentic_commerce import DelegatedPaymentRequest, DelegatedPaymentHeaders


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return AgenticCommerceClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestAgenticCommerceClient:

    def test_create_delegated_payment_token(self, mocker, client: AgenticCommerceClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        request = DelegatedPaymentRequest()
        headers = DelegatedPaymentHeaders()

        response = client.create_delegated_payment_token(request, headers)

        assert response == 'response'

    def test_create_delegated_payment_token_with_none_request(self, mocker, client: AgenticCommerceClient):
        mock_post = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        headers = DelegatedPaymentHeaders()

        response = client.create_delegated_payment_token(None, headers)

        assert response == 'response'
        mock_post.assert_called_once()
        args = mock_post.call_args[0]
        assert args[2] is None

    def test_create_delegated_payment_token_with_none_headers(self, mocker, client: AgenticCommerceClient):
        mock_post = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        request = DelegatedPaymentRequest()

        response = client.create_delegated_payment_token(request, None)

        assert response == 'response'
        mock_post.assert_called_once()
        kwargs = mock_post.call_args.kwargs
        assert kwargs['headers'] is None

    def test_create_delegated_payment_token_calls_correct_endpoint(self, mocker, client: AgenticCommerceClient):
        mock_post = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        request = DelegatedPaymentRequest()
        headers = DelegatedPaymentHeaders()

        client.create_delegated_payment_token(request, headers)

        mock_post.assert_called_once()
        args = mock_post.call_args[0]
        assert 'agentic_commerce/delegate_payment' in args[0]
