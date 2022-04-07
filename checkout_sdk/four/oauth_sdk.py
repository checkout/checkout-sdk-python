from __future__ import absolute_import

from abc import ABCMeta

from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.checkout_sdk_builder import CheckoutSdkBuilder
from checkout_sdk.four.checkout_api import CheckoutApi
from checkout_sdk.four.oauth_credentials import FourOAuthSdkCredentials


class OAuthSdk(CheckoutSdkBuilder, metaclass=ABCMeta):
    _client_id: str = ''
    _client_secret: str = ''
    _authorization_uri: str = ''
    _scopes: list = []

    def __init__(self):
        super().__init__()

    def client_credentials(self, client_id: str, client_secret: str):
        self._client_id = client_id
        self._client_secret = client_secret
        return self

    def authorization_uri(self, authorization_uri: str):
        self._authorization_uri = authorization_uri
        return self

    def scopes(self, scopes: list):
        self._scopes = scopes
        return self

    def build(self):
        configuration = CheckoutConfiguration(
            credentials=FourOAuthSdkCredentials.init(http_client=self._http_client,
                                                     environment=self._environment,
                                                     client_id=self._client_id,
                                                     client_secret=self._client_secret,
                                                     scopes=self._scopes,
                                                     authorization_uri=self._authorization_uri),
            environment=self._environment,
            http_client=self._http_client)
        return CheckoutApi(configuration)
