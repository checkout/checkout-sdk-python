import os

from unittest.mock import Mock

import pytest

from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.environment import Environment
from checkout_sdk.environment_subdomain import EnvironmentSubdomain
from checkout_sdk.default_keys_credentials import DefaultKeysSdkCredentials
from checkout_sdk.http_client_interface import HttpClientBuilderInterface


def test_should_create_configuration():
    credentials = DefaultKeysSdkCredentials(
        os.environ.get("CHECKOUT_DEFAULT_SECRET_KEY"),
        os.environ.get("CHECKOUT_DEFAULT_PUBLIC_KEY")
    )
    http_client = Mock(spec=HttpClientBuilderInterface)

    configuration = CheckoutConfiguration(
        credentials=credentials,
        environment=Environment.sandbox(),
        http_client=http_client
    )

    assert configuration.credentials == credentials
    assert configuration.environment.base_uri == Environment.sandbox().base_uri
    assert configuration.environment.base_uri == "https://api.sandbox.checkout.com/"
    assert configuration.http_client == http_client
    assert configuration.environment_subdomain is None


@pytest.mark.parametrize(
    "subdomain, expected_url",
    [
        ("123dmain", "https://123dmain.api.sandbox.checkout.com/"),
        ("123domain", "https://123domain.api.sandbox.checkout.com/"),
        ("1234domain", "https://1234domain.api.sandbox.checkout.com/"),
        ("12345domain", "https://12345domain.api.sandbox.checkout.com/")
    ]
)
def test_should_create_configuration_with_subdomain(subdomain, expected_url):
    credentials = DefaultKeysSdkCredentials(
        os.environ.get("CHECKOUT_DEFAULT_SECRET_KEY"),
        os.environ.get("CHECKOUT_DEFAULT_PUBLIC_KEY")
    )
    http_client = Mock(spec=HttpClientBuilderInterface)

    environment_subdomain = EnvironmentSubdomain(Environment.sandbox(), subdomain)

    configuration = CheckoutConfiguration(
        credentials=credentials,
        environment=Environment.sandbox(),
        http_client=http_client,
        environment_subdomain=environment_subdomain
    )

    assert configuration.credentials == credentials
    assert configuration.environment.base_uri == Environment.sandbox().base_uri
    assert configuration.http_client == http_client
    assert configuration.environment_subdomain.base_uri == expected_url


@pytest.mark.parametrize(
    "subdomain, expected_url",
    [
        ("", "https://api.sandbox.checkout.com/"),
        ("123", "https://api.sandbox.checkout.com/"),
        ("123bad", "https://api.sandbox.checkout.com/"),
        ("12345domainBad", "https://api.sandbox.checkout.com/")
    ]
)
def test_should_create_configuration_with_bad_subdomain(subdomain, expected_url):
    credentials = DefaultKeysSdkCredentials(
        os.environ.get("CHECKOUT_DEFAULT_SECRET_KEY"),
        os.environ.get("CHECKOUT_DEFAULT_PUBLIC_KEY")
    )
    http_client = Mock(spec=HttpClientBuilderInterface)

    environment_subdomain = EnvironmentSubdomain(Environment.sandbox(), subdomain)

    configuration = CheckoutConfiguration(
        credentials=credentials,
        environment=Environment.sandbox(),
        http_client=http_client,
        environment_subdomain=environment_subdomain
    )

    assert configuration.credentials == credentials
    assert configuration.environment.base_uri == Environment.sandbox().base_uri
    assert configuration.http_client == http_client
    assert configuration.environment_subdomain.base_uri == expected_url
