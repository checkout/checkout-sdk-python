# Checkout.com Python SDK

## Installation

From source:

    python setup.py install

### Requirements

* Python 3.5+

## Usage

### Using environment variables

``` python

os.environ['CKO_SECRET_KEY'] = '<your secret key>'
os.environ['CKO_SANDBOX'] = 'True|true|1' # else is False (Production)

# ...

import checkout_sdk as sdk

api = sdk.get_api()

```

### Using initialisation values

``` python

import checkout_sdk as sdk

api = sdk.get_api(secret_key='sk_test_be994177-4711-44a6-b719-fceb82bde8c4') # default sandbox = True

```

### Payment Request

#### Full Card

``` python
try:
    response = api.Payments.request(
        card = {
            'number': '4242424242424242',
            'expiryMonth': 6,
            'expiryYear': 2018,
            'cvv': '100'
        },
        amount=100, # cents
        currency=sdk.Currency.USD, # or 'usd'
        email='customer@email.com'
    )
    print(response) # status, elapsed ms
    print(response.json) # JSON body
except sdk.errors.CheckoutSdkError as e:
    print('{0.http_status} {0.error_code} {0.elapsed} {0.event_id} // {0.message}'.format(e))

```

#### Card Id

``` python
try:
    response = api.Payments.request(
        card = 'card_713A3978-AFB2-4D30-BF9A-BA55714DC309',
        amount=100, # cents
        currency=sdk.Currency.USD, # or 'usd'
        email='customer@email.com'
    )
    print(response) # status, elapsed ms
    print(response.json) # JSON body
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
class APIError(CheckoutSdkError):              # 500 / fallback

```