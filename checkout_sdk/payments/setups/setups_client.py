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
        """Create a Payment Setup (POST /payments/setups).

        Args:
            payment_setups_request: The Payment Setup request body. To offer Cash App Pay, set
                payment_methods.cashapp (initialization, customer_profile_sharing) and
                customer.device.client.
        Returns:
            ResponseWrapper with the Payment Setup. For Cash App Pay, the customer is sent to
            payment_methods.cashapp.action.redirect_url to authorize the payment.
        """
        return self._api_client.post(
            self.build_path(self.__PAYMENTS_PATH, self.__SETUPS_PATH),
            self._sdk_authorization(),
            payment_setups_request
        )

    def update_payment_setup(self, setup_id: str, payment_setups_request: PaymentSetupsRequest):
        """Update a Payment Setup (PUT /payments/setups/{id}).

        Args:
            setup_id: The unique identifier of the Payment Setup to update.
            payment_setups_request: The Payment Setup request body.
        Returns:
            ResponseWrapper with the updated Payment Setup.
        """
        return self._api_client.put(
            self.build_path(self.__PAYMENTS_PATH, self.__SETUPS_PATH, setup_id),
            self._sdk_authorization(),
            payment_setups_request
        )

    def get_payment_setup(self, setup_id: str):
        """Retrieve a Payment Setup (GET /payments/setups/{id}).

        Args:
            setup_id: The unique identifier of the Payment Setup to retrieve.
        Returns:
            ResponseWrapper with the Payment Setup. For Cash App Pay with
            customer_profile_sharing enabled, payment_methods.cashapp.customer_profile is
            present only in the first successful response after the customer authorizes the
            payment, so store it on first read.
        """
        return self._api_client.get(
            self.build_path(self.__PAYMENTS_PATH, self.__SETUPS_PATH, setup_id),
            self._sdk_authorization()
        )

    def confirm_payment_setup(self, setup_id: str, payment_method_name: str):
        """Confirm a Payment Setup (POST /payments/setups/{id}/confirm/{payment_method_name}).

        Args:
            setup_id: The unique identifier of the Payment Setup to confirm.
            payment_method_name: The name of the payment method to confirm the Payment Setup
                with. For example, card, klarna, tabby or cashapp.
        Returns:
            ResponseWrapper with the Payment Setup.
        """
        return self._api_client.post(
            self.build_path(self.__PAYMENTS_PATH, self.__SETUPS_PATH, setup_id,
                            self.__CONFIRM_PATH, payment_method_name),
            self._sdk_authorization()
        )
