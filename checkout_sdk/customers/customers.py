from checkout_sdk.common.common import Phone


class CustomerRequest:
    email: str
    name: str
    phone: Phone
    metadata: dict
    default: str
    instruments: list  # Not available on previous
