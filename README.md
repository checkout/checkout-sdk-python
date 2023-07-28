# Checkout.com Python SDK

[![build-status](https://github.com/checkout/checkout-sdk-python/workflows/build-main/badge.svg)](https://github.com/checkout/checkout-sdk-python/actions/workflows/build-main.yml)
![CodeQL](https://github.com/checkout/checkout-sdk-python/workflows/CodeQL/badge.svg)

[![build-status](https://github.com/checkout/checkout-sdk-python/workflows/build-release/badge.svg)](https://github.com/checkout/checkout-sdk-python/actions/workflows/build-release.yml)
[![GitHub release](https://img.shields.io/github/release/checkout/checkout-sdk-python.svg)](https://GitHub.com/checkout/checkout-sdk-php/releases/)
[![PyPI - latest](https://img.shields.io/pypi/v/checkout-sdk?label=latest&logo=pypi)](https://pypi.org/project/checkout-sdk)

[![GitHub license](https://img.shields.io/github/license/checkout/checkout-sdk-python.svg)](https://github.com/checkout/checkout-sdk-python/blob/main/LICENSE.md)

## Getting started

```
# Requires Python > 3.6
pip install checkout-sdk==<version>
```

> **Version 3.0.0 is here!**
>  <br/><br/>
> We improved the initialization of SDK making it easier to understand the available options. <br/>
> Now `NAS` accounts are the default instance for the SDK and `ABC` structure was moved to a `previous` prefixes. <br/>
> If you have been using this SDK before, you may find the following important changes:
> * Imports: if you used to import `checkout_sdk.payments.payments` now use `checkout_sdk.payments.payments_previous`
> * Marketplace module was moved to Accounts module, same for classes and references.
> * In most cases, IDE can help you determine from where to import, but if you’re still having issues don't hesitate to open a [ticket](https://github.com/checkout/checkout-sdk-python/issues/new/choose).


### :rocket: Please check in [GitHub releases](https://github.com/checkout/checkout-sdk-python/releases) for all the versions available.

### :book: Checkout our official documentation.

* [Official Docs (Default)](https://docs.checkout.com/)
* [Official Docs (Previous)](https://docs.checkout.com/previous)

### :books: Check out our official API documentation guide, where you can also find more usage examples.

* [API Reference (Default)](https://api-reference.checkout.com/)
* [API Reference (Previous)](https://api-reference.checkout.com/previous)

## How to use the SDK

This SDK can be used with two different pair of API keys provided by Checkout. However, using different API keys imply
using specific API features. Please find in the table below the types of keys that can be used within this SDK.

| Account System | Public Key (example)                    | Secret Key (example)                    |
|----------------|-----------------------------------------|-----------------------------------------|
| Default        | pk_pkhpdtvabcf7hdgpwnbhw7r2uic          | sk_m73dzypy7cf3gf5d2xr4k7sxo4e          |
| Previous       | pk_g650ff27-7c42-4ce1-ae90-5691a188ee7b | sk_gk3517a8-3z01-45fq-b4bd-4282384b0a64 |

Note: sandbox keys have a `sbox_` or `test_` identifier, for Default and Previous accounts respectively.

If you don't have your own API keys, you can sign up for a test
account [here](https://www.checkout.com/get-test-account).

**PLEASE NEVER SHARE OR PUBLISH YOUR CHECKOUT CREDENTIALS.**

### Default

Default keys client instantiation can be done as follows:

```python
from checkout_sdk.checkout_sdk import CheckoutSdk
from checkout_sdk.environment import Environment


def default():
    # public key is optional, only required for operations related with tokens
    checkout_api = CheckoutSdk
        .builder()
        .secret_key('secret_key')
        .public_key('public_key')
        .environment(Environment.sandbox())
        .build()

    payments_client = checkout_api.payments
    payments_client.refund_payment('payment_id')
```

### Default OAuth

The SDK supports client credentials OAuth, when initialized as follows:

```python
from checkout_sdk.checkout_sdk import CheckoutSdk
from checkout_sdk.environment import Environment
from checkout_sdk.oauth_scopes import OAuthScopes


def oauth():
    checkout_api = CheckoutSdk
        .builder()
        .oauth()
        .client_credentials(client_id='client_id', client_secret='client_secret')
        .environment(Environment.sandbox())
        .scopes([OAuthScopes.GATEWAY_PAYMENT_REFUNDS, OAuthScopes.FILES])
        .build()

    payments_client = checkout_api.payments
    payments_client.refund_payment('payment_id')
```

### Previous

If your pair of keys matches the Previous type, this is how the SDK should be used:

```python
from checkout_sdk.checkout_sdk import CheckoutSdk
from checkout_sdk.environment import Environment

def previous():
    # public key is optional, only required for operations related with tokens
    checkout_api = CheckoutSdk
        .builder()
        .previous()
        .secret_key('secret_key')
        .public_key('public_key')
        .environment(Environment.sandbox())
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
from checkout_sdk.checkout_sdk import CheckoutSdk
from checkout_sdk.environment import Environment
from checkout_sdk.oauth_scopes import OAuthScopes
from checkout_sdk.http_client_interface import HttpClientBuilderInterface


class CustomHttpClientBuilder(HttpClientBuilderInterface):

    def get_client(self) -> Session:
        session = requests.Session()
        session.max_redirects = 5
        return session


def oauth():
    checkout_api = CheckoutSdk
        .builder()
        .oauth()
        .client_credentials(client_id='client_id', client_secret='client_secret')
        .environment(Environment.sandbox())
        .http_client_builder(CustomHttpClientBuilder())
        .scopes([OAuthScopes.GATEWAY_PAYMENT_REFUNDS, OAuthScopes.FILES])
        .build()

    payments_client = checkout_api.payments
    payments_client.refund_payment('payment_id')
```

## Exception handling

All the API responses that do not fall in the 2** status codes will cause a `CheckoutApiException`. The exception encapsulates
the `http_metadata` and a dictionary of `error_details`, if available.

```python
try:
    checkout_api.customers.get("customer_id")
except CheckoutApiException as err:
    http_status_code = err.http_metadata.status_code
    error_details = err.error_details
```

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

* For Default account systems: `CHECKOUT_DEFAULT_PUBLIC_KEY` & `CHECKOUT_DEFAULT_SECRET_KEY`
* For OAuth account systems: `CHECKOUT_DEFAULT_OAUTH_CLIENT_ID` & `CHECKOUT_DEFAULT_OAUTH_CLIENT_SECRET`
* For Previous account systems: `CHECKOUT_PREVIOUS_PUBLIC_KEY` & `CHECKOUT_PREVIOUS_SECRET_KEY`

## Code of Conduct

Please refer to [Code of Conduct](CODE_OF_CONDUCT.md)

## Licensing

[MIT](LICENSE.md)
