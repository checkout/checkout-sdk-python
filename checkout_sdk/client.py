from __future__ import absolute_import

import re
from enum import Enum
from urllib.parse import quote

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.exception import CheckoutArgumentException

_FORBIDDEN_SEGMENT_CHARACTERS = re.compile(r'[/\\\x00-\x1f\x7f]')
_INVALID_SEGMENT_MESSAGE = ("Invalid path segment: it must be a non-empty string, not '.' or '..', "
                            "without '/', '\\' or ASCII control characters (U+0000 to U+001F, U+007F)")


class Client:

    def __init__(self, api_client: ApiClient,
                 configuration: CheckoutConfiguration,
                 authorization_type: AuthorizationType):
        self._api_client = api_client
        self._authorization_type = authorization_type
        self._configuration = configuration

    def _sdk_authorization(self, authorization_type: AuthorizationType = None):
        if authorization_type is not None:
            return self._configuration.credentials.get_authorization(authorization_type)
        else:
            return self._configuration.credentials.get_authorization(self._authorization_type)

    def is_sandbox(self):
        return self._configuration.environment.is_sandbox

    @staticmethod
    def build_path(*params):
        """Join path segments into a request path, encoding each one as a single segment.

        Every argument is percent-encoded (RFC 3986, only ``A-Z a-z 0-9 - . _ ~`` kept), so
        ``?``, ``#``, ``%`` and spaces stay inside their segment. Pass identifiers unencoded: an
        already encoded value is encoded again. Enum members are sent by their value.

        Args:
            *params: the path segments, path constants and caller identifiers alike.

        Returns:
            str: the segments joined with ``/``.

        Raises:
            CheckoutArgumentException: a segment is not a string (or a string-valued Enum
                member), is empty, ``.`` or ``..``, contains ``/``, ``\\`` or an ASCII control
                character (U+0000 to U+001F, U+007F), or cannot be encoded as UTF-8.
        """
        return '/'.join(Client._encode_path_segment(param) for param in params)

    @staticmethod
    def _encode_path_segment(value):
        # type() rather than isinstance(): a __class__ property cannot change it.
        if issubclass(type(value), Enum):
            value = value.value
        if not issubclass(type(value), str):
            raise CheckoutArgumentException(_INVALID_SEGMENT_MESSAGE)
        # Exact str copy of the characters, so no overridden method of a str subclass takes part.
        # A full slice copies on CPython and PyPy alike; str.__str__ keeps the subclass on PyPy.
        value = str.__getitem__(value, slice(None))
        if _FORBIDDEN_SEGMENT_CHARACTERS.search(value):
            raise CheckoutArgumentException(_INVALID_SEGMENT_MESSAGE)
        try:
            encoded = quote(value, safe='')
        except UnicodeEncodeError:
            raise CheckoutArgumentException(_INVALID_SEGMENT_MESSAGE) from None
        if encoded in ('', '.', '..'):
            raise CheckoutArgumentException(_INVALID_SEGMENT_MESSAGE)
        return encoded
