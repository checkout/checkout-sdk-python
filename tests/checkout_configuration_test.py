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


def test_environment_sandbox_urls():
    env = Environment.sandbox()
    assert env.base_uri == "https://api.sandbox.checkout.com/"
    assert env.forward_uri == "https://forward.sandbox.checkout.com/"
    assert env.identity_uri == "https://identity-verification.sandbox.checkout.com/"


def test_environment_production_urls():
    env = Environment.production()
    assert env.base_uri == "https://api.checkout.com/"
    assert env.forward_uri == "https://forward.checkout.com/"
    assert env.identity_uri == "https://identity-verification.checkout.com/"


@pytest.mark.parametrize(
    "subdomain, expected_url",
    [
        ("a", "https://a.api.sandbox.checkout.com/"),
        ("ab", "https://ab.api.sandbox.checkout.com/"),
        ("abc", "https://abc.api.sandbox.checkout.com/"),
        ("abc1", "https://abc1.api.sandbox.checkout.com/"),
        ("12345domain", "https://12345domain.api.sandbox.checkout.com/"),
        ("pl-vkuhvk4v", "https://pl-vkuhvk4v.api.sandbox.checkout.com/"),
        ("pl-abc123", "https://pl-abc123.api.sandbox.checkout.com/")
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
    assert configuration.environment_subdomain.authorization_uri == (
        f"https://{subdomain}.access.sandbox.checkout.com/connect/token"
    )


@pytest.mark.parametrize(
    "subdomain, expected_url",
    [
        ("", "https://api.sandbox.checkout.com/"),
        (" ", "https://api.sandbox.checkout.com/"),
        ("   ", "https://api.sandbox.checkout.com/"),
        (" - ", "https://api.sandbox.checkout.com/"),
        ("a b", "https://api.sandbox.checkout.com/"),
        ("ab c1.", "https://api.sandbox.checkout.com/"),
        ("foo-", "https://api.sandbox.checkout.com/"),
        ("-foo", "https://api.sandbox.checkout.com/"),
        ("FooBar", "https://api.sandbox.checkout.com/"),
        ("test-123", "https://api.sandbox.checkout.com/"),
        ("foo-bar", "https://api.sandbox.checkout.com/"),
        ("pl-", "https://api.sandbox.checkout.com/")
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
    assert configuration.environment_subdomain.authorization_uri == "https://access.sandbox.checkout.com/connect/token"


def test_should_create_configuration_with_subdomain_for_production():
    subdomain = "1234prod"
    credentials = DefaultKeysSdkCredentials(
        os.environ.get("CHECKOUT_DEFAULT_SECRET_KEY"),
        os.environ.get("CHECKOUT_DEFAULT_PUBLIC_KEY")
    )
    http_client = Mock(spec=HttpClientBuilderInterface)

    environment_subdomain = EnvironmentSubdomain(Environment.production(), subdomain)

    configuration = CheckoutConfiguration(
        credentials=credentials,
        environment=Environment.production(),
        http_client=http_client,
        environment_subdomain=environment_subdomain
    )

    assert configuration.credentials == credentials
    assert configuration.environment.base_uri == Environment.production().base_uri
    assert configuration.http_client == http_client
    assert configuration.environment_subdomain.base_uri == f"https://{subdomain}.api.checkout.com/"
    assert configuration.environment_subdomain.authorization_uri == (
        f"https://{subdomain}.access.checkout.com/connect/token"
    )
