from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.payments.links.payments_links import PaymentLinkRequest


class PaymentsLinksClient(Client):
    __PAYMENT_LINKS_PATH = 'payment-links'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY)

    def get_payment_link(self, payment_link_id: str):
        return self._api_client.get(self.build_path(self.__PAYMENT_LINKS_PATH, payment_link_id),
                                    self._sdk_authorization())

    def create_payment_link(self, payment_link_request: PaymentLinkRequest):
        return self._api_client.post(self.__PAYMENT_LINKS_PATH, self._sdk_authorization(),
                                     payment_link_request)
