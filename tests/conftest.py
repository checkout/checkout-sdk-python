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


def use_subdomain():
    return os.environ.get('CHECKOUT_TEST_USE_SUBDOMAIN', '').lower() == 'true'


def configure_domain(builder):
    """
    Every client the suite builds has to choose a domain now that the merchant-specific subdomain
    is mandatory, so they all come through here. There are deliberately two modes.

    Default: the shared hosts. The sandbox OAuth clients are not provisioned for the
    merchant-specific subdomain, so pointing the token request at
    {subdomain}.access.sandbox.checkout.com returns invalid_client for every integration test.

    Opt-in: set CHECKOUT_TEST_USE_SUBDOMAIN=true and the suite runs against
    CHECKOUT_MERCHANT_SUBDOMAIN instead, exercising end to end the path merchants are being moved
    to. Once sandbox is provisioned like production, set that variable in the workflows and this
    becomes the mode CI runs in. The switch is deliberately separate from
    CHECKOUT_MERCHANT_SUBDOMAIN, which CI already exports, so provisioning drives the change rather
    than the presence of a secret.
    """
    subdomain = os.environ.get('CHECKOUT_MERCHANT_SUBDOMAIN')
    if use_subdomain() and subdomain and subdomain.strip():
        return builder.environment_subdomain(subdomain)
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
