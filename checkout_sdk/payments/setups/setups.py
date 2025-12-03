from __future__ import absolute_import
from datetime import datetime
from enum import Enum

from checkout_sdk.common.common import Address, Phone, CustomerRetry
from checkout_sdk.common.enums import Currency, Country
from checkout_sdk.payments.payments import PaymentType, ShippingDetails
from checkout_sdk.payments.contexts.contexts import PaymentContextsItems, PaymentContextsTicket, PaymentContextsPassenger, PaymentContextsFlightLegDetails


# Enums
class PaymentMethodInitialization(str, Enum):
    DISABLED = 'disabled'
    ENABLED = 'enabled'


class PaymentMethodStatus(str, Enum):
    """Payment method status for responses"""
    AVAILABLE = 'available'
    REQUIRES_ACTION = 'requires_action'
    UNAVAILABLE = 'unavailable'


class PaymentMethodOptionStatus(str, Enum):
    """Payment method option status for responses"""
    UNAVAILABLE = 'unavailable'
    ACTION_REQUIRED = 'action_required'
    PENDING = 'pending'
    READY = 'ready'


class PaymentStatus(str, Enum):
    """Payment status for confirm responses"""
    AUTHORIZED = 'Authorized'
    PENDING = 'Pending'
    CARD_VERIFIED = 'Card Verified'
    DECLINED = 'Declined'
    RETRY_SCHEDULED = 'Retry Scheduled'


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
        self.status: PaymentMethodOptionStatus = None  # Enum: unavailable, action_required, pending, ready (for responses)
        self.flags: list = None  # list of str - error codes or indicators that highlight missing/invalid info
        self.action: PaymentMethodAction = None


class PaymentMethodOptions:
    def __init__(self):
        self.sdk: PaymentMethodOption = None
        self.pay_in_full: PaymentMethodOption = None
        self.installments: PaymentMethodOption = None
        self.pay_now: PaymentMethodOption = None


class PaymentMethodBase:
    def __init__(self):
        self.status: PaymentMethodStatus = None  # Enum: available, requires_action, unavailable (for responses)
        self.flags: list = None  # list of str - error codes or indicators
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
    def __init__(self):
        self.id: str = None
        self.email: str = None
        self.name: str = None
        self.phone: Phone = None
        self.summary = None  # Customer summary object for risk assessment


# Source for Confirm Response
class PaymentSetupSource:
    def __init__(self):
        self.type: str = None
        self.id: str = None
        self.expiry_month: int = None
        self.expiry_year: int = None
        self.last4: str = None
        self.fingerprint: str = None
        self.bin: str = None
        self.billing_address: Address = None
        self.phone: Phone = None
        self.name: str = None
        self.scheme: str = None
        self.scheme_local: str = None
        self.local_schemes: list = None  # list of str
        self.card_type: str = None
        self.card_category: str = None
        self.card_wallet_type: str = None
        self.issuer: str = None
        self.issuer_country: Country = None
        self.product_id: str = None
        self.product_type: str = None
        self.avs_check: str = None
        self.cvv_check: str = None
        self.payment_account_reference: str = None
        self.encrypted_card_number: str = None
        self.account_update_status: str = None
        self.account_update_failure_code: str = None
        self.account_holder = None  # Can be various types based on account holder type


# Nested classes for Confirm Response (reusing from payments)
class Risk:
    def __init__(self):
        self.flagged: bool = None
        self.score: int = None


class ThreeDs:
    def __init__(self):
        self.downgraded: bool = None
        self.enrolled: str = None
        self.upgrade_reason: str = None


class Processing:
    def __init__(self):
        self.retrieval_reference_number: str = None
        self.acquirer_transaction_id: str = None
        self.recommendation_code: str = None
        self.scheme: str = None  # The scheme the transaction was processed with
        self.partner_merchant_advice_code: str = None
        self.partner_response_code: str = None
        self.partner_order_id: str = None
        self.partner_payment_id: str = None
        self.partner_status: str = None
        self.partner_transaction_id: str = None
        self.partner_error_codes: list = None  # list of str
        self.partner_error_message: str = None
        self.partner_authorization_code: str = None
        self.partner_authorization_response_code: str = None
        self.surcharge_amount: int = None
        self.pan_type_processed: str = None
        self.cko_network_token_available: bool = None
        self.purchase_country: str = None
        self.foreign_retailer_amount: int = None


# Additional classes for Confirm Response (reusing from common)
class Balances:
    def __init__(self):
        self.total_authorized: int = None
        self.total_voided: int = None
        self.available_to_void: int = None
        self.total_captured: int = None
        self.available_to_capture: int = None
        self.total_refunded: int = None
        self.available_to_refund: int = None


class Subscription:
    def __init__(self):
        self.id: str = None


class Retry(CustomerRetry):
    def __init__(self):
        super().__init__()
        self.ends_on: datetime = None
        self.next_attempt_on: datetime = None


# Confirm Response
class PaymentSetupsConfirmResponse:
    def __init__(self):
        self.id: str = None
        self.action_id: str = None
        self.amount: int = None
        self.currency: Currency = None
        self.approved: bool = None
        self.status: str = None
        self.response_code: str = None
        self.processed_on: datetime = None
        self.amount_requested: int = None
        self.auth_code: str = None
        self.response_summary: str = None
        self.expires_on: str = None
        self.threeds: ThreeDs = None
        self.risk: Risk = None
        self.source: PaymentSetupSource = None
        self.customer: CustomerResponse = None
        self.balances: Balances = None
        self.reference: str = None
        self.subscription: Subscription = None
        self.processing: Processing = None
        self.eci: str = None
        self.scheme_id: str = None
        self.retry: Retry = None
        
    @property
    def threeds_3ds(self):
        """API spec uses '3ds' as field name - this provides compatibility"""
        return self.threeds
        
    @threeds_3ds.setter
    def threeds_3ds(self, value):
        self.threeds = value