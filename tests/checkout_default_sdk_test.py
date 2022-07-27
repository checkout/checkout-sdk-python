import pytest

from checkout_sdk.checkout_sdk import CheckoutSdk
from checkout_sdk.environment import Environment
from checkout_sdk.exception import CheckoutArgumentException


def test_should_create_default_sdk():
    CheckoutSdk \
        .builder() \
        .secret_key('sk_sbox_m73dzbpy7cf3gfd46xr4yj5xo4e') \
        .public_key('pk_sbox_pkhpdtvmkgf7hdnpwnbhw7r2uic') \
        .environment(Environment.sandbox()) \
        .build()

    sdk = CheckoutSdk \
        .builder() \
        .secret_key('sk_m73dzbpy7cf3gfd46xr4yj5xo4e') \
        .public_key('pk_pkhpdtvmkgf7hdnpwnbhw7r2uic') \
        .environment(Environment.production()) \
        .build()

    assert sdk is not None
    assert sdk.tokens is not None


def test_should_fail_create_default_sdk():
    with pytest.raises(CheckoutArgumentException):
        CheckoutSdk \
            .builder() \
            .secret_key('sk_sbox_m73dzbpy7c-f3gfd46xr4yj5xo4e') \
            .environment(Environment.sandbox()) \
            .build()

    with pytest.raises(CheckoutArgumentException):
        CheckoutSdk \
            .builder() \
            .public_key('pk_sbox_pkh') \
            .environment(Environment.sandbox()) \
            .build()
