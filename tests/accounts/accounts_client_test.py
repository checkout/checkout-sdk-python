import pytest

from checkout_sdk.accounts.accounts import OnboardEntityRequest, AccountsPaymentInstrument, UpdateScheduleRequest, \
    PaymentInstrumentRequest, PaymentInstrumentsQuery
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
