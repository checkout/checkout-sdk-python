import pytest

from checkout_sdk.payments.googlepay.googlepay import GooglePayEnrollmentRequest, GooglePayRegisterDomainRequest
from checkout_sdk.payments.googlepay.googlepay_client import GooglePayClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return GooglePayClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


# tests

class TestGooglePayClient:

    def test_should_create_enrollment(self, mocker, client: GooglePayClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_enrollment(GooglePayEnrollmentRequest()) == 'response'

    def test_should_register_domain(self, mocker, client: GooglePayClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.register_domain('ent_uzm3uxtssvmuxnyrfdffcyjxeu', GooglePayRegisterDomainRequest()) == 'response'

    def test_should_get_registered_domains(self, mocker, client: GooglePayClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_registered_domains('ent_uzm3uxtssvmuxnyrfdffcyjxeu') == 'response'

    def test_should_get_enrollment_state(self, mocker, client: GooglePayClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_enrollment_state('ent_uzm3uxtssvmuxnyrfdffcyjxeu') == 'response'
