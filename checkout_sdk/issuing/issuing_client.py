from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.issuing.cardholders import CardholderRequest
from checkout_sdk.issuing.cards import CardRequest, ThreeDsEnrollmentRequest, UpdateThreeDsEnrollmentRequest, \
    CardCredentialsQuery, RevokeRequest, SuspendRequest, UpdateCardRequest, RenewCardRequest, \
    ScheduleCardRevocationRequest
from checkout_sdk.issuing.controls import CardControlRequest, CardControlsQuery, UpdateCardControlRequest, \
    CreateControlGroupRequest, ControlGroupQueryTarget, ControlProfileRequest
from checkout_sdk.issuing.disputes import CreateDisputeRequest, EscalateDisputeRequest
from checkout_sdk.issuing.testing import CardAuthorizationRequest, SimulationRequest, \
    CardRefundAuthorizationRequest, SimulateOobAuthenticationRequest
from checkout_sdk.issuing.transactions import TransactionsQueryFilter


class IssuingClient(Client):
    __ISSUING = 'issuing'
    __CARDHOLDERS = 'cardholders'
    __CARDS = 'cards'
    __THREE_DS = '3ds-enrollment'
    __ACTIVATE = 'activate'
    __CREDENTIALS = 'credentials'
    __RENEW = 'renew'
    __REVOKE = 'revoke'
    __SCHEDULE_REVOCATION = 'schedule-revocation'
    __SUSPEND = 'suspend'
    __CONTROLS = 'controls'
    __CONTROL_GROUPS = 'control-groups'
    __CONTROL_PROFILES = 'control-profiles'
    __ADD = 'add'
    __REMOVE = 'remove'
    __DIGITAL_CARDS = 'digital-cards'
    __TRANSACTIONS = 'transactions'
    __DISPUTES = 'disputes'
    __CANCEL = 'cancel'
    __ESCALATE = 'escalate'
    __SIMULATE = 'simulate'
    __AUTHORIZATIONS = 'authorizations'
    __PRESENTMENTS = 'presentments'
    __REVERSALS = 'reversals'
    __REFUNDS = 'refunds'
    __OOB = 'oob'
    __AUTHENTICATION = 'authentication'

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

    def update_cardholder(self, cardholder_id: str, cardholder_request: CardholderRequest):
        return self._api_client.patch(self.build_path(self.__ISSUING, self.__CARDHOLDERS, cardholder_id),
                                      self._sdk_authorization(),
                                      cardholder_request)

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

    def update_card(self, card_id: str, update_card_request: UpdateCardRequest):
        return self._api_client.patch(self.build_path(self.__ISSUING, self.__CARDS, card_id),
                                      self._sdk_authorization(),
                                      update_card_request)

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

    def renew_card(self, card_id: str, renew_card_request: RenewCardRequest):
        return self._api_client.post(self.build_path(self.__ISSUING, self.__CARDS, card_id, self.__RENEW),
                                     self._sdk_authorization(),
                                     renew_card_request)

    def revoke_card(self, card_id: str, revoke_request: RevokeRequest):
        return self._api_client.post(self.build_path(self.__ISSUING, self.__CARDS, card_id, self.__REVOKE),
                                     self._sdk_authorization(),
                                     revoke_request)

    def schedule_card_revocation(self, card_id: str, schedule_request: ScheduleCardRevocationRequest):
        return self._api_client.post(
            self.build_path(self.__ISSUING, self.__CARDS, card_id, self.__SCHEDULE_REVOCATION),
            self._sdk_authorization(),
            schedule_request)

    def delete_card_revocation(self, card_id: str):
        return self._api_client.delete(
            self.build_path(self.__ISSUING, self.__CARDS, card_id, self.__SCHEDULE_REVOCATION),
            self._sdk_authorization())

    def suspend_card(self, card_id: str, suspend_request: SuspendRequest):
        return self._api_client.post(self.build_path(self.__ISSUING, self.__CARDS, card_id, self.__SUSPEND),
                                     self._sdk_authorization(),
                                     suspend_request)

    def get_digital_card(self, digital_card_id: str):
        return self._api_client.get(self.build_path(self.__ISSUING, self.__DIGITAL_CARDS, digital_card_id),
                                    self._sdk_authorization())

    def get_list_transactions(self, query: TransactionsQueryFilter):
        return self._api_client.get(self.build_path(self.__ISSUING, self.__TRANSACTIONS),
                                    self._sdk_authorization(),
                                    query)

    def get_single_transaction(self, transaction_id: str):
        return self._api_client.get(self.build_path(self.__ISSUING, self.__TRANSACTIONS, transaction_id),
                                    self._sdk_authorization())

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

    def create_control_group(self, create_control_group_request: CreateControlGroupRequest):
        return self._api_client.post(self.build_path(self.__ISSUING, self.__CONTROLS, self.__CONTROL_GROUPS),
                                     self._sdk_authorization(),
                                     create_control_group_request)

    def get_target_control_groups(self, query: ControlGroupQueryTarget):
        return self._api_client.get(self.build_path(self.__ISSUING, self.__CONTROLS, self.__CONTROL_GROUPS),
                                    self._sdk_authorization(),
                                    query)

    def get_control_group_details(self, control_group_id: str):
        return self._api_client.get(
            self.build_path(self.__ISSUING, self.__CONTROLS, self.__CONTROL_GROUPS, control_group_id),
            self._sdk_authorization())

    def delete_control_group(self, control_group_id: str):
        return self._api_client.delete(
            self.build_path(self.__ISSUING, self.__CONTROLS, self.__CONTROL_GROUPS, control_group_id),
            self._sdk_authorization())

    def create_control_profile(self, control_profile_request: ControlProfileRequest):
        return self._api_client.post(self.build_path(self.__ISSUING, self.__CONTROLS, self.__CONTROL_PROFILES),
                                     self._sdk_authorization(),
                                     control_profile_request)

    def get_all_control_profiles(self, query: ControlGroupQueryTarget):
        return self._api_client.get(self.build_path(self.__ISSUING, self.__CONTROLS, self.__CONTROL_PROFILES),
                                    self._sdk_authorization(),
                                    query)

    def get_control_profile_details(self, control_profile_id: str):
        return self._api_client.get(
            self.build_path(self.__ISSUING, self.__CONTROLS, self.__CONTROL_PROFILES, control_profile_id),
            self._sdk_authorization())

    def update_control_profile(self, control_profile_id: str, control_profile_request: ControlProfileRequest):
        return self._api_client.patch(
            self.build_path(self.__ISSUING, self.__CONTROLS, self.__CONTROL_PROFILES, control_profile_id),
            self._sdk_authorization(),
            control_profile_request)

    def delete_control_profile(self, control_profile_id: str):
        return self._api_client.delete(
            self.build_path(self.__ISSUING, self.__CONTROLS, self.__CONTROL_PROFILES, control_profile_id),
            self._sdk_authorization())

    def add_target_to_control_profile(self, control_profile_id: str, target_id: str):
        return self._api_client.post(
            self.build_path(self.__ISSUING, self.__CONTROLS, self.__CONTROL_PROFILES, control_profile_id,
                            self.__ADD, target_id),
            self._sdk_authorization())

    def remove_target_from_control_profile(self, control_profile_id: str, target_id: str):
        return self._api_client.post(
            self.build_path(self.__ISSUING, self.__CONTROLS, self.__CONTROL_PROFILES, control_profile_id,
                            self.__REMOVE, target_id),
            self._sdk_authorization())

    def create_dispute(self, create_dispute_request: CreateDisputeRequest, idempotency_key: str = None):
        return self._api_client.post(self.build_path(self.__ISSUING, self.__DISPUTES),
                                     self._sdk_authorization(),
                                     create_dispute_request,
                                     idempotency_key)

    def get_dispute_details(self, dispute_id: str):
        return self._api_client.get(self.build_path(self.__ISSUING, self.__DISPUTES, dispute_id),
                                    self._sdk_authorization())

    def cancel_dispute(self, dispute_id: str, idempotency_key: str = None):
        return self._api_client.post(self.build_path(self.__ISSUING, self.__DISPUTES, dispute_id, self.__CANCEL),
                                     self._sdk_authorization(),
                                     None,
                                     idempotency_key)

    def escalate_dispute(self, dispute_id: str, escalate_dispute_request: EscalateDisputeRequest,
                         idempotency_key: str = None):
        return self._api_client.post(self.build_path(self.__ISSUING, self.__DISPUTES, dispute_id, self.__ESCALATE),
                                     self._sdk_authorization(),
                                     escalate_dispute_request,
                                     idempotency_key)

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

    def simulate_refund(self, transaction_id: str, refund_request: CardRefundAuthorizationRequest):
        return self._api_client.post(
            self.build_path(
                self.__ISSUING, self.__SIMULATE, self.__AUTHORIZATIONS, transaction_id, self.__REFUNDS),
            self._sdk_authorization(),
            refund_request)

    def simulate_oob_authentication(self, simulate_oob_request: SimulateOobAuthenticationRequest):
        return self._api_client.post(
            self.build_path(self.__ISSUING, self.__SIMULATE, self.__OOB, self.__AUTHENTICATION),
            self._sdk_authorization(),
            simulate_oob_request)
