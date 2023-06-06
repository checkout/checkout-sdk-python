from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.issuing.cardholders import CardholderRequest
from checkout_sdk.issuing.cards import CardRequest, ThreeDsEnrollmentRequest, UpdateThreeDsEnrollmentRequest, \
    CardCredentialsQuery, RevokeRequest, SuspendRequest
from checkout_sdk.issuing.controls import CardControlRequest, CardControlsQuery, UpdateCardControlRequest
from checkout_sdk.issuing.testing import CardAuthorizationRequest, SimulationRequest


class IssuingClient(Client):
    __ISSUING = 'issuing'
    __CARDHOLDERS = 'cardholders'
    __CARDS = 'cards'
    __THREE_DS = '3ds-enrollment'
    __ACTIVATE = 'activate'
    __CREDENTIALS = 'credentials'
    __REVOKE = 'revoke'
    __SUSPEND = 'suspend'
    __CONTROLS = 'controls'
    __SIMULATE = 'simulate'
    __AUTHORIZATIONS = 'authorizations'
    __PRESENTMENTS = 'presentments'
    __REVERSALS = 'reversals'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def create_cardholder(self, cardholder_request: CardholderRequest):
        return self._api_client.post(self.build_path(self.__ISSUING, self.__CARDHOLDERS),
                                     self._sdk_authorization(),
                                     cardholder_request)

    def get_cardholder(self, cardholder_id: str):
        return self._api_client.get(self.build_path(self.__ISSUING, self.__CARDHOLDERS, cardholder_id),
                                    self._sdk_authorization())

    def get_cardholder_cards(self, cardholder_id: str):
        return self._api_client.get(self.build_path(self.__ISSUING, self.__CARDHOLDERS, cardholder_id, self.__CARDS),
                                    self._sdk_authorization())

    def create_card(self, card_request: CardRequest):
        return self._api_client.post(self.build_path(self.__ISSUING, self.__CARDS),
                                     self._sdk_authorization(),
                                     card_request)

    def get_card_details(self, card_id: str):
        return self._api_client.get(self.build_path(self.__ISSUING, self.__CARDS, card_id),
                                    self._sdk_authorization())

    def enroll_three_ds(self, card_id: str, three_ds_enrollment_request: ThreeDsEnrollmentRequest):
        return self._api_client.post(self.build_path(self.__ISSUING, self.__CARDS, card_id, self.__THREE_DS),
                                     self._sdk_authorization(),
                                     three_ds_enrollment_request)

    def update_three_ds_enrollment(self, card_id: str, update_three_ds_enrollment: UpdateThreeDsEnrollmentRequest):
        return self._api_client.patch(self.build_path(self.__ISSUING, self.__CARDS, card_id, self.__THREE_DS),
                                      self._sdk_authorization(),
                                      update_three_ds_enrollment)

    def get_three_ds_details(self, card_id: str):
        return self._api_client.get(self.build_path(self.__ISSUING, self.__CARDS, card_id, self.__THREE_DS),
                                    self._sdk_authorization())

    def activate_card(self, card_id: str):
        return self._api_client.post(self.build_path(self.__ISSUING, self.__CARDS, card_id, self.__ACTIVATE),
                                     self._sdk_authorization())

    def get_card_credentials(self, card_id: str, card_credentials_query: CardCredentialsQuery):
        return self._api_client.get(self.build_path(self.__ISSUING, self.__CARDS, card_id, self.__CREDENTIALS),
                                    self._sdk_authorization(),
                                    card_credentials_query)

    def revoke_card(self, card_id: str, revoke_request: RevokeRequest):
        return self._api_client.post(self.build_path(self.__ISSUING, self.__CARDS, card_id, self.__REVOKE),
                                     self._sdk_authorization(),
                                     revoke_request)

    def suspend_card(self, card_id: str, suspend_request: SuspendRequest):
        return self._api_client.post(self.build_path(self.__ISSUING, self.__CARDS, card_id, self.__SUSPEND),
                                     self._sdk_authorization(),
                                     suspend_request)

    def create_control(self, control_request: CardControlRequest):
        return self._api_client.post(self.build_path(self.__ISSUING, self.__CONTROLS),
                                     self._sdk_authorization(),
                                     control_request)

    def get_card_controls(self, query: CardControlsQuery):
        return self._api_client.get(self.build_path(self.__ISSUING, self.__CONTROLS),
                                    self._sdk_authorization(),
                                    query)

    def get_card_control_details(self, control_id: str):
        return self._api_client.get(self.build_path(self.__ISSUING, self.__CONTROLS, control_id),
                                    self._sdk_authorization())

    def update_card_control(self, control_id: str, update_request: UpdateCardControlRequest):
        return self._api_client.put(self.build_path(self.__ISSUING, self.__CONTROLS, control_id),
                                    self._sdk_authorization(),
                                    update_request)

    def remove_control(self, control_id: str):
        return self._api_client.delete(self.build_path(self.__ISSUING, self.__CONTROLS, control_id),
                                       self._sdk_authorization())

    def simulate_authorization(self, authorization_request: CardAuthorizationRequest):
        return self._api_client.post(self.build_path(self.__ISSUING, self.__SIMULATE, self.__AUTHORIZATIONS),
                                     self._sdk_authorization(),
                                     authorization_request)

    def simulate_increment(self, transaction_id: str, increment_request: SimulationRequest):
        return self._api_client.post(
            self.build_path(
                self.__ISSUING, self.__SIMULATE, self.__AUTHORIZATIONS, transaction_id, self.__AUTHORIZATIONS),
            self._sdk_authorization(),
            increment_request)

    def simulate_clearing(self, transaction_id: str, clearing_request: SimulationRequest):
        return self._api_client.post(
            self.build_path(
                self.__ISSUING, self.__SIMULATE, self.__AUTHORIZATIONS, transaction_id, self.__PRESENTMENTS),
            self._sdk_authorization(),
            clearing_request)

    def simulate_reversal(self, transaction_id: str, reversal_request: SimulationRequest):
        return self._api_client.post(
            self.build_path(
                self.__ISSUING, self.__SIMULATE, self.__AUTHORIZATIONS, transaction_id, self.__REVERSALS),
            self._sdk_authorization(),
            reversal_request)
