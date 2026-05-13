import pytest

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
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_cardholder(CardholderRequest()) == 'response'

    def test_should_get_cardholder(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_cardholder('cardholder_id') == 'response'

    def test_should_update_cardholder(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        assert client.update_cardholder('cardholder_id', CardholderRequest()) == 'response'

    def test_should_get_cardholder_cards(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_cardholder_cards('cardholder_id') == 'response'

    def test_should_create_card(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_card(PhysicalCardRequest()) == 'response'

    def test_should_get_card_details(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_card_details('card_id') == 'response'

    def test_should_update_card(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        assert client.update_card('card_id', UpdateCardRequest()) == 'response'

    def test_should_enroll_three_ds(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.enroll_three_ds('card_id', PasswordEnrollmentRequest()) == 'response'

    def test_should_update_three_ds_enrollment(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        assert client.update_three_ds_enrollment('card_id', UpdateThreeDsEnrollmentRequest()) == 'response'

    def test_should_get_three_ds_details(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_three_ds_details('card_id') == 'response'

    def test_should_activate_card(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.activate_card('card_id') == 'response'

    def test_should_get_card_credentials(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_card_credentials('card_id', CardCredentialsQuery()) == 'response'

    def test_should_renew_card(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.renew_card('card_id', VirtualCardRenewRequest()) == 'response'

    def test_should_revoke_card(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.revoke_card('card_id', RevokeRequest()) == 'response'

    def test_should_schedule_card_revocation(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.schedule_card_revocation('card_id', ScheduleCardRevocationRequest()) == 'response'

    def test_should_delete_card_revocation(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')
        assert client.delete_card_revocation('card_id') == 'response'

    def test_should_suspend_card(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.suspend_card('card_id', SuspendRequest()) == 'response'

    def test_should_get_digital_card(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_digital_card('digital_card_id') == 'response'

    def test_should_get_list_transactions(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_list_transactions(TransactionsQueryFilter()) == 'response'

    def test_should_get_single_transaction(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_single_transaction('transaction_id') == 'response'

    def test_should_create_control(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_control(MccControlRequest()) == 'response'

    def test_should_get_card_controls(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_card_controls(CardControlsQuery()) == 'response'

    def test_should_get_card_control_details(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_card_control_details('control_id') == 'response'

    def test_should_update_card_control(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        assert client.update_card_control('control_id', UpdateCardControlRequest()) == 'response'

    def test_should_remove_control(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')
        assert client.remove_control('control_id') == 'response'

    def test_should_create_control_group(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_control_group(CreateControlGroupRequest()) == 'response'

    def test_should_get_target_control_groups(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_target_control_groups(ControlGroupQueryTarget()) == 'response'

    def test_should_get_control_group_details(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_control_group_details('control_group_id') == 'response'

    def test_should_delete_control_group(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')
        assert client.delete_control_group('control_group_id') == 'response'

    def test_should_create_control_profile(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_control_profile(ControlProfileRequest()) == 'response'

    def test_should_get_all_control_profiles(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_all_control_profiles(ControlGroupQueryTarget()) == 'response'

    def test_should_get_control_profile_details(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_control_profile_details('control_profile_id') == 'response'

    def test_should_update_control_profile(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        assert client.update_control_profile('control_profile_id', ControlProfileRequest()) == 'response'

    def test_should_delete_control_profile(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')
        assert client.delete_control_profile('control_profile_id') == 'response'

    def test_should_add_target_to_control_profile(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.add_target_to_control_profile('control_profile_id', 'target_id') == 'response'

    def test_should_remove_target_from_control_profile(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.remove_target_from_control_profile('control_profile_id', 'target_id') == 'response'

    def test_should_create_dispute(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_dispute(CreateDisputeRequest()) == 'response'

    def test_should_get_dispute_details(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_dispute_details('dispute_id') == 'response'

    def test_should_cancel_dispute(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.cancel_dispute('dispute_id') == 'response'

    def test_should_escalate_dispute(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.escalate_dispute('dispute_id', EscalateDisputeRequest()) == 'response'

    def test_should_simulate_authorization(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.simulate_authorization(CardAuthorizationRequest()) == 'response'

    def test_should_simulate_increment(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.simulate_increment('transaction_id', SimulationRequest()) == 'response'

    def test_should_simulate_clearing(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.simulate_clearing('transaction_id', SimulationRequest()) == 'response'

    def test_should_simulate_reversal(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.simulate_reversal('transaction_id', SimulationRequest()) == 'response'

    def test_should_simulate_refund(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.simulate_refund('transaction_id', CardRefundAuthorizationRequest()) == 'response'

    def test_should_simulate_oob_authentication(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.simulate_oob_authentication(SimulateOobAuthenticationRequest()) == 'response'
