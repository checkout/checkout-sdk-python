from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.apm.klarna import CreditSessionRequest, OrderCaptureRequest
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.payments.payments import VoidRequest


class KlarnaClient(Client):
    __CREDIT_SESSIONS_PATH = 'credit-sessions'
    __ORDERS_PATH = 'orders'
    __CAPTURES_PATH = 'captures'
    __VOIDS_PATH = 'voids'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY)

    def create_credit_session(self, create_session_request: CreditSessionRequest):
        return self._api_client.post(self.build_path(self.__get_base_url(), self.__CREDIT_SESSIONS_PATH),
                                     self._sdk_authorization(), create_session_request)

    def get_credit_session(self, session_id: str):
        return self._api_client.get(self.build_path(self.__get_base_url(), self.__CREDIT_SESSIONS_PATH, session_id),
                                    self._sdk_authorization())

    def capture_payment(self, payment_id: str, order_capture_request: OrderCaptureRequest):
        return self._api_client.post(
            self.build_path(self.__get_base_url(), self.__ORDERS_PATH, payment_id, self.__CAPTURES_PATH),
            self._sdk_authorization(), order_capture_request)

    def void_payment(self, payment_id: str, void_request: VoidRequest):
        return self._api_client.post(
            self.build_path(self.__get_base_url(), self.__ORDERS_PATH, payment_id, self.__VOIDS_PATH),
            self._sdk_authorization(), void_request)

    def __get_base_url(self):
        return 'klarna-external' if self.is_sandbox() else 'klarna'
