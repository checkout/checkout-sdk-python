from __future__ import absolute_import

from abc import ABCMeta

from checkout_sdk.api_client import ApiClient
from checkout_sdk.checkout_api import CheckoutApi
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.default_keys_credentials import DefaultKeysSdkCredentials
from checkout_sdk.static_keys_builder import StaticKeysBuilder, validate_secret_key, validate_public_key


class DefaultStaticKeys(StaticKeysBuilder, metaclass=ABCMeta):
    _PUBLIC_KEY_PATTERN = '^pk_(test_)?(\\w{8})-(\\w{4})-(\\w{4})-(\\w{4})-(\\w{12})$'
    _SECRET_KEY_PATTERN = '^sk_(test_)?(\\w{8})-(\\w{4})-(\\w{4})-(\\w{4})-(\\w{12})$'

    def secret_key(self, secret_key):
        super().secret_key(secret_key)
        return self

    def public_key(self, public_key):
        super().public_key(public_key)
        return self


class DefaultSdk(DefaultStaticKeys):

    def __init__(self):
        super().__init__()

    def build(self):
        validate_secret_key(self._SECRET_KEY_PATTERN, self._secret_key)
        validate_public_key(self._PUBLIC_KEY_PATTERN, self._public_key)
        configuration = CheckoutConfiguration(
            credentials=DefaultKeysSdkCredentials(secret_key=self._secret_key, public_key=self._public_key),
            environment=self._environment,
            http_client=self._http_client)
        return CheckoutApi(ApiClient(configuration, configuration.environment.base_uri), configuration)
