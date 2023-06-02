import pytest

from checkout_sdk.issuing.cardholders import CardholderRequest
from checkout_sdk.issuing.cards import PhysicalCardRequest, PasswordEnrollmentRequest, UpdateThreeDsEnrollmentRequest, \
    CardCredentialsQuery, RevokeRequest, SuspendRequest
from checkout_sdk.issuing.controls import MccControlRequest, CardControlsQuery, UpdateCardControlRequest
from checkout_sdk.issuing.issuing_client import IssuingClient
from checkout_sdk.issuing.testing import CardAuthorizationRequest


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

    def test_should_get_cardholder_cards(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_cardholder_cards('cardholder_id') == 'response'

    def test_should_create_card(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_card(PhysicalCardRequest()) == 'response'

    def test_should_get_card_details(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_card_details('card_id') == 'response'

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

    def test_should_revoke_card(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.revoke_card('card_id', RevokeRequest()) == 'response'

    def test_should_suspend_card(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.suspend_card('card_id', SuspendRequest()) == 'response'

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

    def test_should_simulate_authorization(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.simulate_authorization(CardAuthorizationRequest()) == 'response'
