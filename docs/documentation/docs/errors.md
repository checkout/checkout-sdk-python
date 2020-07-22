---
id: errors
title: Error Handling
---

## Exception handling

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

## How errors are determined

The errors above are triggered by status codes that do not fall in the 20X Status codes, or by validation issues. This means that statuses like a 202, 204 will not throw an exception

:::tip

It's important to understand that Declines or 3D Secure responses do not throw an exception since the status code associated with them is in the 20X range. In the Payments section you will see some examples of best practices when it comes to handling responses.

:::
