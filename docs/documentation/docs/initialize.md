---
id: initialize
title: Initialize
---

## Initialisation 
You can initialise the sdk api either by initialisation values or with environment variables:

### Using initialisation values

To start making API requests you need to create an instance of `sdk.get_api` providing your Checkout.com secret API key:

```jsx
api = sdk.get_api(secret_key='sk_07fa5e52-3971-4bab-ae6b-a8e26007fccc')
```
The second parameter determines whether the SDK will use our Sandbox API (default) or Production. For testing purposes you should use Sandbox.
```jsx
api = sdk.get_api(secret_key='sk_07fa5e52-3971-4bab-ae6b-a8e26007fccc', false) // for live
```

### Using environment variables

``` python
os.environ['CKO_SECRET_KEY'] = '<your secret key>'
os.environ['CKO_SANDBOX'] = 'True|true|1'               # else is False (Production)
os.environ['CKO_LOGGING'] = 'debug|DEBUG|info|INFO'

# ...

import checkout_sdk as sdk

api = sdk.get_api()
```


`sdk.get_api()` provides access to each of our API resources, for example:

```jsx
payment = api.payments.request(...)
``` 

## General Usage

To make the SDK as intuitive as possible, we have made each API operation to be called by a function with the same name in the api:

```jsx
void_action = api.payments.void(...);
refund_action = api.payments.refund(...);
...
```

For detailed examples, please see [[API Resources]].