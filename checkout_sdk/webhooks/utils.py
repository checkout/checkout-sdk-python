import hashlib
import hmac

from checkout_sdk.errors import InvalidSignatureError


def _to_bytes(string):
    if isinstance(string, str):
        return bytes(string, 'utf-8')
    return bytes(string)


def _to_string(byte_sequence):
    if isinstance(byte_sequence, bytearray):
        return byte_sequence.decode("utf-8")
    return byte_sequence


def verify_signature(body, key, expected_signature):
    digest = hmac.new(
        _to_bytes(key),
        _to_bytes(body),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, digest):
        raise InvalidSignatureError()
