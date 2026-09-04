from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.apm.bacs import BacsNotificationRequest
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client


class BacsClient(Client):
    __APMS_PATH = 'apms'
    __BACS_PATH = 'bacs'
    __NOTIFICATIONS_PATH = 'notifications'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY)

    def send_notification(self, bacs_notification_request: BacsNotificationRequest):
        """Sends a Bacs Direct Debit pre-notification (advance notice) to a payer ahead of collecting
        funds from their account.

        Args:
            bacs_notification_request: The pre-notification details.

        Returns:
            The notification event, carrying event_id.
        """
        return self._api_client.post(
            self.build_path(self.__APMS_PATH, self.__BACS_PATH, self.__NOTIFICATIONS_PATH),
            self._sdk_authorization(),
            bacs_notification_request)
