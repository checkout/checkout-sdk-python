import logging
import os

import pytest
import requests
from requests import Session

import checkout_sdk
from checkout_sdk.api_client import ApiClient
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.default_http_client import DefaultHttpClientBuilder
from checkout_sdk.environment import Environment
from checkout_sdk.four.oauth_scopes import OAuthScopes
from checkout_sdk.http_client_interface import HttpClientBuilderInterface
from checkout_sdk.sdk_credentials import SdkCredentials

logging.basicConfig()
logging.getLogger('checkout').setLevel(logging.INFO)


@pytest.fixture(scope='session', autouse=True)
def default_api():
    return checkout_sdk.DefaultSdk() \
        .secret_key(os.environ.get('CHECKOUT_SECRET_KEY')) \
        .public_key(os.environ.get('CHECKOUT_PUBLIC_KEY')) \
        .build()


@pytest.fixture(scope='session', autouse=True)
def four_api():
    return checkout_sdk.FourSdk() \
        .secret_key(os.environ.get('CHECKOUT_FOUR_SECRET_KEY')) \
        .public_key(os.environ.get('CHECKOUT_FOUR_PUBLIC_KEY')) \
        .build()


@pytest.fixture(scope='session', autouse=True)
def oauth_api():
    return checkout_sdk.OAuthSdk() \
        .client_credentials(client_id=os.environ.get('CHECKOUT_FOUR_OAUTH_CLIENT_ID'),
                            client_secret=os.environ.get('CHECKOUT_FOUR_OAUTH_CLIENT_SECRET')) \
        .http_client_builder(CustomHttpClientBuilder()) \
        .scopes([OAuthScopes.GATEWAY, OAuthScopes.VAULT, OAuthScopes.PAYOUTS_BANK_DETAILS,
                 OAuthScopes.SESSIONS_APP, OAuthScopes.SESSIONS_BROWSER, OAuthScopes.FX, OAuthScopes.MARKETPLACE,
                 OAuthScopes.FILES]) \
        .build()


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
