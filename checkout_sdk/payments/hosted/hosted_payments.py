from datetime import datetime

from checkout_sdk.common.common import CustomerRequest, CustomerRetry
from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.payments import BillingDescriptor, PaymentType, ShippingDetails, ThreeDsRequest, \
    RiskRequest, PaymentRecipient, ProcessingSettings, PaymentSender
from checkout_sdk.payments.payments_previous import BillingInformation


class HostedPaymentsSessionRequest:
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
    customer: CustomerRequest
    shipping: ShippingDetails
    billing: BillingInformation
    recipient: PaymentRecipient
    processing: ProcessingSettings
    allow_payment_methods: list  # PaymentSourceType
    disabled_payment_methods: list  # PaymentSourceType
    products: list  # common.Product
    risk: RiskRequest
    customer_retry: CustomerRetry
    sender: PaymentSender
    success_url: str
    cancel_url: str
    failure_url: str
    metadata: dict
    locale: str
    three_ds: ThreeDsRequest
    capture: bool
    capture_on: datetime
