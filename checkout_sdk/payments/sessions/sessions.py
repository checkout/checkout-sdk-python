from datetime import datetime
from enum import Enum

from checkout_sdk.common.common import Address, CustomerRequest
from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.payments import PaymentType, BillingDescriptor, PaymentCustomerRequest, ShippingDetails, \
    PaymentRecipient, ProcessingSettings, RiskRequest, PaymentRetryRequest, ThreeDsRequest, PaymentSender
from checkout_sdk.payments.payments_previous import BillingInformation


class PaymentMethodsType(str, Enum):
    APPLEPAY = 'applepay'
    BANCONTACT = 'bancontact'
    CARD = 'card'
    EPS = 'eps'
    GIROPAY = 'giropay'
    GOOGLEPAY = 'googlepay'
    IDEAL = 'ideal'
    KNET = 'knet'
    MULTIBANCO = 'multibanco'
    PRZELEWY24 = 'p24'
    PAYPAL = 'paypal'
    SOFORT = 'sofort'


class StorePaymentDetails(str, Enum):
    DISABLED = 'disabled'
    ENABLED = 'enabled'


class Billing:
    address: Address


class Card:
    store_payment_details: StorePaymentDetails


class PaymentMethodConfiguration:
    card: Card


class PaymentSessionsRequest:
    amount: int
    currency: Currency
    payment_type: PaymentType
    billing: BillingInformation
    billing_descriptor: BillingDescriptor
    reference: str
    description: str
    customer: PaymentCustomerRequest
    customer: CustomerRequest
    shipping: ShippingDetails
    recipient: PaymentRecipient
    processing: ProcessingSettings
    processing_channel_id: str
    expires_on: datetime
    payment_method_configuration: PaymentMethodConfiguration
    enabled_payment_methods: list  # PaymentMethodsType
    disabled_payment_methods: list  # PaymentMethodsType
    items: list  # payments.Product
    amount_allocations: list  # values of AmountAllocations
    risk: RiskRequest
    customer_retry: PaymentRetryRequest
    display_name: str
    success_url: str
    failure_url: str
    metadata: dict
    locale: str
    three_ds: ThreeDsRequest
    sender: PaymentSender
    capture: bool
    ip_address: str
