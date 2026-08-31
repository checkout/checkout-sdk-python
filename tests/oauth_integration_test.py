import warnings
import pytest
from checkout_sdk.checkout_sdk import CheckoutSdk
from checkout_sdk.customers.customers import CustomerRequest
from checkout_sdk.environment import Environment
from checkout_sdk.exception import CheckoutArgumentException, CheckoutException
from checkout_sdk.oauth_scopes import OAuthScopes
from tests.checkout_test_utils import assert_response, random_email, phone


def test_should_create_customer_with_oauth(oauth_api):
    customer_request = CustomerRequest()
    customer_request.email = random_email()
    customer_request.name = 'OAuth Customer'
    customer_request.phone = phone()

    customer_response = oauth_api.customers.create(customer_request)
    assert_response(customer_response, 'id')


def test_should_fail_init_authorization_invalid_credentials():
    try:
        builder = CheckoutSdk \
            .builder() \
            .oauth() \
            .client_credentials(client_id='fake_id',
                                client_secret='fake_secret') \
            .environment(Environment.sandbox()) \
            .scopes([OAuthScopes.GATEWAY, OAuthScopes.VAULT])
        # The sandbox OAuth clients are not provisioned for the merchant-specific subdomain, so
        # the token request would come back invalid_client. Opting out explicitly until they are.
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', DeprecationWarning)
            builder.use_legacy_domain().build()
    except CheckoutException as err:
        assert err.args[0] == 'OAuth client_credentials authentication failed with error: (invalid_client)'


def test_should_fail_init_authorization_invalid_credentials_and_host():
    with pytest.raises(CheckoutArgumentException) as excinfo:
        CheckoutSdk \
            .builder() \
            .oauth() \
            .client_credentials(client_id='fake_id',
                                client_secret='fake_secret') \
            .authorization_uri('https://test.checkout.com') \
            .environment(Environment.sandbox()) \
            .environment_subdomain('123domain') \
            .scopes([OAuthScopes.GATEWAY, OAuthScopes.VAULT]) \
            .build()

    assert 'authorization_uri and environment_subdomain cannot both be set' in str(excinfo.value)


def test_should_fail_oauth_with_subdomain_invalid_credentials():
    try:
        CheckoutSdk \
            .builder() \
            .oauth() \
            .client_credentials(client_id='fake_id',
                                client_secret='fake_secret') \
            .environment(Environment.sandbox()) \
            .environment_subdomain('1234doma') \
            .scopes([OAuthScopes.GATEWAY, OAuthScopes.VAULT]) \
            .build()
    except CheckoutException as err:
        assert err.args[0] == 'OAuth client_credentials authentication failed with error: (invalid_client)'
