import pytest

from tests._assertions import assert_api_call
from checkout_sdk.transfers.transfers import CreateTransferRequest
from checkout_sdk.transfers.transfers_client import TransfersClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return TransfersClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestTransfersClient:

    def test_should_initiate_transfer_of_funds(self, mocker, client: TransfersClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = CreateTransferRequest()

        assert client.initiate_transfer_of_funds(body, 'idempotency_key') == 'response'
        assert_api_call(mock, 'transfers', body)

    def test_should_retrieve_a_transfer(self, mocker, client: TransfersClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.retrieve_a_transfer('transfer_id') == 'response'
        assert_api_call(mock, 'transfers/transfer_id')
