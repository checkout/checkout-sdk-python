from __future__ import absolute_import
from datetime import datetime
from enum import Enum

from checkout_sdk.common.common import Address, Phone, CustomerRequest, Product
from checkout_sdk.common.enums import Currency, Country
from checkout_sdk.payments.payments import PaymentType


# Enums
class PaymentMethodInitialization(str, Enum):
    DISABLED = 'disabled'
    ENABLED = 'enabled'


# Customer entities
class CustomerEmail:
    def __init__(self):
        self.address: str = None
        self.verified: bool = None


class CustomerDevice:
    def __init__(self):
        self.locale: str = None


class MerchantAccount:
    def __init__(self):
        self.id: str = None
        self.registration_date: datetime = None
        self.last_modified: datetime = None
        self.returning_customer: bool = None
        self.first_transaction_date: datetime = None
        self.last_transaction_date: datetime = None
        self.total_order_count: int = None
        self.last_payment_amount: int = None  # Using int for consistency with amount fields


class Customer:
    def __init__(self):
        self.email: CustomerEmail = None
        self.name: str = None
        self.phone: Phone = None
        self.device: CustomerDevice = None
        self.merchant_account: MerchantAccount = None


# Payment Method Common entities
class PaymentMethodAction:
    def __init__(self):
        self.type: str = None
        self.client_token: str = None
        self.session_id: str = None


class PaymentMethodOption:
    def __init__(self):
        self.id: str = None
        self.status: str = None
        self.flags: list = None  # list of str
        self.action: PaymentMethodAction = None


class PaymentMethodOptions:
    def __init__(self):
        self.sdk: PaymentMethodOption = None
        self.pay_in_full: PaymentMethodOption = None
        self.installments: PaymentMethodOption = None
        self.pay_now: PaymentMethodOption = None


class PaymentMethodBase:
    def __init__(self):
        self.status: str = None
        self.flags: list = None  # list of str
        self.initialization: PaymentMethodInitialization = PaymentMethodInitialization.DISABLED


# Klarna entities
class KlarnaAccountHolder:
    def __init__(self):
        self.billing_address: Address = None


class Klarna(PaymentMethodBase):
    def __init__(self):
        super().__init__()
        self.account_holder: KlarnaAccountHolder = None
        self.payment_method_options: PaymentMethodOptions = None


# Stcpay entities
class Stcpay(PaymentMethodBase):
    def __init__(self):
        super().__init__()
        self.otp: str = None
        self.payment_method_options: PaymentMethodOptions = None


# Tabby entities
class Tabby(PaymentMethodBase):
    def __init__(self):
        super().__init__()
        self.payment_method_options: PaymentMethodOptions = None


# Bizum entities
class Bizum(PaymentMethodBase):
    def __init__(self):
        super().__init__()
        self.payment_method_options: PaymentMethodOptions = None


class PaymentMethods:
    def __init__(self):
        self.klarna: Klarna = None
        self.stcpay: Stcpay = None
        self.tabby: Tabby = None
        self.bizum: Bizum = None


# Settings entity
class Settings:
    def __init__(self):
        self.success_url: str = None
        self.failure_url: str = None


# Order entities
class OrderSubMerchant:
    def __init__(self):
        self.id: str = None
        self.product_category: str = None
        self.number_of_trades: int = None
        self.registration_date: datetime = None


class Order:
    def __init__(self):
        self.items: list = None  # list of PaymentContextsItems (reused from contexts)
        self.shipping = None  # ShippingDetails (reused from common)
        self.sub_merchants: list = None  # list of OrderSubMerchant
        self.discount_amount: int = None


# Industry entities (reusing from contexts where possible)
class AirlineData:
    def __init__(self):
        self.ticket = None  # PaymentContextsTicket (reused from contexts)
        self.passengers: list = None  # list of PaymentContextsPassenger (reused from contexts)
        self.flight_leg_details: list = None  # list of PaymentContextsFlightLegDetails (reused from contexts)


class Industry:
    def __init__(self):
        self.airline_data: AirlineData = None
        self.accommodation_data: list = None  # list of AccommodationData (reused from contexts)


# Main Request and Response classes
class PaymentSetupsRequest:
    def __init__(self):
        self.processing_channel_id: str = None
        self.amount: int = None
        self.currency: Currency = None
        self.payment_type: PaymentType = None
        self.reference: str = None
        self.description: str = None
        self.payment_methods: PaymentMethods = None
        self.settings: Settings = None
        self.customer: Customer = None
        self.order: Order = None
        self.industry: Industry = None


class PaymentSetupsResponse:
    def __init__(self):
        self.id: str = None
        self.processing_channel_id: str = None
        self.amount: int = None
        self.currency: Currency = None
        self.payment_type: PaymentType = None
        self.reference: str = None
        self.description: str = None
        self.payment_methods: PaymentMethods = None
        self.settings: Settings = None
        self.customer: Customer = None
        self.order: Order = None
        self.industry: Industry = None


# Customer Response for Confirm
class CustomerResponse:
    id: str = None
    email: str = None
    name: str = None
    phone: Phone = None


# Source for Confirm Response
class PaymentSetupSource:
    type: str = None
    id: str = None
    billing_address: Address = None
    phone: Phone = None
    scheme: str = None
    last4: str = None
    fingerprint: str = None
    bin: str = None
    card_type: str = None
    card_category: str = None
    issuer: str = None
    issuer_country: Country = None
    product_type: str = None
    avs_check: str = None
    cvv_check: str = None
    payment_account_reference: str = None


# Nested classes for Confirm Response (reusing from payments)
class Risk:
    flagged: bool = None


class ThreeDs:
    downgraded: bool = None
    enrolled: str = None


class Processing:
    retrieval_reference_number: str = None
    acquirer_transaction_id: str = None
    recommendation_code: str = None
    partner_order_id: str = None


# Confirm Response
class PaymentSetupsConfirmResponse:
    def __init__(self):
        self.id: str = None
        self.action_id: str = None
        self.amount: int = None
        self.currency: Currency = None
        self.approved: bool = None
        self.status: str = None
        self.auth_code: str = None
        self.response_code: str = None
        self.response_summary: str = None
        self.threeds: ThreeDs = None  # Note: using 'threeds' as per JSON, not '3ds'
        self.risk: Risk = None
        self.source: PaymentSetupSource = None
        self.customer: CustomerResponse = None
        self.processed_on: datetime = None
        self.reference: str = None
        self.processing: Processing = None
        self.eci: str = None
        self.scheme_id: str = None
        self._links: dict = None