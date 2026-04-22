import pytest

from checkout_sdk.identities.identityverification.identityverification import (
    IdentityVerificationRequest, IdentityVerificationAndAttemptRequest, IdentityVerificationAttemptRequest
)
from checkout_sdk.identities.identityverification.identityverification_client import IdentityVerificationClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return IdentityVerificationClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


# tests

class TestIdentityVerificationClient:

    def test_should_create_identity_verification_and_attempt(self, mocker, client: IdentityVerificationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_identity_verification_and_attempt(IdentityVerificationAndAttemptRequest()) == 'response'

    def test_should_create_identity_verification(self, mocker, client: IdentityVerificationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_identity_verification(IdentityVerificationRequest()) == 'response'

    def test_should_get_identity_verification(self, mocker, client: IdentityVerificationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_identity_verification('idv_12345') == 'response'

    def test_should_anonymize_identity_verification(self, mocker, client: IdentityVerificationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.anonymize_identity_verification('idv_12345') == 'response'

    def test_should_create_identity_verification_attempt(self, mocker, client: IdentityVerificationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_identity_verification_attempt('idv_12345',
                                                           IdentityVerificationAttemptRequest()) == 'response'

    def test_should_get_identity_verification_attempts(self, mocker, client: IdentityVerificationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_identity_verification_attempts('idv_12345') == 'response'

    def test_should_get_identity_verification_attempt(self, mocker, client: IdentityVerificationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_identity_verification_attempt('idv_12345', 'attempt_67890') == 'response'

    def test_should_get_identity_verification_report(self, mocker, client: IdentityVerificationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_identity_verification_report('idv_12345') == 'response'
