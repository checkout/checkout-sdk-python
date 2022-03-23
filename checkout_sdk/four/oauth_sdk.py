from __future__ import absolute_import

from abc import ABCMeta

from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.checkout_sdk_builder import CheckoutSdkBuilder
from checkout_sdk.exception import CheckoutArgumentException
from checkout_sdk.four.checkout_api import CheckoutApi
from checkout_sdk.four.oauth_credentials import FourOAuthSdkCredentials


class OAuthSdk(CheckoutSdkBuilder, metaclass=ABCMeta):
    _client_id: str
    _client_secret: str
    _authorization_uri: str
    _scopes: list

    def __init__(self):
        super(OAuthSdk, self).__init__()

    def client_credentials(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret
        return self

    def authorization_uri(self, authorization_uri):
        self._authorization_uri = authorization_uri
        return self

    def scopes(self, scopes):
        self._scopes = scopes
        return self

    def build(self):
        self.validate_arguments()
        configuration = CheckoutConfiguration(
            credentials=FourOAuthSdkCredentials.init(http_client=self._http_client, client_id=self._client_id,
                                                     client_secret=self._client_secret, scopes=self._scopes,
                                                     authorization_uri=self._authorization_uri),
            environment=self._environment,
            http_client=self._http_client)
        return CheckoutApi(configuration)

    def validate_arguments(self):
        if not hasattr(self, '_authorization_uri'):
            if not hasattr(self, '_environment'):
                raise CheckoutArgumentException(
                    "Invalid configuration. Please specify an Environment or a specific OAuth authorizationURI.")
            self._authorization_uri = self._environment.authorization_uri
