from __future__ import absolute_import
from datetime import datetime
from enum import Enum

from checkout_sdk.common.common import Address, Phone
from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.contexts.contexts import PaymentContextsTicket
from checkout_sdk.payments.payments import PaymentType, ShippingDetails


# Enums
class PaymentMethodInitialization(str, Enum):
    DISABLED = 'disabled'
    ENABLED = 'enabled'


# Customer entities
class CustomerEmail:
    address: str
    verified: bool


class CustomerDevice:
    locale: str


class MerchantAccount:
    id: str
    registration_date: datetime
    last_modified: datetime
    returning_customer: bool
    first_transaction_date: datetime
    last_transaction_date: datetime
    total_order_count: int
    last_payment_amount: int


class Customer:
    email: CustomerEmail
    name: str
    phone: Phone
    device: CustomerDevice
    merchant_account: MerchantAccount
    country: str
    id: str
    tax_number: str


# Payment Method Common entities
class PaymentMethodAction:
    type: str
    client_token: str
    session_id: str
    order_id: str


class PaymentMethodOption:
    id: str
    flags: list  # list of str
    action: PaymentMethodAction


class PaymentMethodOptions:
    sdk: PaymentMethodOption
    pay_in_full: PaymentMethodOption
    installments: PaymentMethodOption
    pay_now: PaymentMethodOption


class PaymentMethodBase:
    status: str
    flags: list  # list of str
    initialization: PaymentMethodInitialization = PaymentMethodInitialization.DISABLED


# Klarna entities
class KlarnaAccountHolder:
    billing_address: Address


class Klarna(PaymentMethodBase):
    def __init__(self):
        super().__init__()
        self.account_holder: KlarnaAccountHolder
        self.payment_method_options: PaymentMethodOptions


# Stcpay entities
class Stcpay(PaymentMethodBase):
    def __init__(self):
        super().__init__()
        self.otp: str
        self.payment_method_options: PaymentMethodOptions


# Tabby entities
class Tabby(PaymentMethodBase):
    payment_types: list  # list of str

    def __init__(self):
        super().__init__()
        self.payment_method_options: PaymentMethodOptions


# Bizum entities
class Bizum(PaymentMethodBase):
    def __init__(self):
        super().__init__()
        self.payment_method_options: PaymentMethodOptions


class Blik(PaymentMethodBase):
    partner_code: str


class PaypalUserAction(str, Enum):
    PAY_NOW = 'pay_now'
    CONTINUE = 'continue'


class PaypalShippingPreference(str, Enum):
    NO_SHIPPING = 'no_shipping'
    GET_FROM_FILE = 'get_from_file'
    SET_PROVIDED_ADDRESS = 'set_provided_address'


class Paypal(PaymentMethodBase):
    user_action: PaypalUserAction
    brand_name: str
    shipping_preference: PaypalShippingPreference
    action: PaymentMethodAction


# Base for payment methods that only expose status/flags (swagger PaymentSetupPaymentMethod).
# Distinct from PaymentMethodBase, which also carries the writable `initialization` field
# supported only by klarna, stcpay, tabby and paypal.
class PaymentSetupPaymentMethod:
    status: str
    flags: list  # list of str


# Shared payment-method enums
class TerminalType(str, Enum):
    WEB = 'web'
    WAP = 'wap'
    APP = 'app'


class OsType(str, Enum):
    ANDROID = 'android'
    IOS = 'ios'


class KnetLanguage(str, Enum):
    EN = 'en'
    AR = 'ar'


class PaymentSetupAccountHolderType(str, Enum):
    INDIVIDUAL = 'individual'
    CORPORATE = 'corporate'
    GOVERNMENT = 'government'


# Account holder shared by card, wallet and instrument methods
class PaymentSetupAccountHolder:
    type: PaymentSetupAccountHolderType
    first_name: str
    last_name: str
    middle_name: str
    company_name: str
    account_name_inquiry: bool


# Instrument entities
class PaymentSetupInstrument(PaymentSetupPaymentMethod):
    id: str
    phone: Phone
    account_holder: PaymentSetupAccountHolder
    allow_update: bool
    action: PaymentMethodAction


# Status/flags-only methods
class PayNow(PaymentSetupPaymentMethod):
    pass


class Eps(PaymentSetupPaymentMethod):
    pass


class Benefit(PaymentSetupPaymentMethod):
    pass


class Vipps(PaymentSetupPaymentMethod):
    pass


class Twint(PaymentSetupPaymentMethod):
    pass


class MobilePay(PaymentSetupPaymentMethod):
    pass


class Tamara(PaymentSetupPaymentMethod):
    pass


class MBWay(PaymentSetupPaymentMethod):
    pass


class WeChatPay(PaymentSetupPaymentMethod):
    pass


class Octopus(PaymentSetupPaymentMethod):
    pass


class Alma(PaymentSetupPaymentMethod):
    pass


class Sequra(PaymentSetupPaymentMethod):
    pass


# Wallets that share terminal_type/os_type configuration
class TerminalPaymentMethod(PaymentSetupPaymentMethod):
    terminal_type: TerminalType
    os_type: OsType


class AlipayCn(TerminalPaymentMethod):
    pass


class AlipayHK(TerminalPaymentMethod):
    pass


class GCash(TerminalPaymentMethod):
    pass


class Tng(TerminalPaymentMethod):
    pass


class Dana(TerminalPaymentMethod):
    pass


class KakaoPay(TerminalPaymentMethod):
    pass


class TrueMoney(TerminalPaymentMethod):
    pass


# Methods with specific fields
class Qpay(PaymentSetupPaymentMethod):
    national_id: str
    description: str


class Ideal(PaymentSetupPaymentMethod):
    description: str


class Knet(PaymentSetupPaymentMethod):
    language: KnetLanguage


class Bancontact(PaymentSetupPaymentMethod):
    account_holder_name: str


class Multibanco(PaymentSetupPaymentMethod):
    account_holder_name: str


class P24AccountHolder:
    name: str
    email: str


class P24(PaymentSetupPaymentMethod):
    account_holder: P24AccountHolder


class SwishAccountHolder:
    first_name: str
    last_name: str


class Swish(PaymentSetupPaymentMethod):
    billing_descriptor: str
    account_holder: SwishAccountHolder


# ACH entities
class AchAccountType(str, Enum):
    SAVINGS = 'savings'
    CURRENT = 'current'
    CASH = 'cash'


class AchAccountHolderIdentification:
    type: str
    issuing_country: str
    number: str


class AchAccountHolder:
    type: PaymentSetupAccountHolderType
    first_name: str
    last_name: str
    company_name: str
    date_of_birth: str
    identification: AchAccountHolderIdentification


class Ach(PaymentSetupPaymentMethod):
    account_type: AchAccountType
    account_holder: AchAccountHolder
    account_number: str
    bank_code: str
    country: str


# SEPA entities
class SepaMandateType(str, Enum):
    CORE = 'core'
    B2B = 'b2b'


class SepaMandate:
    id: str
    type: SepaMandateType
    date_of_signature: datetime


class SepaAccountHolder:
    type: PaymentSetupAccountHolderType
    first_name: str
    last_name: str
    company_name: str


class Sepa(PaymentSetupPaymentMethod):
    account_holder: SepaAccountHolder
    account_number: str
    country: str
    currency: Currency
    mandate: SepaMandate


# Google Pay entities
class GooglePayTokenData:
    protocol_version: str
    signature: str
    signed_message: str
    tokenization_key: str


class GooglePay(PaymentSetupPaymentMethod):
    token_data: GooglePayTokenData
    token: str
    expires_on: datetime
    store_for_future_use: bool
    phone: Phone
    account_holder: PaymentSetupAccountHolder


# Apple Pay entities
class ApplePayTokenDataHeader:
    ephemeral_public_key: str
    public_key_hash: str
    transaction_id: str


class ApplePayTokenData:
    version: str
    data: str
    signature: str
    header: ApplePayTokenDataHeader


class ApplePay(PaymentSetupPaymentMethod):
    token_data: ApplePayTokenData
    token: str
    expires_on: datetime
    store_for_future_use: bool
    phone: Phone
    account_holder: PaymentSetupAccountHolder


# Card entities
class Card(PaymentSetupPaymentMethod):
    number: str
    last4: str
    bin: str
    scheme: str
    expiry_month: int
    expiry_year: int
    name: str
    cvv: str
    stored: bool
    expires_on: datetime
    store_for_future_use: bool
    phone: Phone
    account_holder: PaymentSetupAccountHolder
    allow_update: bool


class PaymentMethods:
    instrument: PaymentSetupInstrument
    klarna: Klarna
    stcpay: Stcpay
    tabby: Tabby
    bizum: Bizum
    paynow: PayNow
    qpay: Qpay
    eps: Eps
    ideal: Ideal
    knet: Knet
    bancontact: Bancontact
    benefit: Benefit
    blik: Blik
    vipps: Vipps
    twint: Twint
    alipay_cn: AlipayCn
    alipay_hk: AlipayHK
    gcash: GCash
    tng: Tng
    dana: Dana
    mobilepay: MobilePay
    tamara: Tamara
    mbway: MBWay
    multibanco: Multibanco
    wechatpay: WeChatPay
    kakaopay: KakaoPay
    truemoney: TrueMoney
    octopus: Octopus
    p24: P24
    alma: Alma
    swish: Swish
    sequra: Sequra
    ach: Ach
    sepa: Sepa
    paypal: Paypal
    googlepay: GooglePay
    applepay: ApplePay
    card: Card


# Settings entity
class Settings:
    success_url: str
    failure_url: str
    capture: bool
    excluded_payment_methods: list  # list of str (PaymentSourceType values)


# Order entities
class OrderSubMerchant:
    id: str
    product_category: str
    number_of_sales: int
    registration_date: datetime


class Order:
    items: list  # list of PaymentContextsItems
    shipping: ShippingDetails
    sub_merchants: list  # list of OrderSubMerchant
    discount_amount: int
    invoice_id: str
    shipping_amount: int
    tax_amount: int


# Industry entities
class AirlineData:
    ticket: PaymentContextsTicket
    passengers: list  # list of PaymentContextsPassenger
    flight_leg_details: list  # list of PaymentContextsFlightLegDetails


class Industry:
    airline_data: AirlineData
    accommodation_data: list  # list of AccommodationData


# Billing entity
class PaymentSetupBilling:
    address: Address


class AccountFundingTransactionIdentificationType(str, Enum):
    PASSPORT = 'passport'
    DRIVING_LICENSE = 'driving_license'
    NATIONAL_ID = 'national_id'


class AccountFundingTransactionIdentification:
    type: AccountFundingTransactionIdentificationType
    number: str
    issuing_country: str


class AccountFundingTransactionSender:
    date_of_birth: str
    reference: str
    identification: AccountFundingTransactionIdentification


class AccountFundingTransactionPurpose(str, Enum):
    DONATIONS = 'donations'
    EDUCATION = 'education'
    EMERGENCY_NEED = 'emergency_need'
    EXPATRIATION = 'expatriation'
    FAMILY_SUPPORT = 'family_support'
    FINANCIAL_SERVICES = 'financial_services'
    GIFTS = 'gifts'
    INCOME = 'income'
    INSURANCE = 'insurance'
    INVESTMENT = 'investment'
    IT_SERVICES = 'it_services'
    LEISURE = 'leisure'
    LOAN_PAYMENT = 'loan_payment'
    MEDICAL_TREATMENT = 'medical_treatment'
    OTHER = 'other'
    PENSION = 'pension'
    ROYALTIES = 'royalties'
    SAVINGS = 'savings'
    TRAVEL_AND_TOURISM = 'travel_and_tourism'


class AccountFundingTransactionRecipient:
    date_of_birth: str
    account_number: str
    first_name: str
    last_name: str
    address: Address


class PaymentSetupAccountFundingTransaction:
    enabled: bool
    purpose: AccountFundingTransactionPurpose
    sender: AccountFundingTransactionSender
    recipient: AccountFundingTransactionRecipient


# Main Request and Response classes
class PaymentSetupsRequest:
    processing_channel_id: str
    amount: int
    currency: Currency
    payment_type: PaymentType
    reference: str
    description: str
    payment_methods: PaymentMethods
    settings: Settings
    customer: Customer
    order: Order
    industry: Industry
    billing: PaymentSetupBilling
    account_funding_transaction: PaymentSetupAccountFundingTransaction
