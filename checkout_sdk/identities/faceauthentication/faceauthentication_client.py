from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.identities.entities import AttemptAssetsQueryFilter, AttemptsQueryFilter
from checkout_sdk.identities.faceauthentication.faceauthentication import (
    FaceAuthenticationRequest, FaceAuthenticationAttemptRequest
)


class FaceAuthenticationClient(Client):
    __FACE_AUTHENTICATIONS_PATH = 'face-authentications'
    __ANONYMIZE_PATH = 'anonymize'
    __ATTEMPTS_PATH = 'attempts'
    __ASSETS_PATH = 'assets'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def create_face_authentication(self, request: FaceAuthenticationRequest):
        """Create a face authentication.
        Beta.

        Args:
            request: The face authentication to create.
        Returns:
            ResponseWrapper with the created face authentication.
        """
        return self._api_client.post(self.__FACE_AUTHENTICATIONS_PATH,
                                     self._sdk_authorization(),
                                     request)

    def get_face_authentication(self, face_authentication_id: str):
        """Get the details of a face authentication.
        Beta.

        Args:
            face_authentication_id: The face authentication's unique identifier.
        Returns:
            ResponseWrapper with the face authentication details.
        """
        return self._api_client.get(self.build_path(self.__FACE_AUTHENTICATIONS_PATH, face_authentication_id),
                                    self._sdk_authorization())

    def anonymize_face_authentication(self, face_authentication_id: str):
        """Anonymize a face authentication and its attempts.
        Beta.

        Args:
            face_authentication_id: The face authentication's unique identifier.
        Returns:
            ResponseWrapper with the anonymized face authentication.
        """
        return self._api_client.post(
            self.build_path(self.__FACE_AUTHENTICATIONS_PATH, face_authentication_id, self.__ANONYMIZE_PATH),
            self._sdk_authorization())

    def create_face_authentication_attempt(self, face_authentication_id: str,
                                           request: FaceAuthenticationAttemptRequest):
        """Create an attempt for a face authentication.
        Beta.

        Args:
            face_authentication_id: The face authentication's unique identifier.
            request: The attempt to create.
        Returns:
            ResponseWrapper with the created attempt, including redirect_url.
        """
        return self._api_client.post(
            self.build_path(self.__FACE_AUTHENTICATIONS_PATH, face_authentication_id, self.__ATTEMPTS_PATH),
            self._sdk_authorization(),
            request)

    def get_face_authentication_attempts(self, face_authentication_id: str,
                                         query: AttemptsQueryFilter = None):
        """Get the details of all attempts for a specific face authentication.

        Results are paginated. Beta.

        Args:
            face_authentication_id: The face authentication's unique identifier.
            query: Optional skip and limit pagination parameters.
        Returns:
            ResponseWrapper with the paginated attempt list.
        """
        return self._api_client.get(
            self.build_path(self.__FACE_AUTHENTICATIONS_PATH, face_authentication_id, self.__ATTEMPTS_PATH),
            self._sdk_authorization(),
            query)

    def get_face_authentication_attempt(self, face_authentication_id: str, attempt_id: str):
        """Get the details of a single face authentication attempt.
        Beta.

        Args:
            face_authentication_id: The face authentication's unique identifier.
            attempt_id: The attempt's unique identifier.
        Returns:
            ResponseWrapper with the attempt details.
        """
        return self._api_client.get(
            self.build_path(self.__FACE_AUTHENTICATIONS_PATH, face_authentication_id, self.__ATTEMPTS_PATH,
                            attempt_id),
            self._sdk_authorization())

    def get_face_authentication_attempt_assets(self, face_authentication_id: str, attempt_id: str,
                                               query: AttemptAssetsQueryFilter = None):
        """Get the assets (face images and videos) captured during a face authentication attempt.
        Videos are not exposed by default; contact your account manager to enable them.
        Results are paginated. Beta.

        Args:
            face_authentication_id: The face authentication's unique identifier.
            attempt_id: The attempt's unique identifier.
            query: Optional skip and limit pagination parameters.
        Returns:
            ResponseWrapper with the paginated asset list.
        """
        return self._api_client.get(
            self.build_path(self.__FACE_AUTHENTICATIONS_PATH, face_authentication_id, self.__ATTEMPTS_PATH,
                            attempt_id, self.__ASSETS_PATH),
            self._sdk_authorization(),
            query)
