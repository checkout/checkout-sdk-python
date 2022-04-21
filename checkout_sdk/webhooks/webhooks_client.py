from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.webhooks.webhooks import WebhookRequest


class WebhooksClient(Client):
    __WEBHOOKS_PATH = 'webhooks'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY)

    def retrieve_webhooks(self):
        return self._api_client.get(self.__WEBHOOKS_PATH, self._sdk_authorization())

    def register_webhook(self, webhook_request: WebhookRequest):
        return self._api_client.post(self.__WEBHOOKS_PATH, self._sdk_authorization(), webhook_request)

    def retrieve_webhook(self, webhook_id: str):
        return self._api_client.get(self.build_path(self.__WEBHOOKS_PATH, webhook_id), self._sdk_authorization())

    def update_webhook(self, webhook_id: str, webhook_request: WebhookRequest):
        return self._api_client.put(self.build_path(self.__WEBHOOKS_PATH, webhook_id),
                                    self._sdk_authorization(), webhook_request)

    def patch_webhook(self, webhook_id: str, webhook_request: WebhookRequest):
        return self._api_client.patch(self.build_path(self.__WEBHOOKS_PATH, webhook_id),
                                      self._sdk_authorization(), webhook_request)

    def remove_webhook(self, webhook_id: str):
        return self._api_client.delete(self.build_path(self.__WEBHOOKS_PATH, webhook_id), self._sdk_authorization())
