from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.payments.hosted.hosted_payments import HostedPaymentsSessionRequest


class HostedPaymentsClient(Client):
    __HOSTED_PAYMENTS_PATH = 'hosted-payments'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY)

    def get_hosted_payments_page_details(self, hosted_payment_id: str):
        return self._api_client.get(self.build_path(self.__HOSTED_PAYMENTS_PATH, hosted_payment_id),
                                    self._sdk_authorization())

    def create_hosted_payments_page_session(self, hosted_payments_session_request: HostedPaymentsSessionRequest):
        return self._api_client.post(self.__HOSTED_PAYMENTS_PATH, self._sdk_authorization(),
                                     hosted_payments_session_request)
