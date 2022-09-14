from datetime import datetime

from checkout_sdk.common.common import CustomerRequest
from checkout_sdk.common.common import MarketplaceData
from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.payments import BillingDescriptor, PaymentType, ShippingDetails, ThreeDsRequest, \
    RiskRequest, PaymentRecipient, ProcessingSettings
from checkout_sdk.payments.payments_previous import BillingInformation


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
    products: list  # common.Product
    metadata: dict
    three_ds: ThreeDsRequest
    risk: RiskRequest
    return_url: str
    locale: str
    capture: bool
    capture_on: datetime
    processing_channel_id: str
    # @deprecated marketplace property will be removed in the future, and should be used amount_allocations instead
    marketplace: MarketplaceData
    amount_allocations: list  # values of AmountAllocations
