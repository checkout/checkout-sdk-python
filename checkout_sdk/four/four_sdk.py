from __future__ import absolute_import

from abc import ABCMeta

from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.four.checkout_api import CheckoutApi
from checkout_sdk.four.four_keys_credentials import FourKeysSdkCredentials
from checkout_sdk.static_keys_builder import StaticKeysBuilder, validate_secret_key, validate_public_key


class FourStaticKeys(StaticKeysBuilder, metaclass=ABCMeta):
    _PUBLIC_KEY_PATTERN = '^pk_(sbox_)?[a-z2-7]{26}[a-z2-7*#$=]$'
    _SECRET_KEY_PATTERN = '^sk_(sbox_)?[a-z2-7]{26}[a-z2-7*#$=]$'

    def secret_key(self, secret_key):
        super().secret_key(secret_key)
        return self

    def public_key(self, public_key):
        super().public_key(public_key)
        return self


class FourSdk(FourStaticKeys):

    def __init__(self):
        super().__init__()

    def build(self):
        validate_secret_key(self._SECRET_KEY_PATTERN, self._secret_key)
        validate_public_key(self._PUBLIC_KEY_PATTERN, self._public_key)
        configuration = CheckoutConfiguration(
            credentials=FourKeysSdkCredentials(secret_key=self._secret_key, public_key=self._public_key),
            environment=self._environment,
            http_client=self._http_client)
        return CheckoutApi(configuration)
