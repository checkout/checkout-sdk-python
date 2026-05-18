import pytest

from tests._assertions import assert_api_call
from checkout_sdk.instruments.instruments_previous import CreateInstrumentRequest, UpdateInstrumentRequest
from checkout_sdk.instruments.instruments_client_previous import InstrumentsClient


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
        body = CreateInstrumentRequest()

        assert client.create(body) == 'response'
        assert_api_call(mock, 'instruments', body)

    def test_should_update_instrument(self, mocker, client: InstrumentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        body = UpdateInstrumentRequest()

        assert client.update('instrument_id', body) == 'response'
        assert_api_call(mock, 'instruments/instrument_id', body)

    def test_should_delete_instrument(self, mocker, client: InstrumentsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')

        assert client.delete('instrument_id') == 'response'
        assert_api_call(mock, 'instruments/instrument_id')
