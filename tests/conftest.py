import logging
import os
import warnings

import pytest
import requests
from requests import Session

from checkout_sdk import CheckoutSdk
from checkout_sdk.api_client import ApiClient
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.default_http_client import DefaultHttpClientBuilder
from checkout_sdk.environment import Environment
from checkout_sdk.http_client_interface import HttpClientBuilderInterface
from checkout_sdk.oauth_scopes import OAuthScopes
from checkout_sdk.sdk_credentials import SdkCredentials

logging.basicConfig()
logging.getLogger('checkout').setLevel(logging.INFO)


def configure_domain(builder):
    """
    Every client the suite builds has to choose a domain now that the merchant-specific
    subdomain is mandatory, so they all come through here.

    The suite uses the shared hosts. It would be better to exercise the merchant-specific
    subdomain, since that is the path merchants are being moved to, but the sandbox OAuth
    clients are not provisioned for it: pointing the token request at
    {subdomain}.access.sandbox.checkout.com returns invalid_client for every integration test.
    Until those clients are bound to the subdomain, CI has to use the legacy hosts.
    """
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', DeprecationWarning)
        return builder.use_legacy_domain()


@pytest.fixture(scope='session', autouse=True)
def previous_api():
    return CheckoutSdk \
        .builder() \
        .previous() \
        .secret_key(os.environ.get('CHECKOUT_PREVIOUS_SECRET_KEY')) \
        .public_key(os.environ.get('CHECKOUT_PREVIOUS_PUBLIC_KEY')) \
        .build()


@pytest.fixture(scope='session', autouse=True)
def default_api():
    return configure_domain(CheckoutSdk()
                            .builder()
                            .secret_key(os.environ.get('CHECKOUT_DEFAULT_SECRET_KEY'))
                            .public_key(os.environ.get('CHECKOUT_DEFAULT_PUBLIC_KEY'))).build()


@pytest.fixture(scope='session', autouse=True)
def oauth_api():
    builder = CheckoutSdk() \
        .builder() \
        .oauth() \
        .client_credentials(client_id=os.environ.get('CHECKOUT_DEFAULT_OAUTH_CLIENT_ID'),
                            client_secret=os.environ.get('CHECKOUT_DEFAULT_OAUTH_CLIENT_SECRET')) \
        .http_client_builder(CustomHttpClientBuilder()) \
        .scopes([OAuthScopes.GATEWAY, OAuthScopes.VAULT, OAuthScopes.PAYOUTS_BANK_DETAILS,
                 OAuthScopes.SESSIONS_APP, OAuthScopes.SESSIONS_BROWSER, OAuthScopes.FX, OAuthScopes.ACCOUNTS,
                 OAuthScopes.FILES, OAuthScopes.TRANSFERS, OAuthScopes.BALANCES_VIEW,
                 OAuthScopes.VAULT_CARD_METADATA, OAuthScopes.FINANCIAL_ACTIONS,
                 OAuthScopes.VAULT_REAL_TIME_ACCOUNT_UPDATER, OAuthScopes.PAYMENTS_SEARCH,
                 OAuthScopes.GATEWAY_PAYMENT_CANCELLATIONS])
    return configure_domain(builder).build()


@pytest.fixture(scope='session', autouse=True)
def mock_sdk_configuration():
    return CheckoutConfiguration(SdkCredentials(), Environment.sandbox(), DefaultHttpClientBuilder().get_client())


@pytest.fixture(scope='session', autouse=True)
def mock_api_client(mock_sdk_configuration):
    return ApiClient(configuration=mock_sdk_configuration, base_uri=mock_sdk_configuration.environment.base_uri)


class CustomHttpClientBuilder(HttpClientBuilderInterface):

    def get_client(self) -> Session:
        session = requests.Session()
        session.max_redirects = 5
        return session
