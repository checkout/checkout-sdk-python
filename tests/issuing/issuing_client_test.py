import pytest

from tests._assertions import assert_api_call
from checkout_sdk.issuing.cardholders import CardholderRequest
from checkout_sdk.issuing.cards import PhysicalCardRequest, PasswordEnrollmentRequest, UpdateThreeDsEnrollmentRequest, \
    CardCredentialsQuery, RevokeRequest, SuspendRequest, UpdateCardRequest, VirtualCardRenewRequest, \
    ScheduleCardRevocationRequest
from checkout_sdk.issuing.controls import MccControlRequest, CardControlsQuery, UpdateCardControlRequest, \
    CreateControlGroupRequest, ControlGroupQueryTarget, ControlProfileRequest
from checkout_sdk.issuing.disputes import CreateDisputeRequest, EscalateDisputeRequest
from checkout_sdk.issuing.issuing_client import IssuingClient
from checkout_sdk.issuing.testing import CardAuthorizationRequest, SimulationRequest, \
    CardRefundAuthorizationRequest, SimulateOobAuthenticationRequest
from checkout_sdk.issuing.transactions import TransactionsQueryFilter


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return IssuingClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestIssuingClient:

    def test_should_create_cardholder(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = CardholderRequest()

        assert client.create_cardholder(body) == 'response'
        assert_api_call(mock, 'issuing/cardholders', body)

    def test_should_get_cardholder(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_cardholder('cardholder_id') == 'response'
        assert_api_call(mock, 'issuing/cardholders/cardholder_id')

    def test_should_update_cardholder(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        body = CardholderRequest()

        assert client.update_cardholder('cardholder_id', body) == 'response'
        assert_api_call(mock, 'issuing/cardholders/cardholder_id', body)

    def test_should_get_cardholder_cards(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_cardholder_cards('cardholder_id') == 'response'
        assert_api_call(mock, 'issuing/cardholders/cardholder_id/cards')

    def test_should_create_card(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = PhysicalCardRequest()

        assert client.create_card(body) == 'response'
        assert_api_call(mock, 'issuing/cards', body)

    def test_should_get_card_details(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_card_details('card_id') == 'response'
        assert_api_call(mock, 'issuing/cards/card_id')

    def test_should_update_card(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        body = UpdateCardRequest()

        assert client.update_card('card_id', body) == 'response'
        assert_api_call(mock, 'issuing/cards/card_id', body)

    def test_should_enroll_three_ds(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = PasswordEnrollmentRequest()

        assert client.enroll_three_ds('card_id', body) == 'response'
        assert_api_call(mock, 'issuing/cards/card_id/3ds-enrollment', body)

    def test_should_update_three_ds_enrollment(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        body = UpdateThreeDsEnrollmentRequest()

        assert client.update_three_ds_enrollment('card_id', body) == 'response'
        assert_api_call(mock, 'issuing/cards/card_id/3ds-enrollment', body)

    def test_should_get_three_ds_details(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_three_ds_details('card_id') == 'response'
        assert_api_call(mock, 'issuing/cards/card_id/3ds-enrollment')

    def test_should_activate_card(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.activate_card('card_id') == 'response'
        assert_api_call(mock, 'issuing/cards/card_id/activate')

    def test_should_get_card_credentials(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        query = CardCredentialsQuery()

        assert client.get_card_credentials('card_id', query) == 'response'
        # query is passed as the `params` positional arg of ApiClient.get
        # (path, authorization, params) — same position the helper checks as body.
        assert_api_call(mock, 'issuing/cards/card_id/credentials', query)

    def test_should_renew_card(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = VirtualCardRenewRequest()

        assert client.renew_card('card_id', body) == 'response'
        assert_api_call(mock, 'issuing/cards/card_id/renew', body)

    def test_should_revoke_card(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = RevokeRequest()

        assert client.revoke_card('card_id', body) == 'response'
        assert_api_call(mock, 'issuing/cards/card_id/revoke', body)

    def test_should_schedule_card_revocation(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = ScheduleCardRevocationRequest()

        assert client.schedule_card_revocation('card_id', body) == 'response'
        assert_api_call(mock, 'issuing/cards/card_id/schedule-revocation', body)

    def test_should_delete_card_revocation(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')

        assert client.delete_card_revocation('card_id') == 'response'
        assert_api_call(mock, 'issuing/cards/card_id/schedule-revocation')

    def test_should_suspend_card(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = SuspendRequest()

        assert client.suspend_card('card_id', body) == 'response'
        assert_api_call(mock, 'issuing/cards/card_id/suspend', body)

    def test_should_get_digital_card(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_digital_card('digital_card_id') == 'response'
        assert_api_call(mock, 'issuing/digital-cards/digital_card_id')

    def test_should_get_list_transactions(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        query = TransactionsQueryFilter()

        assert client.get_list_transactions(query) == 'response'
        assert_api_call(mock, 'issuing/transactions', query)

    def test_should_get_single_transaction(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_single_transaction('transaction_id') == 'response'
        assert_api_call(mock, 'issuing/transactions/transaction_id')

    def test_should_create_control(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = MccControlRequest()

        assert client.create_control(body) == 'response'
        assert_api_call(mock, 'issuing/controls', body)

    def test_should_get_card_controls(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        query = CardControlsQuery()

        assert client.get_card_controls(query) == 'response'
        assert_api_call(mock, 'issuing/controls', query)

    def test_should_get_card_control_details(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_card_control_details('control_id') == 'response'
        assert_api_call(mock, 'issuing/controls/control_id')

    def test_should_update_card_control(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        body = UpdateCardControlRequest()

        assert client.update_card_control('control_id', body) == 'response'
        assert_api_call(mock, 'issuing/controls/control_id', body)

    def test_should_remove_control(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')

        assert client.remove_control('control_id') == 'response'
        assert_api_call(mock, 'issuing/controls/control_id')

    def test_should_create_control_group(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = CreateControlGroupRequest()

        assert client.create_control_group(body) == 'response'
        assert_api_call(mock, 'issuing/controls/control-groups', body)

    def test_should_get_target_control_groups(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        query = ControlGroupQueryTarget()

        assert client.get_target_control_groups(query) == 'response'
        assert_api_call(mock, 'issuing/controls/control-groups', query)

    def test_should_get_control_group_details(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_control_group_details('control_group_id') == 'response'
        assert_api_call(mock, 'issuing/controls/control-groups/control_group_id')

    def test_should_delete_control_group(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')

        assert client.delete_control_group('control_group_id') == 'response'
        assert_api_call(mock, 'issuing/controls/control-groups/control_group_id')

    def test_should_create_control_profile(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = ControlProfileRequest()

        assert client.create_control_profile(body) == 'response'
        assert_api_call(mock, 'issuing/controls/control-profiles', body)

    def test_should_get_all_control_profiles(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        query = ControlGroupQueryTarget()

        assert client.get_all_control_profiles(query) == 'response'
        assert_api_call(mock, 'issuing/controls/control-profiles', query)

    def test_should_get_control_profile_details(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_control_profile_details('control_profile_id') == 'response'
        assert_api_call(mock, 'issuing/controls/control-profiles/control_profile_id')

    def test_should_update_control_profile(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        body = ControlProfileRequest()

        assert client.update_control_profile('control_profile_id', body) == 'response'
        assert_api_call(mock, 'issuing/controls/control-profiles/control_profile_id', body)

    def test_should_delete_control_profile(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')

        assert client.delete_control_profile('control_profile_id') == 'response'
        assert_api_call(mock, 'issuing/controls/control-profiles/control_profile_id')

    def test_should_add_target_to_control_profile(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.add_target_to_control_profile('control_profile_id', 'target_id') == 'response'
        assert_api_call(mock, 'issuing/controls/control-profiles/control_profile_id/add/target_id')

    def test_should_remove_target_from_control_profile(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.remove_target_from_control_profile('control_profile_id', 'target_id') == 'response'
        assert_api_call(mock, 'issuing/controls/control-profiles/control_profile_id/remove/target_id')

    def test_should_create_dispute(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = CreateDisputeRequest()

        assert client.create_dispute(body) == 'response'
        assert_api_call(mock, 'issuing/disputes', body)

    def test_should_get_dispute_details(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_dispute_details('dispute_id') == 'response'
        assert_api_call(mock, 'issuing/disputes/dispute_id')

    def test_should_cancel_dispute(self, mocker, client: IssuingClient):
        # cancel_dispute passes body=None explicitly to ApiClient.post for the
        # idempotency-key 4th-arg signature, so we don't assert a body.
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.cancel_dispute('dispute_id') == 'response'
        assert_api_call(mock, 'issuing/disputes/dispute_id/cancel')

    def test_should_escalate_dispute(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = EscalateDisputeRequest()

        assert client.escalate_dispute('dispute_id', body) == 'response'
        assert_api_call(mock, 'issuing/disputes/dispute_id/escalate', body)

    def test_should_simulate_authorization(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = CardAuthorizationRequest()

        assert client.simulate_authorization(body) == 'response'
        assert_api_call(mock, 'issuing/simulate/authorizations', body)

    def test_should_simulate_increment(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = SimulationRequest()

        assert client.simulate_increment('transaction_id', body) == 'response'
        assert_api_call(mock, 'issuing/simulate/authorizations/transaction_id/authorizations', body)

    def test_should_simulate_clearing(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = SimulationRequest()

        assert client.simulate_clearing('transaction_id', body) == 'response'
        assert_api_call(mock, 'issuing/simulate/authorizations/transaction_id/presentments', body)

    def test_should_simulate_reversal(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = SimulationRequest()

        assert client.simulate_reversal('transaction_id', body) == 'response'
        assert_api_call(mock, 'issuing/simulate/authorizations/transaction_id/reversals', body)

    def test_should_simulate_refund(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = CardRefundAuthorizationRequest()

        assert client.simulate_refund('transaction_id', body) == 'response'
        assert_api_call(mock, 'issuing/simulate/authorizations/transaction_id/refunds', body)

    def test_should_simulate_oob_authentication(self, mocker, client: IssuingClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = SimulateOobAuthenticationRequest()

        assert client.simulate_oob_authentication(body) == 'response'
        assert_api_call(mock, 'issuing/simulate/oob/authentication', body)
