import os

import pytest

from checkout_sdk.checkout_sdk import CheckoutSdk
from checkout_sdk.environment import Environment
from checkout_sdk.exception import CheckoutArgumentException


def test_should_create_default_sdk():
    CheckoutSdk \
        .builder() \
        .secret_key(os.environ.get("CHECKOUT_DEFAULT_SECRET_KEY")) \
        .public_key(os.environ.get("CHECKOUT_DEFAULT_PUBLIC_KEY")) \
        .environment(Environment.sandbox()) \
        .environment_subdomain('123domain') \
        .build()

    sdk = CheckoutSdk \
        .builder() \
        .secret_key(os.environ.get("CHECKOUT_DEFAULT_SECRET_KEY")) \
        .public_key(os.environ.get("CHECKOUT_DEFAULT_PUBLIC_KEY")) \
        .environment(Environment.production()) \
        .environment_subdomain('123domain') \
        .build()

    assert sdk is not None
    assert sdk.tokens is not None


def test_should_create_default_sdk_with_legacy_domain():
    with pytest.deprecated_call():
        sdk = CheckoutSdk \
            .builder() \
            .secret_key(os.environ.get("CHECKOUT_DEFAULT_SECRET_KEY")) \
            .public_key(os.environ.get("CHECKOUT_DEFAULT_PUBLIC_KEY")) \
            .environment(Environment.sandbox()) \
            .use_legacy_domain() \
            .build()

    assert sdk is not None
    assert sdk.tokens is not None


def test_should_fail_without_subdomain_or_legacy_domain():
    with pytest.raises(CheckoutArgumentException) as excinfo:
        CheckoutSdk \
            .builder() \
            .secret_key(os.environ.get("CHECKOUT_DEFAULT_SECRET_KEY")) \
            .public_key(os.environ.get("CHECKOUT_DEFAULT_PUBLIC_KEY")) \
            .environment(Environment.sandbox()) \
            .build()

    assert "environment_subdomain is required" in str(excinfo.value)


def test_should_fail_with_both_subdomain_and_legacy_domain():
    with pytest.raises(CheckoutArgumentException) as excinfo, pytest.deprecated_call():
        CheckoutSdk \
            .builder() \
            .secret_key(os.environ.get("CHECKOUT_DEFAULT_SECRET_KEY")) \
            .public_key(os.environ.get("CHECKOUT_DEFAULT_PUBLIC_KEY")) \
            .environment(Environment.sandbox()) \
            .environment_subdomain('123domain') \
            .use_legacy_domain() \
            .build()

    assert "cannot both be set" in str(excinfo.value)


def test_should_fail_with_invalid_subdomain():
    with pytest.raises(CheckoutArgumentException) as excinfo:
        CheckoutSdk \
            .builder() \
            .secret_key(os.environ.get("CHECKOUT_DEFAULT_SECRET_KEY")) \
            .public_key(os.environ.get("CHECKOUT_DEFAULT_PUBLIC_KEY")) \
            .environment(Environment.sandbox()) \
            .environment_subdomain('not a subdomain') \
            .build()

    assert "invalid environment subdomain" in str(excinfo.value)


def test_should_create_default_sdk_with_subdomain():
    sdk_1 = CheckoutSdk \
        .builder() \
        .secret_key(os.environ.get("CHECKOUT_DEFAULT_SECRET_KEY")) \
        .public_key(os.environ.get("CHECKOUT_DEFAULT_PUBLIC_KEY")) \
        .environment(Environment.sandbox()) \
        .environment_subdomain('123domain') \
        .build()

    assert sdk_1 is not None

    sdk_2 = CheckoutSdk \
        .builder() \
        .secret_key(os.environ.get("CHECKOUT_DEFAULT_SECRET_KEY")) \
        .public_key(os.environ.get("CHECKOUT_DEFAULT_PUBLIC_KEY")) \
        .environment(Environment.production()) \
        .environment_subdomain('123domain') \
        .build()

    assert sdk_2 is not None
    assert sdk_2.tokens is not None


def test_should_fail_create_default_sdk():
    with pytest.raises(CheckoutArgumentException):
        CheckoutSdk \
            .builder() \
            .secret_key(os.environ.get("CHECKOUT_DEFAULT_PUBLIC_KEY")) \
            .environment(Environment.sandbox()) \
            .build()

    with pytest.raises(CheckoutArgumentException):
        CheckoutSdk \
            .builder() \
            .public_key('pk_sbox_pkh') \
            .environment(Environment.sandbox()) \
            .build()
