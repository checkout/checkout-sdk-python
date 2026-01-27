from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.payments.setups.setups import PaymentSetupsRequest


class PaymentSetupsClient(Client):
    __PAYMENTS_PATH = 'payments'
    __SETUPS_PATH = 'setups'
    __CONFIRM_PATH = 'confirm'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def create_payment_setup(self, payment_setups_request: PaymentSetupsRequest):
        """
        Creates a Payment Setup
        """
        return self._api_client.post(
            self.build_path(self.__PAYMENTS_PATH, self.__SETUPS_PATH),
            self._sdk_authorization(),
            payment_setups_request
        )

    def update_payment_setup(self, setup_id: str, payment_setups_request: PaymentSetupsRequest):
        """
        Updates a Payment Setup
        """
        return self._api_client.put(
            self.build_path(self.__PAYMENTS_PATH, self.__SETUPS_PATH, setup_id),
            self._sdk_authorization(),
            payment_setups_request
        )

    def get_payment_setup(self, setup_id: str):
        """
        Gets a Payment Setup
        """
        return self._api_client.get(
            self.build_path(self.__PAYMENTS_PATH, self.__SETUPS_PATH, setup_id),
            self._sdk_authorization()
        )

    def confirm_payment_setup(self, setup_id: str, payment_method_option_id: str):
        """
        Confirms a Payment Setup
        """
        return self._api_client.post(
            self.build_path(self.__PAYMENTS_PATH, self.__SETUPS_PATH, setup_id,
                            self.__CONFIRM_PATH, payment_method_option_id),
            self._sdk_authorization()
        )
