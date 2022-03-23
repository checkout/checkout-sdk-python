from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.sessions.session_secret_credentials import SessionSecretSdkCredentials
from checkout_sdk.sessions.sessions import SessionRequest, ChannelData, ThreeDsMethodCompletionRequest


class SessionsClient(Client):
    __SESSIONS_PATH = 'sessions'
    __COLLECT_DATA_PATH = 'collect-data'
    __COMPLETE_PATH = 'complete'
    __ISSUER_FINGERPRINT_PATH = 'issuer-fingerprint'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.OAUTH)

    def request_session(self, session_request: SessionRequest):
        return self._api_client.post(self.__SESSIONS_PATH, self._sdk_authorization(), session_request)

    def get_session_details(self, session_id: str, session_secret: str = None):
        return self._api_client.get(self.build_path(self.__SESSIONS_PATH, session_id),
                                    self.__custom_sdk_authorization(session_secret))

    def update_session(self, session_id: str, channel_data: ChannelData, session_secret: str = None):
        return self._api_client.put(self.build_path(self.__SESSIONS_PATH, session_id, self.__COLLECT_DATA_PATH),
                                    self.__custom_sdk_authorization(session_secret), channel_data)

    def complete_session(self, session_id: str, session_secret: str = None):
        return self._api_client.post(self.build_path(self.__SESSIONS_PATH, session_id, self.__COMPLETE_PATH),
                                     self.__custom_sdk_authorization(session_secret))

    def update_3ds_method_completion(self, session_id: str,
                                     three_ds_method_completion_request: ThreeDsMethodCompletionRequest,
                                     session_secret: str = None):
        return self._api_client.put(self.build_path(self.__SESSIONS_PATH, session_id, self.__ISSUER_FINGERPRINT_PATH),
                                    self.__custom_sdk_authorization(session_secret),
                                    three_ds_method_completion_request)

    def __custom_sdk_authorization(self, session_secret: str = None):
        if session_secret is None:
            return self._sdk_authorization()
        else:
            return SessionSecretSdkCredentials(session_secret).get_authorization(AuthorizationType.CUSTOM)
