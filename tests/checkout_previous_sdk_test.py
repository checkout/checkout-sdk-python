import pytest

from checkout_sdk.checkout_sdk import CheckoutSdk
from checkout_sdk.environment import Environment
from checkout_sdk.exception import CheckoutArgumentException


def test_should_create_previous_sdk():
    CheckoutSdk \
        .builder() \
        .previous() \
        .secret_key('sk_test_fde517a8-3f01-41ef-b4bd-4282384b0a64') \
        .public_key('pk_test_fe70ff27-7c32-4ce1-ae90-5691a188ee7b') \
        .environment(Environment.sandbox()) \
        .build()

    sdk = CheckoutSdk \
        .builder() \
        .previous() \
        .secret_key('sk_fde517a8-3f01-41ef-b4bd-4282384b0a64') \
        .public_key('pk_fe70ff27-7c32-4ce1-ae90-5691a188ee7b') \
        .environment(Environment.production()) \
        .build()

    assert sdk is not None
    assert sdk.tokens is not None
    assert sdk.sources is not None


def test_should_fail_create_previous_sdk():
    with pytest.raises(CheckoutArgumentException):
        CheckoutSdk \
            .builder() \
            .previous() \
            .secret_key('sk_test_asdsad3q4dq') \
            .environment(Environment.sandbox()) \
            .build()

    with pytest.raises(CheckoutArgumentException):
        CheckoutSdk \
            .builder() \
            .previous() \
            .public_key('pk_test_q414dasds') \
            .environment(Environment.sandbox()) \
            .build()
