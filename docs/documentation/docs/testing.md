---
id: testing
title: Testing
---


## Testing

### Sandbox
The tests currently need a Sandbox account. This will eventually be replaced by the incoming Checkout.com Mock API.

```
export CKO_SECRET_KEY="<your secret key>"
export CKO_LOGGING="info|debug"
python setup.py test
```

### Testing Cards

If you are testing in the Sandbox environment, Checkout.com provides a list of [test test card details](https://docs.checkout.com/docs/testing#section-test-card-numbers). You can also simulate a lot of edge cases like Declines, by using [special transaction values](https://docs.checkout.com/docs/testing#section-response-codes).

:::note

You can also test 3D Secure with the test cards provided. If you want to test 3DS 2 flows, use the cards mentioned [here](https://docs.checkout.com/docs/testing#section-3-ds-test-cards).

:::
