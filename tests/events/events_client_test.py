import pytest

from tests._assertions import assert_api_call
from checkout_sdk.events.events import RetrieveEventsRequest
from checkout_sdk.events.events_client import EventsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return EventsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestEventsClient:

    def test_retrieve_all_event_types(self, mocker, client: EventsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.retrieve_all_event_types() == 'response'
        assert_api_call(mock, 'event-types')

    def test_retrieve_events(self, mocker, client: EventsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        query = RetrieveEventsRequest()

        assert client.retrieve_events(query) == 'response'
        assert_api_call(mock, 'events', query)

    def test_retrieve_event(self, mocker, client: EventsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.retrieve_event('event_id') == 'response'
        assert_api_call(mock, 'events/event_id')

    def test_retrieve_event_notification(self, mocker, client: EventsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.retrieve_event_notification('event_id', 'notification_id') == 'response'
        assert_api_call(mock, 'events/event_id/notifications/notification_id')

    def test_retry_webhook(self, mocker, client: EventsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.retry_webhook('event_id', 'webhook_id') == 'response'
        assert_api_call(mock, 'events/event_id/webhooks/webhook_id/retry')

    def test_retry_all_webhooks(self, mocker, client: EventsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.retry_all_webhooks('event_id') == 'response'
        assert_api_call(mock, 'events/event_id/webhooks/retry')
