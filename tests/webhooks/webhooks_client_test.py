import pytest

from checkout_sdk.webhooks.webhooks import WebhookRequest
from checkout_sdk.webhooks.webhooks_client import WebhooksClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return WebhooksClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestWebhooksClient:

    def test_retrieve_webhooks(self, mocker, client: WebhooksClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.retrieve_webhooks() == 'response'

    def test_register_webhook(self, mocker, client: WebhooksClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.register_webhook(WebhookRequest()) == 'response'

    def test_retrieve_webhook(self, mocker, client: WebhooksClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.retrieve_webhook('webhook_id') == 'response'

    def test_update_webhook(self, mocker, client: WebhooksClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        assert client.update_webhook('webhook_id', WebhookRequest()) == 'response'

    def test_patch_webhook(self, mocker, client: WebhooksClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        assert client.patch_webhook('webhook_id', WebhookRequest()) == 'response'

    def test_remove_webhook(self, mocker, client: WebhooksClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')
        assert client.remove_webhook('webhook_id') == 'response'
