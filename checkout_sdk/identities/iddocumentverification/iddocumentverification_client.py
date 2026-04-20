from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.identities.iddocumentverification.iddocumentverification import (
    IdDocumentVerificationRequest, IdDocumentVerificationAttemptRequest
)


class IdDocumentVerificationClient(Client):
    __ID_DOCUMENT_VERIFICATIONS_PATH = 'id-document-verifications'
    __ANONYMIZE_PATH = 'anonymize'
    __ATTEMPTS_PATH = 'attempts'
    __PDF_REPORT_PATH = 'pdf-report'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def create_id_document_verification(self, request: IdDocumentVerificationRequest):
        return self._api_client.post(self.__ID_DOCUMENT_VERIFICATIONS_PATH,
                                     self._sdk_authorization(),
                                     request)

    def get_id_document_verification(self, id_document_verification_id: str):
        return self._api_client.get(
            self.build_path(self.__ID_DOCUMENT_VERIFICATIONS_PATH, id_document_verification_id),
            self._sdk_authorization())

    def anonymize_id_document_verification(self, id_document_verification_id: str):
        return self._api_client.post(
            self.build_path(self.__ID_DOCUMENT_VERIFICATIONS_PATH, id_document_verification_id,
                            self.__ANONYMIZE_PATH),
            self._sdk_authorization())

    def create_id_document_verification_attempt(self, id_document_verification_id: str,
                                                request: IdDocumentVerificationAttemptRequest):
        return self._api_client.post(
            self.build_path(self.__ID_DOCUMENT_VERIFICATIONS_PATH, id_document_verification_id,
                            self.__ATTEMPTS_PATH),
            self._sdk_authorization(),
            request)

    def get_id_document_verification_attempts(self, id_document_verification_id: str):
        return self._api_client.get(
            self.build_path(self.__ID_DOCUMENT_VERIFICATIONS_PATH, id_document_verification_id,
                            self.__ATTEMPTS_PATH),
            self._sdk_authorization())

    def get_id_document_verification_attempt(self, id_document_verification_id: str, attempt_id: str):
        return self._api_client.get(
            self.build_path(self.__ID_DOCUMENT_VERIFICATIONS_PATH, id_document_verification_id,
                            self.__ATTEMPTS_PATH, attempt_id),
            self._sdk_authorization())

    def get_id_document_verification_report(self, id_document_verification_id: str):
        return self._api_client.get(
            self.build_path(self.__ID_DOCUMENT_VERIFICATIONS_PATH, id_document_verification_id,
                            self.__PDF_REPORT_PATH),
            self._sdk_authorization())
