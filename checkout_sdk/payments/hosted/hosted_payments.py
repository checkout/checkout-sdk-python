from datetime import datetime

from checkout_sdk.common.common import CustomerRequest
from checkout_sdk.common.common import MarketplaceData
from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.payments_previous import BillingInformation
from checkout_sdk.payments.payments import BillingDescriptor, PaymentType, ShippingDetails, ThreeDsRequest, \
    RiskRequest, PaymentRecipient, ProcessingSettings


class HostedPaymentsSessionRequest:
    payment_type: PaymentType.REGULAR
    amount: int
    currency: Currency
    payment_ip: str
    billing_descriptor: BillingDescriptor
    reference: str
    description: str
    customer: CustomerRequest
    shipping: ShippingDetails
    billing: BillingInformation
    recipient: PaymentRecipient
    processing: ProcessingSettings
    allow_payment_methods: list  # PaymentSourceType
    products: list  # common.Product
    risk: RiskRequest
    success_url: str
    cancel_url: str
    failure_url: str
    metadata: dict
    locale: str
    three_ds: ThreeDsRequest
    capture: bool
    capture_on: datetime
    # Not available on Previous
    processing_channel_id: str
    marketplace: MarketplaceData
