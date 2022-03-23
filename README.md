# Checkout.com Python SDK

![build-status](https://github.com/checkout/checkout-sdk-python/workflows/build-main/badge.svg)
[![GitHub license](https://img.shields.io/github/license/checkout/checkout-sdk-python.svg)](https://github.com/checkout/checkout-sdk-python/blob/main/LICENSE.md)

## Getting started

```
# Requires Python > 3.6
pip install checkout-sdk==3.0.0b1
```

Please check in [GitHub releases](https://github.com/checkout/checkout-sdk-python/releases) for all the versions
available.

## How to use the SDK

This SDK can be used with two different pair of API keys provided by Checkout. However, using different API keys imply
using specific API features. Please find in the table below the types of keys that can be used within this SDK.

| Account System | Public Key (example)                    | Secret Key (example)                    |
|----------------|-----------------------------------------|-----------------------------------------|
| default        | pk_g650ff27-7c42-4ce1-ae90-5691a188ee7b | sk_gk3517a8-3z01-45fq-b4bd-4282384b0a64 |
| Four           | pk_pkhpdtvabcf7hdgpwnbhw7r2uic          | sk_m73dzypy7cf3gf5d2xr4k7sxo4e          |

Note: sandbox keys have a `test_` or `sbox_` identifier, for Default and Four accounts respectively.

If you don't have your own API keys, you can sign up for a test
account [here](https://www.checkout.com/get-test-account).

**PLEASE NEVER SHARE OR PUBLISH YOUR CHECKOUT CREDENTIALS.**

## Default

Default keys client instantiation can be done as follows:

```python
import checkout_sdk
from checkout_sdk.environment import Environment


def default():
    checkout_api = checkout_sdk.DefaultSdk() \
        .secret_key('secret_key') \
        .public_key('public_key') \
        .environment(Environment.sandbox()) \
        .build()

    payments_client = checkout_api.payments
    payments_client.refund_payment('payment_id')

```

### Four

If your pair of keys matches the Four type, this is how the SDK should be used:

```python
import checkout_sdk
from checkout_sdk.environment import Environment


def four():
    checkout_api = checkout_sdk.FourSdk() \
        .secret_key('secret_key') \
        .public_key('public_key') \
        .environment(Environment.sandbox()) \
        .build()

    payments_client = checkout_api.payments
    payments_client.refund_payment('payment_id')
```

The SDK supports client credentials OAuth, when initialized as follows:

```python
import checkout_sdk
from checkout_sdk.environment import Environment
from checkout_sdk.four.oauth_scopes import OAuthScopes

def oauth():
    checkout_api = checkout_sdk.OAuthSdk() \
        .client_credentials(client_id='client_id', client_secret='client_secret') \
        .environment(Environment.sandbox()) \
        .scopes([OAuthScopes.GATEWAY_PAYMENT_REFUNDS, OAuthScopes.FILES]) \
        .build()

    payments_client = checkout_api.payments
    payments_client.refund_payment('payment_id')

```

## Logging

Checkout SDK custom logger can be enabled and configured through Python's logging module:

```python
import logging
logging.basicConfig()
logging.getLogger('checkout').setLevel(logging.INFO)
```

## HttpClient

Checkout SDK uses `requests` library to perform http operations, and you can provide your own custom http client implementing `HttpClientBuilderInterface`

```python
import requests
from requests import Session

import checkout_sdk
from checkout_sdk.environment import Environment
from checkout_sdk.four.oauth_scopes import OAuthScopes
from checkout_sdk.http_client_interface import HttpClientBuilderInterface


class CustomHttpClientBuilder(HttpClientBuilderInterface):

    def get_client(self) -> Session:
        session = requests.Session()
        session.max_redirects = 5
        return session


def oauth():
    checkout_api = checkout_sdk.OAuthSdk() \
        .client_credentials(client_id='client_id', client_secret='client_secret') \
        .environment(Environment.sandbox()) \
        .http_client_builder(CustomHttpClientBuilder()) \
        .scopes([OAuthScopes.GATEWAY_PAYMENT_REFUNDS, OAuthScopes.FILES]) \
        .build()

    payments_client = checkout_api.payments
    payments_client.refund_payment('payment_id')

```

## Exception handling

All the API responses that do not fall in the 2** status codes will cause a `CheckoutApiException`. The exception encapsulates
the `request_id`, `http_status_code` and a dictionary of `error_details`, if available.

```python
try:
    api.customers.get("customer_id")
except CheckoutApiException as err:
    request_id = err.request_id
    http_status_code = err.http_status_code
    error_details = err.error_details
```

* [API Reference (Default)](https://api-reference.checkout.com/)
* [API Reference (Four)](https://api-reference.checkout.com/preview/crusoe/)
* [Official Docs (Default)](https://docs.checkout.com/)
* [Official Docs (Four)](https://docs.checkout.com/four)

## Building from source

Once you checkout the code from GitHub, the project can be built using `pip`:

```
# install the latest version pip
python -m pip install --upgrade pip

# install project dependencies
pip install -r requirements-dev.txt

# run unit and integration tests
python -m pytest
```

The execution of integration tests require the following environment variables set in your system:

* For Default account systems: `CHECKOUT_PUBLIC_KEY` & `CHECKOUT_SECRET_KEY`
* For Four account systems: `CHECKOUT_FOUR_PUBLIC_KEY` & `CHECKOUT_FOUR_SECRET_KEY`
* For Four account systems (OAuth): `CHECKOUT_FOUR_OAUTH_CLIENT_ID` & `CHECKOUT_FOUR_OAUTH_CLIENT_SECRET`

## Code of Conduct

Please refer to [Code of Conduct](CODE_OF_CONDUCT.md)

## Licensing

[MIT](LICENSE.md)