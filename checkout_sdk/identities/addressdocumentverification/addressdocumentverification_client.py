from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.identities.entities import AttemptAssetsQueryFilter, AttemptsQueryFilter
from checkout_sdk.identities.addressdocumentverification.addressdocumentverification import (
    AddressDocumentVerificationRequest, AddressDocumentVerificationAttemptRequest
)


class AddressDocumentVerificationClient(Client):
    __ADDRESS_DOCUMENT_VERIFICATIONS_PATH = 'address-document-verifications'
    __ANONYMIZE_PATH = 'anonymize'
    __ATTEMPTS_PATH = 'attempts'
    __PDF_REPORT_PATH = 'pdf-report'
    __ASSETS_PATH = 'assets'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def create_address_document_verification(self, request: AddressDocumentVerificationRequest):
        """Create an address document verification.
        Beta.

        Args:
            request: The address document verification to create.
        Returns:
            ResponseWrapper with the created verification.
        """
        return self._api_client.post(self.__ADDRESS_DOCUMENT_VERIFICATIONS_PATH,
                                     self._sdk_authorization(),
                                     request)

    def get_address_document_verification(self, address_document_verification_id: str):
        """Get the details of an address document verification.
        Beta.

        Args:
            address_document_verification_id: The address document verification's unique identifier.
        Returns:
            ResponseWrapper with the verification details.
        """
        return self._api_client.get(
            self.build_path(self.__ADDRESS_DOCUMENT_VERIFICATIONS_PATH, address_document_verification_id),
            self._sdk_authorization())

    def anonymize_address_document_verification(self, address_document_verification_id: str):
        """Anonymize an address document verification and its attempts.
        Beta.

        Args:
            address_document_verification_id: The address document verification's unique identifier.
        Returns:
            ResponseWrapper with the anonymized verification.
        """
        return self._api_client.post(
            self.build_path(self.__ADDRESS_DOCUMENT_VERIFICATIONS_PATH, address_document_verification_id,
                            self.__ANONYMIZE_PATH),
            self._sdk_authorization())

    def create_address_document_verification_attempt(self, address_document_verification_id: str,
                                                     request: AddressDocumentVerificationAttemptRequest):
        """Create an attempt for an address document verification, uploading the document image.
        Beta.

        Args:
            address_document_verification_id: The address document verification's unique identifier.
            request: The attempt to create, carrying the document image.
        Returns:
            ResponseWrapper with the created attempt.
        """
        return self._api_client.post(
            self.build_path(self.__ADDRESS_DOCUMENT_VERIFICATIONS_PATH, address_document_verification_id,
                            self.__ATTEMPTS_PATH),
            self._sdk_authorization(),
            request)

    def get_address_document_verification_attempts(self, address_document_verification_id: str,
                                                   query: AttemptsQueryFilter = None):
        """Get the details of all attempts for a specific address document verification.

        Results are paginated. Beta.

        Args:
            address_document_verification_id: The address document verification's unique identifier.
            query: Optional skip and limit pagination parameters.
        Returns:
            ResponseWrapper with the paginated attempt list.
        """
        return self._api_client.get(
            self.build_path(self.__ADDRESS_DOCUMENT_VERIFICATIONS_PATH, address_document_verification_id,
                            self.__ATTEMPTS_PATH),
            self._sdk_authorization(),
            query)

    def get_address_document_verification_attempt(self, address_document_verification_id: str, attempt_id: str):
        """Get the details of a single address document verification attempt.
        Beta.

        Args:
            address_document_verification_id: The address document verification's unique identifier.
            attempt_id: The attempt's unique identifier.
        Returns:
            ResponseWrapper with the attempt details.
        """
        return self._api_client.get(
            self.build_path(self.__ADDRESS_DOCUMENT_VERIFICATIONS_PATH, address_document_verification_id,
                            self.__ATTEMPTS_PATH, attempt_id),
            self._sdk_authorization())

    def get_address_document_verification_report(self, address_document_verification_id: str):
        """Get the PDF report for an address document verification.
        Beta.

        Args:
            address_document_verification_id: The address document verification's unique identifier.
        Returns:
            ResponseWrapper carrying pdf_report, the pre-signed URL to the PDF.
        """
        return self._api_client.get(
            self.build_path(self.__ADDRESS_DOCUMENT_VERIFICATIONS_PATH, address_document_verification_id,
                            self.__PDF_REPORT_PATH),
            self._sdk_authorization())

    def get_address_document_verification_attempt_assets(self, address_document_verification_id: str,
                                                         attempt_id: str,
                                                         query: AttemptAssetsQueryFilter = None):
        """Get the assets (the document image) uploaded for an address document verification attempt.

        Results are paginated. Beta.

        Args:
            address_document_verification_id: The address document verification's unique identifier.
            attempt_id: The attempt's unique identifier.
            query: Optional skip and limit pagination parameters.
        Returns:
            ResponseWrapper with the paginated asset list.
        """
        return self._api_client.get(
            self.build_path(self.__ADDRESS_DOCUMENT_VERIFICATIONS_PATH, address_document_verification_id,
                            self.__ATTEMPTS_PATH, attempt_id, self.__ASSETS_PATH),
            self._sdk_authorization(),
            query)
