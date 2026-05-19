import pytest

from tests._assertions import assert_api_call
from checkout_sdk.agenticcommerce.agentic_commerce_client import AgenticCommerceClient
from checkout_sdk.agenticcommerce.agentic_commerce import DelegatedPaymentRequest, DelegatedPaymentHeaders


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return AgenticCommerceClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestAgenticCommerceClient:

    def test_create_delegated_payment_token(self, mocker, client: AgenticCommerceClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = DelegatedPaymentRequest()
        headers = DelegatedPaymentHeaders()

        assert client.create_delegated_payment_token(body, headers) == 'response'
        assert_api_call(mock, 'agentic_commerce/delegate_payment', body)
        # Verify headers are forwarded as a kwarg (not part of positional args)
        assert mock.call_args.kwargs.get('headers') is headers

    def test_create_delegated_payment_token_with_none_request(self, mocker, client: AgenticCommerceClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.create_delegated_payment_token(None, DelegatedPaymentHeaders()) == 'response'
        # Body=None — verify path only; positional args[2] is the None body.
        assert_api_call(mock, 'agentic_commerce/delegate_payment')
        assert mock.call_args.args[2] is None

    def test_create_delegated_payment_token_with_none_headers(self, mocker, client: AgenticCommerceClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = DelegatedPaymentRequest()

        assert client.create_delegated_payment_token(body, None) == 'response'
        assert_api_call(mock, 'agentic_commerce/delegate_payment', body)
        assert mock.call_args.kwargs.get('headers') is None
