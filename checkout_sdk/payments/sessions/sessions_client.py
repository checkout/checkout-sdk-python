from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.payments.sessions.sessions import PaymentSessionsRequest


class PaymentSessionsClient(Client):
    __PAYMENT_SESSIONS_PATH = 'payment-sessions'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY)

    def create_payment_sessions(self, payment_sessions_request: PaymentSessionsRequest):
        return self._api_client.post(self.__PAYMENT_SESSIONS_PATH, self._sdk_authorization(),
                                     payment_sessions_request)
