from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.events.events import RetrieveEventsRequest


class EventsClient(Client):
    __EVENTS_PATH = 'events'
    __NOTIFICATIONS_PATH = 'notifications'
    __WEBHOOKS_PATH = 'webhooks'
    __RETRY_PATH = 'retry'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY)

    def retrieve_all_event_types(self, version: str = None):
        event_types_path = "event-types"
        if version is not None:
            event_types_path += "?version=" + version
        return self._api_client.get(event_types_path, self._sdk_authorization())

    def retrieve_events(self, events_request: RetrieveEventsRequest):
        return self._api_client.get(self.__EVENTS_PATH, self._sdk_authorization(), events_request)

    def retrieve_event(self, event_id: str):
        return self._api_client.get(self.build_path(self.__EVENTS_PATH, event_id), self._sdk_authorization())

    def retrieve_event_notification(self, event_id: str, notification_id: str):
        return self._api_client.get(
            self.build_path(self.__EVENTS_PATH, event_id, self.__NOTIFICATIONS_PATH, notification_id),
            self._sdk_authorization())

    def retry_webhook(self, event_id: str, webhook_id: str):
        return self._api_client.post(
            self.build_path(self.__EVENTS_PATH, event_id, self.__WEBHOOKS_PATH, webhook_id, self.__RETRY_PATH),
            self._sdk_authorization())

    def retry_all_webhooks(self, event_id: str):
        return self._api_client.post(
            self.build_path(self.__EVENTS_PATH, event_id, self.__WEBHOOKS_PATH, self.__RETRY_PATH),
            self._sdk_authorization())
