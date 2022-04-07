from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.payments.payments import PaymentRequest, PayoutRequest, CaptureRequest, RefundRequest, VoidRequest


class PaymentsClient(Client):
    __PAYMENTS_PATH = 'payments'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY)

    def request_payment(self, payment_request: PaymentRequest, idempotency_key: str = None):
        return self._api_client.post(self.__PAYMENTS_PATH,
                                     self._sdk_authorization(),
                                     payment_request,
                                     idempotency_key)

    def request_payout(self, payout_request: PayoutRequest, idempotency_key: str = None):
        return self._api_client.post(self.__PAYMENTS_PATH,
                                     self._sdk_authorization(),
                                     payout_request,
                                     idempotency_key)

    def get_payment_details(self, payment_id: str):
        return self._api_client.get(self.build_path(self.__PAYMENTS_PATH, payment_id),
                                    self._sdk_authorization())

    def get_payment_actions(self, payment_id: str):
        return self._api_client.get(self.build_path(self.__PAYMENTS_PATH, payment_id, 'actions'),
                                    self._sdk_authorization())

    def capture_payment(self, payment_id: str, capture_request: CaptureRequest = None, idempotency_key: str = None):
        return self._api_client.post(self.build_path(self.__PAYMENTS_PATH, payment_id, 'captures'),
                                     self._sdk_authorization(),
                                     capture_request,
                                     idempotency_key)

    def refund_payment(self, payment_id: str, refund_request: RefundRequest = None, idempotency_key: str = None):
        return self._api_client.post(self.build_path(self.__PAYMENTS_PATH, payment_id, 'refunds'),
                                     self._sdk_authorization(),
                                     refund_request,
                                     idempotency_key)

    def void_payment(self, payment_id: str, void_request: VoidRequest = None, idempotency_key: str = None):
        return self._api_client.post(self.build_path(self.__PAYMENTS_PATH, payment_id, 'voids'),
                                     self._sdk_authorization(),
                                     void_request,
                                     idempotency_key)
