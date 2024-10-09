from datetime import datetime

from checkout_sdk.common.common import CustomerRequest, CustomerRetry
from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.payments import BillingDescriptor, PaymentType, ShippingDetails, ThreeDsRequest, \
    RiskRequest, PaymentRecipient, ProcessingSettings, PaymentSender
from checkout_sdk.payments.payments_previous import BillingInformation


class PaymentLinkRequest:
    amount: int
    currency: Currency
    payment_type: PaymentType.REGULAR
    payment_ip: str
    billing_descriptor: BillingDescriptor
    reference: str
    description: str
    display_name: str
    processing_channel_id: str
    amount_allocations: list  # values of AmountAllocations
    expires_in: int
    customer: CustomerRequest
    shipping: ShippingDetails
    billing: BillingInformation
    recipient: PaymentRecipient
    processing: ProcessingSettings
    allow_payment_methods: list  # PaymentSourceType
    disabled_payment_methods: list  # PaymentSourceType
    products: list  # common.Product
    metadata: dict
    three_ds: ThreeDsRequest
    risk: RiskRequest
    customer_retry: CustomerRetry
    sender: PaymentSender
    return_url: str
    locale: str
    capture: bool
    capture_on: datetime
