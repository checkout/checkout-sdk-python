# Checkout.com Python SDK

[![Build Status](https://travis-ci.org/checkout/checkout-sdk-python.svg?branch=master)](https://travis-ci.org/checkout/checkout-sdk-python)
[![codecov](https://codecov.io/gh/checkout/checkout-sdk-python/branch/master/graph/badge.svg)](https://codecov.io/gh/checkout/checkout-sdk-python)

## Installation

    pip install --upgrade checkout-sdk

From source:

    python setup.py install

### Requirements

* Python 3.4+

## Usage

### Using environment variables

``` python
os.environ['CKO_SECRET_KEY'] = '<your secret key>'
os.environ['CKO_SANDBOX'] = 'True|true|1' # else is False (Production)
os.environ['CKO_LOGGING'] = 'debug|DEBUG|info|INFO'

# ...

import checkout_sdk as sdk

api = sdk.get_api()
```

### Using initialisation values

``` python
import checkout_sdk as sdk

api = sdk.get_api(secret_key='<your secret key>') # default sandbox = True
```

### Setting defaults

``` python
sdk.default_currency = sdk.Currency.EUR
sdk.default_auto_capture = True
sdk.default_auto_capture_delay = 0  # valid: 0 - 168 (hours)
sdk.default_payment_type = PaymentType.Regular
```

### Payment Request

#### Full Card

``` python
try:
    payment = api.payments.request(
        card = {
            'number': '4242424242424242',
            'expiryMonth': 6,
            'expiry_year': 2025, # snake_case is automatically converted
            'cvv': '100'
        },
        value=100, # cents
        currency=sdk.Currency.USD, # or 'usd'
        customer='customer@email.com'
    )
    print(payment.id)
    print(payment.card.id)
    print(payment.customer.id)
    print(payment.http_response.body) # JSON body
except sdk.errors.CheckoutSdkError as e:
    print('{0.http_status} {0.error_code} {0.elapsed} {0.event_id} // {0.message}'.format(e))
```

#### Card Id

``` python
try:
    payment = api.payments.request(
        card = 'card_713A3978-AFB2-4D30-BF9A-BA55714DC309',
        value=100, # cents
        currency=sdk.Currency.USD, # or 'usd'
        customer='customer@email.com'
    )
    if payment.approved:
        # ...
except sdk.errors.CheckoutSdkError as e:
    print('{0.http_status} {0.error_code} {0.elapsed} {0.event_id} // {0.message}'.format(e))
```

### Exception handling

``` python
class CheckoutSdkError(Exception):             # catch all
class AuthenticationError(CheckoutSdkError):   # 401
class BadRequestError(CheckoutSdkError):       # 400
class ResourceNotFoundError(CheckoutSdkError): # 404
class Timeout(CheckoutSdkError):
class TooManyRequestsError(CheckoutSdkError):  # 422
class ApiError(CheckoutSdkError):              # 500 / fallback
```

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