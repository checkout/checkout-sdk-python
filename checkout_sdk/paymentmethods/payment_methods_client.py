from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.paymentmethods.payment_methods import PaymentMethodsQueryFilter


class PaymentMethodsClient(Client):
    __PAYMENT_METHODS_PATH = 'payment-methods'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def get_available_payment_methods(self, processing_channel_id: str):
        query = PaymentMethodsQueryFilter()
        query.processing_channel_id = processing_channel_id
        return self._api_client.get(self.__PAYMENT_METHODS_PATH, self._sdk_authorization(), query)
