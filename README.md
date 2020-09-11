# Checkout.com Python SDK

[![Build Status](https://travis-ci.org/checkout/checkout-sdk-python.svg?branch=unified-payments)](https://travis-ci.org/checkout/checkout-sdk-python)
[![codecov](https://codecov.io/gh/checkout/checkout-sdk-python/branch/unified-payments/graph/badge.svg)](https://codecov.io/gh/checkout/checkout-sdk-python)

## Installation

    pip install checkout-sdk==2.0b8

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

**Important**
- If the `type` is not provided and cannot be inferred, a `ValueError` is thrown.
- All `type` values are accepted in the SDK and validated at API level.
- When using alternative payment methods (APMs), a `type` must be provided. See example below.

#### Source Type: `token`
A card token can be obtained using one of Checkout.com's JavaScript frontend solutions such as [Frames](https://docs.checkout.com/docs/frames "Frames") or any of the [mobile SDKs](https://docs.checkout.com/docs/sdks#section-mobile-sdk-libraries "Mobile SDKs")

``` python
try:
    payment = api.payments.request(
        source={
            'token': 'tok_...'.
            'billing_address': { ... },
            'phone': { ... }
        },
        amount=100,                                     # cents
        currency=sdk.Currency.USD,                      # or 'usd'
        reference='pay_ref'
    )
    print(payment.id)
except sdk.errors.CheckoutSdkError as e:
    print('{0.http_status} {0.error_type} {0.elapsed} {0.request_id}'.format(e))
```

#### Source Type: `id`

``` python
try:
    payment = api.payments.request(
        source={
            'id': 'src_...'
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

#### Source Type: `card`
[Fully PCI Compliant](https://docs.checkout.com/docs/pci-compliance) merchants only

``` python
try:
    payment = api.payments.request(
        source={
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

#### Source Type: `customer`

``` python
try:
    payment = api.payments.request(
        source={
            'id': 'cus_...'
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

#### Source Type: Alternative Payment Method (APM)

``` python
try:
    payment = api.payments.request(
        source={
            'type': 'ideal',
            'bic': 'INGBNL2A'                     # source-related attribute
            'description': 'test ideal description'
        },
        amount=100,                                     # cents
        currency=sdk.Currency.EUR,                      # or 'eur'
        reference='pay_apm_ref'
    )
    print(payment.is_pending)                           # True
    print(payment.requires_redirect)                    # True
    print(payment.redirect_link.href)                   # APM url
    print(payment.id)
    print(payment.http_response.body)                   # JSON body
except sdk.errors.CheckoutSdkError as e:
    print('{0.http_status} {0.error_type} {0.elapsed} {0.request_id}'.format(e))
```

### Payment Details

#### Get Payment

``` python
try:
    payment = api.payments.get('pay_...')
    print(payment.id)
except sdk.errors.CheckoutSdkError as e:
    print('{0.http_status} {0.error_type} {0.elapsed} {0.request_id}'.format(e))
```

#### Payment Actions

``` python
try:
    actions = api.payments.get_actions('pay_...')
    for action in actions:
        print(action.id)
        print(action.type)
        print(action.response_code)
        print(action.reference)
except sdk.errors.CheckoutSdkError as e:
    print('{0.http_status} {0.error_type} {0.elapsed} {0.request_id}'.format(e))
```

### Payment Flow

#### Capture, Void, Refund

``` python
try:
    action = api.payments.capture('pay_...', amount=100, reference='CAPTURE')
    # or ...
    action = api.payments.void('pay_...', reference='VOID')
    # or ...
    action = api.payments.refund('pay_...', amount=100, reference='REFUND')

    print(action.id)
    print(action.get_link('payment').href)
except sdk.errors.CheckoutSdkError as e:
    print('{0.http_status} {0.error_type} {0.elapsed} {0.request_id}'.format(e))
```

### 3DS Support

#### Payment Request Example

``` python
try:
    payment = api.payments.request(
        source={
            'number': '4242424242424242',
            'expiry_month': 6,
            'expiry_year': 2025,
            'cvv': '100'
        },
        amount=100,                                     # cents
        currency=sdk.Currency.USD,                      # or 'usd'
        reference='pay_ref'
        threeds=True                                    # shortcut for { 'enabled': True }
    )
    print(payment.is_pending)                           # True (always check this flag)
    print(payment.requires_redirect)                    # True
    print(payment.redirect_link.href)                   # ACS url
    print(payment.id)
    print(payment.http_response.body)                   # JSON body
except sdk.errors.CheckoutSdkError as e:
    print('{0.http_status} {0.error_code} {0.elapsed} {0.event_id} // {0.message}'.format(e))
```

> **Important**: If you use the Checkout.com Risk Engine to upgrade to a 3DS flow (from N3D) depending on criteria, you must always check for `payment.is_pending` first.

#### Payment Request Example With N3D Downgrade Option

``` python
try:
    payment = api.payments.request(
        source={
            'number': '4242424242424242',
            'expiry_month': 6,
            'expiry_year': 2025,
            'cvv': '100'
        },
        amount=100,                                     # cents
        currency=sdk.Currency.USD,                      # or 'usd'
        reference='pay_ref'
        threeds={
            'enabled': True,
            'attempt_n3d': True
        }
    )
    print(payment.is_pending)                           # False
    print(payment.3ds.downgraded)                       # True
    print(payment.id)
except sdk.errors.CheckoutSdkError as e:
    print('{0.http_status} {0.error_code} {0.elapsed} {0.event_id} // {0.message}'.format(e))
```

> **Important**: Value needs to be set to `5000` to simulate a `20153` response code on the Sandbox environment, which will then attempt an N3D charge.



### API Response

All API responses follow this format:

``` python
response = client.do_something(...)
# Request Id and API version
response.request_id
response.api_version
# HTTP response and attributes
response.http_response.status
response.http_response.headers
response.http_response.body                             # JSON body
response.http_response.elapsed
# HATEOAS
response.links
response.self_link
response.has_link(...)                                  # True | False
response.get_link(...)                                  # href and title
```

#### Payload Attributes

All attributes are dynamically mounted on the response as both class attributes and dictionary keys. Set the `sdk.default_response_immutable` default to `False` if you wish to be able to add your own attributes.

``` json
{
    "id": "pay",
    "source": {
        "type": "card",
        "number": "4242",
        "billing_address": {
            "city": "London"
        }
    },
    "_links": {
        "self": {
            "href": "http://url"
        }
    },
    "some_array": [
        {
            "key1": "value1"
        }
    ]
}
```

``` python
response = client.do_something(...)
response.id == 'pay'
response['id'] == 'pay'
response.source.type == 'card'
response['source']['type'] == 'card'
response.source.billing_address.city == 'London'
response.some_array[0].key1 == 'value1'
# if `sdk.default_response_immutable` is False
response.custom_attr1 = 'custom attribute 1'
response['custom_attr2'] = 999
```

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
