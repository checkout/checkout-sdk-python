import pytest

from tests._assertions import assert_api_call
from checkout_sdk.webhooks.webhooks import WebhookRequest
from checkout_sdk.webhooks.webhooks_client import WebhooksClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return WebhooksClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestWebhooksClient:

    def test_retrieve_webhooks(self, mocker, client: WebhooksClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.retrieve_webhooks() == 'response'
        assert_api_call(mock, 'webhooks')

    def test_register_webhook(self, mocker, client: WebhooksClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = WebhookRequest()

        assert client.register_webhook(body) == 'response'
        assert_api_call(mock, 'webhooks', body)

    def test_retrieve_webhook(self, mocker, client: WebhooksClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.retrieve_webhook('webhook_id') == 'response'
        assert_api_call(mock, 'webhooks/webhook_id')

    def test_update_webhook(self, mocker, client: WebhooksClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        body = WebhookRequest()

        assert client.update_webhook('webhook_id', body) == 'response'
        assert_api_call(mock, 'webhooks/webhook_id', body)

    def test_patch_webhook(self, mocker, client: WebhooksClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        body = WebhookRequest()

        assert client.patch_webhook('webhook_id', body) == 'response'
        assert_api_call(mock, 'webhooks/webhook_id', body)

    def test_remove_webhook(self, mocker, client: WebhooksClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')

        assert client.remove_webhook('webhook_id') == 'response'
        assert_api_call(mock, 'webhooks/webhook_id')
