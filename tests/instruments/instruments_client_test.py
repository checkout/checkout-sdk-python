import pytest

from checkout_sdk.common.enums import Country, Currency
from checkout_sdk.instruments.instruments import CreateTokenInstrumentRequest, UpdateCardInstrumentRequest, \
    BankAccountFieldQuery
from checkout_sdk.instruments.instruments_client import InstrumentsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return InstrumentsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestInstrumentsClient:

    def test_should_get_instrument(self, mocker, client: InstrumentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get('instrument_id') == 'response'

    def test_should_create_instrument(self, mocker, client: InstrumentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create(CreateTokenInstrumentRequest()) == 'response'

    def test_should_update_instrument(self, mocker, client: InstrumentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        assert client.update('instrument_id', UpdateCardInstrumentRequest()) == 'response'

    def test_should_delete_instrument(self, mocker, client: InstrumentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')
        assert client.delete('instrument_id') == 'response'

    def test_should_get_bank_account_field_formatting(self, mocker, client: InstrumentsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_bank_account_field_formatting(Country.GB, Currency.GBP, BankAccountFieldQuery()) == 'response'
