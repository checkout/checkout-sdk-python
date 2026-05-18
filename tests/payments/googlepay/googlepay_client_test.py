import pytest

from tests._assertions import assert_api_call
from checkout_sdk.payments.googlepay.googlepay import GooglePayEnrollmentRequest, GooglePayRegisterDomainRequest
from checkout_sdk.payments.googlepay.googlepay_client import GooglePayClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return GooglePayClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


_ENTITY_ID = 'ent_uzm3uxtssvmuxnyrfdffcyjxeu'


class TestGooglePayClient:

    def test_should_create_enrollment(self, mocker, client: GooglePayClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = GooglePayEnrollmentRequest()

        assert client.create_enrollment(body) == 'response'
        assert_api_call(mock, 'googlepay/enrollments', body)

    def test_should_register_domain(self, mocker, client: GooglePayClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = GooglePayRegisterDomainRequest()

        assert client.register_domain(_ENTITY_ID, body) == 'response'
        assert_api_call(mock, f'googlepay/enrollments/{_ENTITY_ID}/domain', body)

    def test_should_get_registered_domains(self, mocker, client: GooglePayClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_registered_domains(_ENTITY_ID) == 'response'
        assert_api_call(mock, f'googlepay/enrollments/{_ENTITY_ID}/domains')

    def test_should_get_enrollment_state(self, mocker, client: GooglePayClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_enrollment_state(_ENTITY_ID) == 'response'
        assert_api_call(mock, f'googlepay/enrollments/{_ENTITY_ID}/state')
