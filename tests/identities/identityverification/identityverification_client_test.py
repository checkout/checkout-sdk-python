import pytest

from tests._assertions import assert_api_call
from checkout_sdk.identities.identityverification.identityverification import (
    IdentityVerificationRequest, IdentityVerificationAndAttemptRequest, IdentityVerificationAttemptRequest
)
from checkout_sdk.identities.identityverification.identityverification_client import IdentityVerificationClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return IdentityVerificationClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestIdentityVerificationClient:

    def test_should_create_identity_verification_and_attempt(self, mocker, client: IdentityVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = IdentityVerificationAndAttemptRequest()

        assert client.create_identity_verification_and_attempt(body) == 'response'
        assert_api_call(mock, 'create-and-open-idv', body)

    def test_should_create_identity_verification(self, mocker, client: IdentityVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = IdentityVerificationRequest()

        assert client.create_identity_verification(body) == 'response'
        assert_api_call(mock, 'identity-verifications', body)

    def test_should_get_identity_verification(self, mocker, client: IdentityVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_identity_verification('idv_12345') == 'response'
        assert_api_call(mock, 'identity-verifications/idv_12345')

    def test_should_anonymize_identity_verification(self, mocker, client: IdentityVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.anonymize_identity_verification('idv_12345') == 'response'
        assert_api_call(mock, 'identity-verifications/idv_12345/anonymize')

    def test_should_create_identity_verification_attempt(self, mocker, client: IdentityVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = IdentityVerificationAttemptRequest()

        assert client.create_identity_verification_attempt('idv_12345', body) == 'response'
        assert_api_call(mock, 'identity-verifications/idv_12345/attempts', body)

    def test_should_get_identity_verification_attempts(self, mocker, client: IdentityVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_identity_verification_attempts('idv_12345') == 'response'
        assert_api_call(mock, 'identity-verifications/idv_12345/attempts')

    def test_should_get_identity_verification_attempt(self, mocker, client: IdentityVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_identity_verification_attempt('idv_12345', 'attempt_67890') == 'response'
        assert_api_call(mock, 'identity-verifications/idv_12345/attempts/attempt_67890')

    def test_should_get_identity_verification_report(self, mocker, client: IdentityVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_identity_verification_report('idv_12345') == 'response'
        assert_api_call(mock, 'identity-verifications/idv_12345/pdf-report')
