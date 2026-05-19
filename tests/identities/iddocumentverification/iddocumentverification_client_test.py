import pytest

from tests._assertions import assert_api_call
from checkout_sdk.identities.iddocumentverification.iddocumentverification import (
    IdDocumentVerificationRequest, IdDocumentVerificationAttemptRequest
)
from checkout_sdk.identities.iddocumentverification.iddocumentverification_client import IdDocumentVerificationClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return IdDocumentVerificationClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestIdDocumentVerificationClient:

    def test_should_create_id_document_verification(self, mocker, client: IdDocumentVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = IdDocumentVerificationRequest()

        assert client.create_id_document_verification(body) == 'response'
        assert_api_call(mock, 'id-document-verifications', body)

    def test_should_get_id_document_verification(self, mocker, client: IdDocumentVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_id_document_verification('iddoc_12345') == 'response'
        assert_api_call(mock, 'id-document-verifications/iddoc_12345')

    def test_should_anonymize_id_document_verification(self, mocker, client: IdDocumentVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.anonymize_id_document_verification('iddoc_12345') == 'response'
        assert_api_call(mock, 'id-document-verifications/iddoc_12345/anonymize')

    def test_should_create_id_document_verification_attempt(self, mocker, client: IdDocumentVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = IdDocumentVerificationAttemptRequest()

        assert client.create_id_document_verification_attempt('iddoc_12345', body) == 'response'
        assert_api_call(mock, 'id-document-verifications/iddoc_12345/attempts', body)

    def test_should_get_id_document_verification_attempts(self, mocker, client: IdDocumentVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_id_document_verification_attempts('iddoc_12345') == 'response'
        assert_api_call(mock, 'id-document-verifications/iddoc_12345/attempts')

    def test_should_get_id_document_verification_attempt(self, mocker, client: IdDocumentVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_id_document_verification_attempt('iddoc_12345', 'attempt_67890') == 'response'
        assert_api_call(mock, 'id-document-verifications/iddoc_12345/attempts/attempt_67890')

    def test_should_get_id_document_verification_report(self, mocker, client: IdDocumentVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_id_document_verification_report('iddoc_12345') == 'response'
        assert_api_call(mock, 'id-document-verifications/iddoc_12345/pdf-report')
