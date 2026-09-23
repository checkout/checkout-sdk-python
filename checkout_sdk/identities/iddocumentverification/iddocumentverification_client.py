from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.identities.entities import AttemptAssetsQueryFilter, AttemptsQueryFilter
from checkout_sdk.identities.iddocumentverification.iddocumentverification import (
    IdDocumentVerificationRequest, IdDocumentVerificationAttemptRequest
)


class IdDocumentVerificationClient(Client):
    __ID_DOCUMENT_VERIFICATIONS_PATH = 'id-document-verifications'
    __ANONYMIZE_PATH = 'anonymize'
    __ATTEMPTS_PATH = 'attempts'
    __PDF_REPORT_PATH = 'pdf-report'
    __ASSETS_PATH = 'assets'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def create_id_document_verification(self, request: IdDocumentVerificationRequest):
        """Create an ID document verification.
        Beta.

        Args:
            request: The ID document verification to create.
        Returns:
            ResponseWrapper with the created verification.
        """
        return self._api_client.post(self.__ID_DOCUMENT_VERIFICATIONS_PATH,
                                     self._sdk_authorization(),
                                     request)

    def get_id_document_verification(self, id_document_verification_id: str):
        """Get the details of an ID document verification.
        Beta.

        Args:
            id_document_verification_id: The ID document verification's unique identifier.
        Returns:
            ResponseWrapper with the verification details.
        """
        return self._api_client.get(
            self.build_path(self.__ID_DOCUMENT_VERIFICATIONS_PATH, id_document_verification_id),
            self._sdk_authorization())

    def anonymize_id_document_verification(self, id_document_verification_id: str):
        """Anonymize an ID document verification and its attempts.
        Beta.

        Args:
            id_document_verification_id: The ID document verification's unique identifier.
        Returns:
            ResponseWrapper with the anonymized verification.
        """
        return self._api_client.post(
            self.build_path(self.__ID_DOCUMENT_VERIFICATIONS_PATH, id_document_verification_id,
                            self.__ANONYMIZE_PATH),
            self._sdk_authorization())

    def create_id_document_verification_attempt(self, id_document_verification_id: str,
                                                request: IdDocumentVerificationAttemptRequest):
        """Create an attempt for an ID document verification, uploading the document images.
        Beta.

        Args:
            id_document_verification_id: The ID document verification's unique identifier.
            request: The attempt to create, carrying the front and back document images.
        Returns:
            ResponseWrapper with the created attempt.
        """
        return self._api_client.post(
            self.build_path(self.__ID_DOCUMENT_VERIFICATIONS_PATH, id_document_verification_id,
                            self.__ATTEMPTS_PATH),
            self._sdk_authorization(),
            request)

    def get_id_document_verification_attempts(self, id_document_verification_id: str,
                                              query: AttemptsQueryFilter = None):
        """Get the details of all attempts for a specific ID document verification.

        Results are paginated. Beta.

        Args:
            id_document_verification_id: The ID document verification's unique identifier.
            query: Optional skip and limit pagination parameters.
        Returns:
            ResponseWrapper with the paginated attempt list.
        """
        return self._api_client.get(
            self.build_path(self.__ID_DOCUMENT_VERIFICATIONS_PATH, id_document_verification_id,
                            self.__ATTEMPTS_PATH),
            self._sdk_authorization(),
            query)

    def get_id_document_verification_attempt(self, id_document_verification_id: str, attempt_id: str):
        """Get the details of a single ID document verification attempt.
        Beta.

        Args:
            id_document_verification_id: The ID document verification's unique identifier.
            attempt_id: The attempt's unique identifier.
        Returns:
            ResponseWrapper with the attempt details.
        """
        return self._api_client.get(
            self.build_path(self.__ID_DOCUMENT_VERIFICATIONS_PATH, id_document_verification_id,
                            self.__ATTEMPTS_PATH, attempt_id),
            self._sdk_authorization())

    def get_id_document_verification_report(self, id_document_verification_id: str):
        """Get the PDF report for an ID document verification.
        Beta.

        Args:
            id_document_verification_id: The ID document verification's unique identifier.
        Returns:
            ResponseWrapper carrying pdf_report, the pre-signed URL to the PDF.
        """
        return self._api_client.get(
            self.build_path(self.__ID_DOCUMENT_VERIFICATIONS_PATH, id_document_verification_id,
                            self.__PDF_REPORT_PATH),
            self._sdk_authorization())

    def get_id_document_verification_attempt_assets(self, id_document_verification_id: str, attempt_id: str,
                                                    query: AttemptAssetsQueryFilter = None):
        """Get the assets (the front and back images of the document) uploaded for an ID document
        verification attempt.

        Results are paginated. Beta.

        Args:
            id_document_verification_id: The ID document verification's unique identifier.
            attempt_id: The attempt's unique identifier.
            query: Optional skip and limit pagination parameters.
        Returns:
            ResponseWrapper with the paginated asset list.
        """
        return self._api_client.get(
            self.build_path(self.__ID_DOCUMENT_VERIFICATIONS_PATH, id_document_verification_id,
                            self.__ATTEMPTS_PATH, attempt_id, self.__ASSETS_PATH),
            self._sdk_authorization(),
            query)
