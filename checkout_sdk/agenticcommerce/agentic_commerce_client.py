from __future__ import absolute_import

from checkout_sdk.agenticcommerce.agentic_commerce import DelegatedPaymentRequest, DelegatedPaymentHeaders
from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client


class AgenticCommerceClient(Client):
    __AGENTIC_COMMERCE_PATH = 'agentic_commerce'
    __DELEGATE_PAYMENT_PATH = 'delegate_payment'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY)

    def create_delegated_payment_token(self, request: DelegatedPaymentRequest, headers: DelegatedPaymentHeaders):
        return self._api_client.post(
            self.build_path(self.__AGENTIC_COMMERCE_PATH, self.__DELEGATE_PAYMENT_PATH),
            self._sdk_authorization(),
            request,
            headers = headers
        )