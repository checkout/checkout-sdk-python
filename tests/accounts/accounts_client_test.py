import pytest

from tests._assertions import assert_api_call
from checkout_sdk.accounts.accounts import OnboardEntityRequest, AccountsPaymentInstrument, UpdateScheduleRequest, \
    PaymentInstrumentRequest, PaymentInstrumentsQuery, UpdatePaymentInstrumentRequest, ReserveRuleRequest, \
    EntityFileRequest, FilePurpose, EntityRequirementUpdateRequest
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
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = OnboardEntityRequest()

        assert client.create_entity(body) == 'response'
        assert_api_call(mock, 'accounts/entities', body)

    def test_should_get_entity(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_entity('entity_id') == 'response'
        assert_api_call(mock, 'accounts/entities/entity_id')

    def test_should_update_entity(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        body = OnboardEntityRequest()

        assert client.update_entity('entity_id', body) == 'response'
        assert_api_call(mock, 'accounts/entities/entity_id', body)

    def test_should_create_payment_instrument_deprecated(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = AccountsPaymentInstrument()

        assert client.create_payment_instrument('entity_id', body) == 'response'
        assert_api_call(mock, 'accounts/entities/entity_id/instruments', body)

    def test_should_create_payment_instrument(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = PaymentInstrumentRequest()

        assert client.add_payment_instrument('entity_id', body) == 'response'
        assert_api_call(mock, 'accounts/entities/entity_id/payment-instruments', body)

    def test_should_update_payment_instrument(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        body = UpdatePaymentInstrumentRequest()

        assert client.update_payment_instrument('entity_id', 'instrument_id', body) == 'response'
        assert_api_call(mock, 'accounts/entities/entity_id/payment-instruments/instrument_id', body)

    def test_should_query_payment_instruments(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        body = PaymentInstrumentsQuery()

        assert client.query_payment_instruments('entity_id', body) == 'response'
        assert_api_call(mock, 'accounts/entities/entity_id/payment-instruments', body)

    def test_should_retrieve_payment_instrument_details(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.retrieve_payment_instrument_details('entity_id', 'payment_instrument_id') == 'response'
        assert_api_call(mock, 'accounts/entities/entity_id/payment-instruments/payment_instrument_id')

    def test_should_upload_file(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.submit_file', return_value='response')
        body = FileRequest()

        assert client.upload_file(body) == 'response'
        mock.assert_called_once()
        args = mock.call_args.args
        assert args[0] == 'files'
        assert args[2] is body

    def test_should_update_payout_schedule(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        body = UpdateScheduleRequest()

        assert client.update_payout_schedule('entity_id', Currency.USD, body) == 'response'
        mock.assert_called_once()
        args = mock.call_args.args
        assert args[0] == 'accounts/entities/entity_id/payout-schedules'
        assert args[2] == {Currency.USD: body}

    def test_should_retrieve_payout_schedule(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.retrieve_payout_schedule('entity_id') == 'response'
        assert_api_call(mock, 'accounts/entities/entity_id/payout-schedules')

    def test_should_get_sub_entity_members(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_sub_entity_members('entity_id') == 'response'
        assert_api_call(mock, 'accounts/entities/entity_id/members')

    def test_should_reinvite_sub_entity_member(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')

        assert client.reinvite_sub_entity_member('entity_id', 'user_id') == 'response'
        assert_api_call(mock, 'accounts/entities/entity_id/members/user_id')

    def test_should_create_reserve_rule(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = ReserveRuleRequest()

        assert client.create_reserve_rule('entity_id', body) == 'response'
        assert_api_call(mock, 'accounts/entities/entity_id/reserve-rules', body)

    def test_should_get_reserve_rules(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_reserve_rules('entity_id') == 'response'
        assert_api_call(mock, 'accounts/entities/entity_id/reserve-rules')

    def test_should_get_reserve_rule_details(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_reserve_rule_details('entity_id', 'reserve_rule_id') == 'response'
        assert_api_call(mock, 'accounts/entities/entity_id/reserve-rules/reserve_rule_id')

    def test_should_update_reserve_rule(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        body = ReserveRuleRequest()

        assert client.update_reserve_rule('entity_id', 'reserve_rule_id', 'etag_value', body) == 'response'
        assert_api_call(mock, 'accounts/entities/entity_id/reserve-rules/reserve_rule_id', body)

    def test_should_upload_entity_file(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = EntityFileRequest()
        body.purpose = FilePurpose.IDENTIFICATION

        assert client.upload_entity_file('entity_id', body) == 'response'
        assert_api_call(mock, 'entities/entity_id/files', body)

    def test_should_retrieve_entity_file(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.retrieve_entity_file('entity_id', 'file_id') == 'response'
        assert_api_call(mock, 'entities/entity_id/files/file_id')

    def test_should_get_entity_requirements(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_entity_requirements('entity_id') == 'response'
        assert_api_call(mock, 'accounts/entities/entity_id/requirements')

    def test_should_get_entity_requirement_details(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_entity_requirement_details('entity_id', 'requirement_id') == 'response'
        assert_api_call(mock, 'accounts/entities/entity_id/requirements/requirement_id')

    def test_should_resolve_entity_requirement(self, mocker, client: AccountsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        body = EntityRequirementUpdateRequest()

        assert client.resolve_entity_requirement('entity_id', 'requirement_id', body) == 'response'
        assert_api_call(mock, 'accounts/entities/entity_id/requirements/requirement_id', body)
