from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.identities.addressdocumentverification.addressdocumentverification import (
    AddressDocumentVerificationRequest, AddressDocumentVerificationAttemptRequest
)


class AddressDocumentVerificationClient(Client):
    __ADDRESS_DOCUMENT_VERIFICATIONS_PATH = 'address-document-verifications'
    __ANONYMIZE_PATH = 'anonymize'
    __ATTEMPTS_PATH = 'attempts'
    __PDF_REPORT_PATH = 'pdf-report'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def create_address_document_verification(self, request: AddressDocumentVerificationRequest):
        return self._api_client.post(self.__ADDRESS_DOCUMENT_VERIFICATIONS_PATH,
                                     self._sdk_authorization(),
                                     request)

    def get_address_document_verification(self, address_document_verification_id: str):
        return self._api_client.get(
            self.build_path(self.__ADDRESS_DOCUMENT_VERIFICATIONS_PATH, address_document_verification_id),
            self._sdk_authorization())

    def anonymize_address_document_verification(self, address_document_verification_id: str):
        return self._api_client.post(
            self.build_path(self.__ADDRESS_DOCUMENT_VERIFICATIONS_PATH, address_document_verification_id,
                            self.__ANONYMIZE_PATH),
            self._sdk_authorization())

    def create_address_document_verification_attempt(self, address_document_verification_id: str,
                                                     request: AddressDocumentVerificationAttemptRequest):
        return self._api_client.post(
            self.build_path(self.__ADDRESS_DOCUMENT_VERIFICATIONS_PATH, address_document_verification_id,
                            self.__ATTEMPTS_PATH),
            self._sdk_authorization(),
            request)

    def get_address_document_verification_attempts(self, address_document_verification_id: str):
        return self._api_client.get(
            self.build_path(self.__ADDRESS_DOCUMENT_VERIFICATIONS_PATH, address_document_verification_id,
                            self.__ATTEMPTS_PATH),
            self._sdk_authorization())

    def get_address_document_verification_attempt(self, address_document_verification_id: str, attempt_id: str):
        return self._api_client.get(
            self.build_path(self.__ADDRESS_DOCUMENT_VERIFICATIONS_PATH, address_document_verification_id,
                            self.__ATTEMPTS_PATH, attempt_id),
            self._sdk_authorization())

    def get_address_document_verification_report(self, address_document_verification_id: str):
        return self._api_client.get(
            self.build_path(self.__ADDRESS_DOCUMENT_VERIFICATIONS_PATH, address_document_verification_id,
                            self.__PDF_REPORT_PATH),
            self._sdk_authorization())
