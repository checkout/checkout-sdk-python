from datetime import datetime

from checkout_sdk.common.common import CustomerRequest
from checkout_sdk.common.common_four import MarketplaceData
from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.payments import PaymentType, ShippingDetails, BillingInformation, PaymentRecipient, \
    ProcessingSettings, RiskRequest, ThreeDsRequest
from checkout_sdk.payments.payments_four import BillingDescriptor


class PaymentLinkRequest:
    payment_type: PaymentType.REGULAR
    amount: int
    currency: Currency
    payment_ip: str
    billing_descriptor: BillingDescriptor
    reference: str
    description: str
    expires_in: int
    customer: CustomerRequest
    shipping: ShippingDetails
    billing: BillingInformation
    recipient: PaymentRecipient
    processing: ProcessingSettings
    allow_payment_methods: list  # PaymentSourceType
    products: list  # Product
    metadata: dict
    three_ds: ThreeDsRequest
    risk: RiskRequest
    return_url: str
    locale: str
    capture: bool
    capture_on: datetime
    # Only available in Four
    processing_channel_id: str
    marketplace: MarketplaceData
