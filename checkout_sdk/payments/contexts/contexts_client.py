from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.payments.contexts.contexts import PaymentContextsRequest


class PaymentContextsClient(Client):
    __PAYMENT_CONTEXTS_PATH = 'payment-contexts'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def create_payment_contexts(self, payment_contexts_request: PaymentContextsRequest):
        return self._api_client.post(self.__PAYMENT_CONTEXTS_PATH, self._sdk_authorization(),
                                     payment_contexts_request)

    def get_payment_context_details(self, payment_context_id: str):
        return self._api_client.get(self.build_path(self.__PAYMENT_CONTEXTS_PATH, payment_context_id),
                                    self._sdk_authorization())
