import pytest

from tests._assertions import assert_api_call
from checkout_sdk.common.common import Phone
from checkout_sdk.common.enums import Country, Currency
from checkout_sdk.instruments.instruments import CreateTokenInstrumentRequest, CreateCardInstrumentRequest, \
    CreateCustomerInstrumentRequest, UpdateCardInstrumentRequest, BankAccountFieldQuery
from checkout_sdk.instruments.instruments_client import InstrumentsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return InstrumentsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestInstrumentsClient:

    def test_should_get_instrument(self, mocker, client: InstrumentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get('instrument_id') == 'response'
        assert_api_call(mock, 'instruments/instrument_id')

    def test_should_create_instrument(self, mocker, client: InstrumentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = CreateTokenInstrumentRequest()

        assert client.create(body) == 'response'
        assert_api_call(mock, 'instruments', body)

    def test_should_create_card_instrument_with_customer(self, mocker, client: InstrumentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        customer = CreateCustomerInstrumentRequest()
        customer.email = 'test@example.com'
        customer.name = 'Test User'
        customer.default = True
        body = CreateCardInstrumentRequest()
        body.number = '4242424242424242'
        body.expiry_month = 6
        body.expiry_year = 2025
        body.customer = customer

        assert client.create(body) == 'response'
        assert_api_call(mock, 'instruments', body)

    def test_should_update_instrument(self, mocker, client: InstrumentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        body = UpdateCardInstrumentRequest()

        assert client.update('instrument_id', body) == 'response'
        assert_api_call(mock, 'instruments/instrument_id', body)

    def test_should_delete_instrument(self, mocker, client: InstrumentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')

        assert client.delete('instrument_id') == 'response'
        assert_api_call(mock, 'instruments/instrument_id')

    def test_should_revoke_instrument(self, mocker, client: InstrumentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')

        assert client.revoke('instrument_id') == 'response'
        assert_api_call(mock, 'instruments/instrument_id/revoke')

    def test_should_get_bank_account_field_formatting(self, mocker, client: InstrumentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        query = BankAccountFieldQuery()

        assert client.get_bank_account_field_formatting(Country.GB, Currency.GBP, query) == 'response'
        # Country / Currency are enums; their .value is what build_path concatenates.
        assert_api_call(mock, 'validation/bank-accounts/GB/GBP', query)
