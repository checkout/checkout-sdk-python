from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
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

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def create_identity_verification_and_attempt(self, request: IdentityVerificationAndAttemptRequest):
        return self._api_client.post(self.__CREATE_AND_OPEN_PATH,
                                     self._sdk_authorization(),
                                     request)

    def create_identity_verification(self, request: IdentityVerificationRequest):
        return self._api_client.post(self.__IDENTITY_VERIFICATIONS_PATH,
                                     self._sdk_authorization(),
                                     request)

    def get_identity_verification(self, identity_verification_id: str):
        return self._api_client.get(self.build_path(self.__IDENTITY_VERIFICATIONS_PATH, identity_verification_id),
                                    self._sdk_authorization())

    def anonymize_identity_verification(self, identity_verification_id: str):
        return self._api_client.post(
            self.build_path(self.__IDENTITY_VERIFICATIONS_PATH, identity_verification_id, self.__ANONYMIZE_PATH),
            self._sdk_authorization())

    def create_identity_verification_attempt(self, identity_verification_id: str,
                                             request: IdentityVerificationAttemptRequest):
        return self._api_client.post(
            self.build_path(self.__IDENTITY_VERIFICATIONS_PATH, identity_verification_id, self.__ATTEMPTS_PATH),
            self._sdk_authorization(),
            request)

    def get_identity_verification_attempts(self, identity_verification_id: str):
        return self._api_client.get(
            self.build_path(self.__IDENTITY_VERIFICATIONS_PATH, identity_verification_id, self.__ATTEMPTS_PATH),
            self._sdk_authorization())

    def get_identity_verification_attempt(self, identity_verification_id: str, attempt_id: str):
        return self._api_client.get(
            self.build_path(self.__IDENTITY_VERIFICATIONS_PATH, identity_verification_id, self.__ATTEMPTS_PATH,
                            attempt_id),
            self._sdk_authorization())

    def get_identity_verification_report(self, identity_verification_id: str):
        return self._api_client.get(
            self.build_path(self.__IDENTITY_VERIFICATIONS_PATH, identity_verification_id, self.__PDF_REPORT_PATH),
            self._sdk_authorization())
