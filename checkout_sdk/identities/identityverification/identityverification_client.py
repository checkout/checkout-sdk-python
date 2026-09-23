from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.identities.entities import AttemptAssetsQueryFilter, AttemptsQueryFilter
from checkout_sdk.identities.identityverification.identityverification import (
    IdentityVerificationRequest,
    IdentityVerificationAndAttemptRequest,
    IdentityVerificationAttemptRequest,
)


class IdentityVerificationClient(Client):
    __CREATE_AND_OPEN_PATH = 'create-and-open-idv'
    __IDENTITY_VERIFICATIONS_PATH = 'identity-verifications'
    __ANONYMIZE_PATH = 'anonymize'
    __ATTEMPTS_PATH = 'attempts'
    __PDF_REPORT_PATH = 'pdf-report'
    __ASSETS_PATH = 'assets'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def create_identity_verification_and_attempt(self, request: IdentityVerificationAndAttemptRequest):
        """Create an identity verification and open its first attempt in one call.
        Beta.

        Args:
            request: The identity verification and attempt to create.
        Returns:
            ResponseWrapper with the created verification, including redirect_url.
        """
        return self._api_client.post(self.__CREATE_AND_OPEN_PATH,
                                     self._sdk_authorization(),
                                     request)

    def create_identity_verification(self, request: IdentityVerificationRequest):
        """Create an identity verification.
        Beta.

        Args:
            request: The identity verification to create.
        Returns:
            ResponseWrapper with the created verification.
        """
        return self._api_client.post(self.__IDENTITY_VERIFICATIONS_PATH,
                                     self._sdk_authorization(),
                                     request)

    def get_identity_verification(self, identity_verification_id: str):
        """Get the details of an identity verification.
        Beta.

        Args:
            identity_verification_id: The identity verification's unique identifier.
        Returns:
            ResponseWrapper with the verification details.
        """
        return self._api_client.get(self.build_path(self.__IDENTITY_VERIFICATIONS_PATH, identity_verification_id),
                                    self._sdk_authorization())

    def anonymize_identity_verification(self, identity_verification_id: str):
        """Anonymize an identity verification and its attempts.
        Beta.

        Args:
            identity_verification_id: The identity verification's unique identifier.
        Returns:
            ResponseWrapper with the anonymized verification.
        """
        return self._api_client.post(
            self.build_path(self.__IDENTITY_VERIFICATIONS_PATH, identity_verification_id, self.__ANONYMIZE_PATH),
            self._sdk_authorization())

    def create_identity_verification_attempt(self, identity_verification_id: str,
                                             request: IdentityVerificationAttemptRequest):
        """Create an attempt for an identity verification.
        Beta.

        Args:
            identity_verification_id: The identity verification's unique identifier.
            request: The attempt to create.
        Returns:
            ResponseWrapper with the created attempt, including redirect_url.
        """
        return self._api_client.post(
            self.build_path(self.__IDENTITY_VERIFICATIONS_PATH, identity_verification_id, self.__ATTEMPTS_PATH),
            self._sdk_authorization(),
            request)

    def get_identity_verification_attempts(self, identity_verification_id: str,
                                           query: AttemptsQueryFilter = None):
        """Get all the attempts for a specific identity verification.

        Results are paginated. Beta.

        Args:
            identity_verification_id: The identity verification's unique identifier.
            query: Optional skip and limit pagination parameters.
        Returns:
            ResponseWrapper with the paginated attempt list.
        """
        return self._api_client.get(
            self.build_path(self.__IDENTITY_VERIFICATIONS_PATH, identity_verification_id, self.__ATTEMPTS_PATH),
            self._sdk_authorization(),
            query)

    def get_identity_verification_attempt(self, identity_verification_id: str, attempt_id: str):
        """Get the details of a single identity verification attempt.
        Beta.

        Args:
            identity_verification_id: The identity verification's unique identifier.
            attempt_id: The attempt's unique identifier.
        Returns:
            ResponseWrapper with the attempt details.
        """
        return self._api_client.get(
            self.build_path(self.__IDENTITY_VERIFICATIONS_PATH, identity_verification_id, self.__ATTEMPTS_PATH,
                            attempt_id),
            self._sdk_authorization())

    def get_identity_verification_attempt_assets(self, identity_verification_id: str, attempt_id: str,
                                                 query: AttemptAssetsQueryFilter = None):
        """Get the assets (face images, videos, and document images) captured during an identity
        verification attempt. Videos are not exposed by default; contact your account manager
        to enable them.
        Results are paginated. Beta.

        Args:
            identity_verification_id: The identity verification's unique identifier.
            attempt_id: The attempt's unique identifier.
            query: Optional skip and limit pagination parameters.
        Returns:
            ResponseWrapper with the paginated asset list.
        """
        return self._api_client.get(
            self.build_path(self.__IDENTITY_VERIFICATIONS_PATH, identity_verification_id, self.__ATTEMPTS_PATH,
                            attempt_id, self.__ASSETS_PATH),
            self._sdk_authorization(),
            query)

    def get_identity_verification_report(self, identity_verification_id: str):
        """Get the PDF report for an identity verification.
        Beta.

        Args:
            identity_verification_id: The identity verification's unique identifier.
        Returns:
            ResponseWrapper carrying pdf_report, the pre-signed URL to the PDF.
        """
        return self._api_client.get(
            self.build_path(self.__IDENTITY_VERIFICATIONS_PATH, identity_verification_id, self.__PDF_REPORT_PATH),
            self._sdk_authorization())
