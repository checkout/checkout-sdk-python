# Checkout.com Python SDK

[![Build Status](https://travis-ci.org/checkout/checkout-sdk-python.svg?branch=dev-unified-payments)](https://travis-ci.org/checkout/checkout-sdk-python)
[![codecov](https://codecov.io/gh/checkout/checkout-sdk-python/branch/dev-unified-payments/graph/badge.svg)](https://codecov.io/gh/checkout/checkout-sdk-python)

## Installation

    pip install checkout-sdk==2.0b3

From source:

    python setup.py install

### Requirements

* Python 3.4+
* Pypy 3

## Usage

### Using environment variables

``` python
os.environ['CKO_SECRET_KEY'] = '<your secret key>'
os.environ['CKO_SANDBOX'] = 'True|true|1'               # else is False (Production)
os.environ['CKO_LOGGING'] = 'debug|DEBUG|info|INFO'

# ...

import checkout_sdk as sdk

api = sdk.get_api()
```

### Using initialisation values

``` python
import checkout_sdk as sdk

api = sdk.get_api(secret_key='<your secret key>')       # default sandbox = True
```

### Setting defaults

``` python
sdk.default_currency = sdk.Currency.EUR
sdk.default_capture = True
sdk.default_payment_type = sdk.PaymentType.Regular
sdk.default_response_immutable = True
```

### Payment Request

The SDK will infer the `type` of the payment `source`, if not provided, as follows:
- `type: "card"` if `number` attribute present.
- `type: "customer"` if `email` attribute present or `id` attribute present and prefix is `cus_`.
- `type: "token"` if `token` attribute present.
- `type: "id"` if `id` attribute present and prefix is `src_`.

#### Source type: `card`

``` python
try:
    payment = api.payments.request(
        source = {
            'number': '4242424242424242',
            'expiry_month': 6,
            'expiry_year': 2025,
            'cvv': '100'
        },
        amount=100,                                     # cents
        currency=sdk.Currency.USD,                      # or 'usd'
        reference='pay_ref'
    )
    print(payment.id)
    print(payment.is_pending)                           # False
    print(payment.http_response.body)                   # JSON body
except sdk.errors.CheckoutSdkError as e:
    print('{0.http_status} {0.error_type} {0.elapsed} {0.request_id}'.format(e))
```

#### Source type: `id`

``` python
try:
    payment = api.payments.request(
        source = {
            'id': 'src_656buhl3fmbuvj27b3jz3ijfyt'
            'cvv': '100'                                # source-related attribute
        },
        amount=100,                                     # cents
        currency=sdk.Currency.USD,                      # or 'usd'
        reference='pay_ref'
    )
    print(payment.id)
except sdk.errors.CheckoutSdkError as e:
    print('{0.http_status} {0.error_type} {0.elapsed} {0.request_id}'.format(e))
```

#### Source type: `customer`

``` python
try:
    payment = api.payments.request(
        source = {
            'id': 'cus_700buhl4hnbuvj27b3jz3ijzzz'
            # or ...
            'email': 'user@checkout.com'
        },
        amount=100,                                     # cents
        currency=sdk.Currency.USD,                      # or 'usd'
        reference='pay_ref'
    )
    print(payment.id)
except sdk.errors.CheckoutSdkError as e:
    print('{0.http_status} {0.error_type} {0.elapsed} {0.request_id}'.format(e))
```

####

### Exception handling

``` python
class CheckoutSdkError(Exception):                      # catch all
class AuthenticationError(CheckoutSdkError):            # 401
class NotAllowedError(CheckoutSdkError):                # 403
class ResourceNotFoundError(CheckoutSdkError):          # 404
class ValidationError(CheckoutSdkError):                # 422
class TooManyRequestsError(CheckoutSdkError):           # 429
class ApiTimeout(CheckoutSdkError):
class ApiError(CheckoutSdkError):                       # 500 / fallback
```

> The SDK will not do any offline business validations. Provided the values and types are correct, all business validations are handled at API level. `ValueError` and `TypeError` are thrown for incorrect usage.

### Logging

```python
os.environ['CKO_LOGGING'] = 'debug|DEBUG|info|INFO'
```

or ...

```python
import logging
logging.getLogger('cko').setLevel(logging.DEBUG)
```

### Test Suite

The tests currently need a Sandbox account. This will eventually be replaced by the incoming Checkout.com Mock API.

```
export CKO_SECRET_KEY="<your secret key>"
export CKO_LOGGING="info|debug"
python setup.py test
```