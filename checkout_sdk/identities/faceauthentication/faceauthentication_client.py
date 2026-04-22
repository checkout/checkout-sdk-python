from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.identities.faceauthentication.faceauthentication import (
    FaceAuthenticationRequest, FaceAuthenticationAttemptRequest
)


class FaceAuthenticationClient(Client):
    __FACE_AUTHENTICATIONS_PATH = 'face-authentications'
    __ANONYMIZE_PATH = 'anonymize'
    __ATTEMPTS_PATH = 'attempts'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def create_face_authentication(self, request: FaceAuthenticationRequest):
        return self._api_client.post(self.__FACE_AUTHENTICATIONS_PATH,
                                     self._sdk_authorization(),
                                     request)

    def get_face_authentication(self, face_authentication_id: str):
        return self._api_client.get(self.build_path(self.__FACE_AUTHENTICATIONS_PATH, face_authentication_id),
                                    self._sdk_authorization())

    def anonymize_face_authentication(self, face_authentication_id: str):
        return self._api_client.post(
            self.build_path(self.__FACE_AUTHENTICATIONS_PATH, face_authentication_id, self.__ANONYMIZE_PATH),
            self._sdk_authorization())

    def create_face_authentication_attempt(self, face_authentication_id: str, request: FaceAuthenticationAttemptRequest):
        return self._api_client.post(
            self.build_path(self.__FACE_AUTHENTICATIONS_PATH, face_authentication_id, self.__ATTEMPTS_PATH),
            self._sdk_authorization(),
            request)

    def get_face_authentication_attempts(self, face_authentication_id: str):
        return self._api_client.get(
            self.build_path(self.__FACE_AUTHENTICATIONS_PATH, face_authentication_id, self.__ATTEMPTS_PATH),
            self._sdk_authorization())

    def get_face_authentication_attempt(self, face_authentication_id: str, attempt_id: str):
        return self._api_client.get(
            self.build_path(self.__FACE_AUTHENTICATIONS_PATH, face_authentication_id, self.__ATTEMPTS_PATH,
                            attempt_id),
            self._sdk_authorization())
