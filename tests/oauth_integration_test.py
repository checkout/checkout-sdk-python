import checkout_sdk
from checkout_sdk.customers.customers import CustomerRequest
from checkout_sdk.environment import Environment
from checkout_sdk.exception import CheckoutException
from checkout_sdk.four.oauth_scopes import OAuthScopes
from tests.checkout_test_utils import assert_response, random_email, phone


def test_should_create_customer_with_oauth(oauth_api):
    customer_request = CustomerRequest()
    customer_request.email = random_email()
    customer_request.name = 'OAuth Customer'
    customer_request.phone = phone()

    customer_response = oauth_api.customers.create(customer_request)
    assert_response(customer_response, 'id')
    return customer_response.id


def test_should_fail_init_authorization_invalid_credentials():
    try:
        checkout_sdk.OAuthSdk() \
            .client_credentials(client_id='fake_id',
                                client_secret='fake_secret') \
            .environment(Environment.sandbox()) \
            .scopes([OAuthScopes.GATEWAY, OAuthScopes.VAULT]) \
            .build()
    except CheckoutException as err:
        assert err.args[0] == 'OAuth client_credentials authentication failed with error: (invalid_client)'


def test_should_fail_init_authorization_invalid_credentials_and_host():
    try:
        checkout_sdk.OAuthSdk() \
            .client_credentials(client_id='fake_id',
                                client_secret='fake_secret') \
            .authorization_uri('https://test.checkout.com') \
            .environment(Environment.sandbox()) \
            .scopes([OAuthScopes.GATEWAY, OAuthScopes.VAULT]) \
            .build()
    except CheckoutException as err:
        assert err.args[0] == 'Unable to establish connection to host: (https://test.checkout.com)'
