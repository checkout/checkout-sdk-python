import pytest

from checkout_sdk.accounts.accounts import OnboardEntityRequest, AccountsPaymentInstrument, UpdateScheduleRequest, \
    PaymentInstrumentRequest, PaymentInstrumentsQuery, UpdatePaymentInstrumentRequest, ReserveRuleRequest, \
    EntityFileRequest, FilePurpose
from checkout_sdk.accounts.accounts_client import AccountsClient
from checkout_sdk.common.enums import Currency
from checkout_sdk.files.files import FileRequest


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return AccountsClient(api_client=mock_api_client,
                          files_client=mock_api_client,
                          configuration=mock_sdk_configuration)


class TestAccountsClient:

    def test_should_create_entity(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_entity(OnboardEntityRequest()) == 'response'

    def test_should_get_entity(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_entity('entity_id') == 'response'

    def test_should_update_entity(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        assert client.update_entity('entity_id', OnboardEntityRequest()) == 'response'

    def test_should_create_payment_instrument_deprecated(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_payment_instrument('entity_id', AccountsPaymentInstrument()) == 'response'

    def test_should_create_payment_instrument(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.add_payment_instrument('entity_id', PaymentInstrumentRequest()) == 'response'

    def test_should_update_payment_instrument(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        assert client.update_payment_instrument('entity_id', 'instrument_id',
                                                UpdatePaymentInstrumentRequest()) == 'response'

    def test_should_query_payment_instruments(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.query_payment_instruments('entity_id', PaymentInstrumentsQuery()) == 'response'

    def test_should_retrieve_payment_instrument_details(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.retrieve_payment_instrument_details('entity_id', 'payment_instrument_id') == 'response'

    def test_should_upload_file(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.submit_file', return_value='response')
        assert client.upload_file(FileRequest()) == 'response'

    def test_should_update_payout_schedule(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        assert client.update_payout_schedule('entity_id', Currency.USD, UpdateScheduleRequest()) == 'response'

    def test_should_retrieve_payout_schedule(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.retrieve_payout_schedule('entity_id') == 'response'

    def test_should_get_sub_entity_members(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_sub_entity_members('entity_id') == 'response'

    def test_should_reinvite_sub_entity_member(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        assert client.reinvite_sub_entity_member('entity_id', 'user_id') == 'response'

    def test_should_create_reserve_rule(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_reserve_rule('entity_id', ReserveRuleRequest()) == 'response'

    def test_should_get_reserve_rules(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_reserve_rules('entity_id') == 'response'

    def test_should_get_reserve_rule_details(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_reserve_rule_details('entity_id', 'reserve_rule_id') == 'response'

    def test_should_update_reserve_rule(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        assert client.update_reserve_rule('entity_id', 'reserve_rule_id', 'etag_value', ReserveRuleRequest()) == 'response'

    def test_should_upload_entity_file(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        request = EntityFileRequest()
        request.purpose = FilePurpose.IDENTIFICATION
        assert client.upload_entity_file('entity_id', request) == 'response'

    def test_should_retrieve_entity_file(self, mocker, client: AccountsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.retrieve_entity_file('entity_id', 'file_id') == 'response'
