import pytest

from tests._assertions import assert_api_call
from checkout_sdk.identities.addressdocumentverification.addressdocumentverification import (
    AddressDocumentVerificationRequest, AddressDocumentVerificationAttemptRequest
)
from checkout_sdk.identities.addressdocumentverification.addressdocumentverification_client import \
    AddressDocumentVerificationClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return AddressDocumentVerificationClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestAddressDocumentVerificationClient:

    def test_should_create_address_document_verification(self, mocker, client: AddressDocumentVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = AddressDocumentVerificationRequest()

        assert client.create_address_document_verification(body) == 'response'
        assert_api_call(mock, 'address-document-verifications', body)

    def test_should_get_address_document_verification(self, mocker, client: AddressDocumentVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_address_document_verification('adv_12345') == 'response'
        assert_api_call(mock, 'address-document-verifications/adv_12345')

    def test_should_anonymize_address_document_verification(self, mocker, client: AddressDocumentVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.anonymize_address_document_verification('adv_12345') == 'response'
        assert_api_call(mock, 'address-document-verifications/adv_12345/anonymize')

    def test_should_create_address_document_verification_attempt(self, mocker,
                                                                 client: AddressDocumentVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = AddressDocumentVerificationAttemptRequest()

        assert client.create_address_document_verification_attempt('adv_12345', body) == 'response'
        assert_api_call(mock, 'address-document-verifications/adv_12345/attempts', body)

    def test_should_get_address_document_verification_attempts(self, mocker,
                                                               client: AddressDocumentVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_address_document_verification_attempts('adv_12345') == 'response'
        assert_api_call(mock, 'address-document-verifications/adv_12345/attempts')

    def test_should_get_address_document_verification_attempt(self, mocker,
                                                              client: AddressDocumentVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_address_document_verification_attempt('adv_12345', 'adva_67890') == 'response'
        assert_api_call(mock, 'address-document-verifications/adv_12345/attempts/adva_67890')

    def test_should_get_address_document_verification_report(self, mocker,
                                                             client: AddressDocumentVerificationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_address_document_verification_report('adv_12345') == 'response'
        assert_api_call(mock, 'address-document-verifications/adv_12345/pdf-report')
