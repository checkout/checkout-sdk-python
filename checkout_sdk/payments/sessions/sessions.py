from checkout_sdk.common.common import Address, CustomerRequest
from checkout_sdk.common.enums import Currency


class Billing:
    address: Address


class PaymentSessionsRequest:
    amount: int
    currency: Currency
    reference: str
    billing: Billing
    customer: CustomerRequest
    success_url: str
    failure_url: str
