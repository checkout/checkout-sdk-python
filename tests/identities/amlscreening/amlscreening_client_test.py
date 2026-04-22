import pytest

from checkout_sdk.identities.amlscreening.amlscreening import AmlScreeningRequest
from checkout_sdk.identities.amlscreening.amlscreening_client import AmlScreeningClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return AmlScreeningClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestAmlScreeningClient:

    def test_should_create_aml_screening(self, mocker, client: AmlScreeningClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_aml_screening(AmlScreeningRequest()) == 'response'

    def test_should_get_aml_screening(self, mocker, client: AmlScreeningClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_aml_screening('scr_7hr7swleu6guzjqesyxmyodnya') == 'response'
