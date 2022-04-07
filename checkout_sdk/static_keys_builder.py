from __future__ import absolute_import

import re
from abc import ABCMeta

from checkout_sdk.checkout_sdk_builder import CheckoutSdkBuilder
from checkout_sdk.exception import CheckoutArgumentException


def validate_key(regex, key):
    return re.match(regex, key)


def validate_secret_key(regex, secret_key=None):
    if secret_key is None or not validate_key(regex, secret_key):
        raise CheckoutArgumentException('invalid secret key')


def validate_public_key(regex, public_key=None):
    if not public_key:
        return
    if validate_key(regex, public_key):
        return
    raise CheckoutArgumentException('invalid public key')


class StaticKeysBuilder(CheckoutSdkBuilder, metaclass=ABCMeta):
    _public_key: str = None
    _secret_key: str = None

    def __init__(self):
        super().__init__()

    def secret_key(self, secret_key):
        self._secret_key = secret_key
        return self

    def public_key(self, public_key):
        self._public_key = public_key
        return self
