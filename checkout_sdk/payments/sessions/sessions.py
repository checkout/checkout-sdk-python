from datetime import datetime
from enum import Enum

from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.payments import PaymentType, BillingDescriptor, ShippingDetails, \
    PaymentRecipient, ProcessingSettings, RiskRequest, ThreeDsRequest, PaymentSender


class PaymentMethodsType(str, Enum):
    ALIPAY_CN = 'alipay_cn'
    ALIPAY_HK = 'alipay_hk'
    ALMA = 'alma'
    APPLEPAY = 'applepay'
    BANCONTACT = 'bancontact'
    BENEFIT = 'benefit'
    BIZUM = 'bizum'
    CARD = 'card'
    DANA = 'dana'
    EPS = 'eps'
    GCASH = 'gcash'
    GOOGLEPAY = 'googlepay'
    IDEAL = 'ideal'
    KAKAOPAY = 'kakaopay'
    KLARNA = 'klarna'
    KNET = 'knet'
    MBWAY = 'mbway'
    MOBILEPAY = 'mobilepay'
    MULTIBANCO = 'multibanco'
    P24 = 'p24'
    PAYNOW = 'paynow'
    PAYPAL = 'paypal'
    PLAID = 'plaid'
    QPAY = 'qpay'
    REMEMBER_ME = 'remember_me'
    SEPA = 'sepa'
    STCPAY = 'stcpay'
    STORED_CARD = 'stored_card'
    TABBY = 'tabby'
    TAMARA = 'tamara'
    TNG = 'tng'
    TRUEMONEY = 'truemoney'
    TWINT = 'twint'
    VIPPS = 'vipps'
    WECHATPAY = 'wechatpay'


class Locale(str, Enum):
    AR = 'ar'
    DA_DK = 'da-DK'
    DE_DE = 'de-DE'
    EL = 'el'
    EN_GB = 'en-GB'
    ES_ES = 'es-ES'
    FI_FI = 'fi-FI'
    FIL_PH = 'fil-PH'
    FR_FR = 'fr-FR'
    HI_IN = 'hi-IN'
    ID_ID = 'id-ID'
    IT_IT = 'it-IT'
    JA_JP = 'ja-JP'
    KO_KR = 'ko-KR'
    MS_MY = 'ms-MY'
    NB_NO = 'nb-NO'
    NL_NL = 'nl-NL'
    PT_PT = 'pt-PT'
    SV_SE = 'sv-SE'
    TH_TH = 'th-TH'
    VI_VN = 'vi-VN'
    ZH_CN = 'zh-CN'
    ZH_HK = 'zh-HK'
    ZH_TW = 'zh-TW'


class StorePaymentDetails(str, Enum):
    DISABLED = 'disabled'
    ENABLED = 'enabled'
    COLLECT_CONSENT = 'collect_consent'


class InstructionPurpose(str, Enum):
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


class Instruction:
    purpose: InstructionPurpose


class CustomerRetry:
    max_attempts: int


class AccountHolderType(str, Enum):
    INDIVIDUAL = 'individual'
    CORPORATE = 'corporate'
    GOVERNMENT = 'government'


class BillingAddress:
    country: str
    address_line1: str
    address_line2: str
    city: str
    state: str
    zip: str


class BillingPhone:
    country_code: str
    number: str


class SessionBilling:
    address: BillingAddress
    phone: BillingPhone


class CustomerSummary:
    registration_date: str
    first_transaction_date: str
    last_payment_date: str
    total_order_count: int
    last_payment_amount: float
    is_premium_customer: bool
    is_returning_customer: bool
    lifetime_value: float


class SessionPaymentCustomerRequest:
    email: str
    name: str
    id: str
    phone: BillingPhone
    tax_number: str
    summary: CustomerSummary


class AccountHolder:
    type: AccountHolderType

    def __init__(self, type_p: AccountHolderType):
        self.type = type_p


class IndividualAccountHolder(AccountHolder):
    first_name: str
    last_name: str
    middle_name: str
    account_name_inquiry: bool

    def __init__(self):
        super().__init__(AccountHolderType.INDIVIDUAL)


class CorporateAccountHolder(AccountHolder):
    company_name: str
    account_name_inquiry: bool

    def __init__(self):
        super().__init__(AccountHolderType.CORPORATE)


class ApplePayConfiguration:
    store_payment_details: StorePaymentDetails
    account_holder: AccountHolder


class CardConfiguration:
    store_payment_details: StorePaymentDetails
    account_holder: AccountHolder


class GooglePayConfiguration:
    store_payment_details: StorePaymentDetails
    account_holder: AccountHolder


class StoredCardConfiguration:
    customer_id: str
    instrument_ids: list  # list of strings
    default_instrument_id: str


class SessionPaymentMethodConfiguration:
    applepay: ApplePayConfiguration
    card: CardConfiguration
    googlepay: GooglePayConfiguration
    stored_card: StoredCardConfiguration


class Item:
    name: str
    quantity: int
    unit_price: int
    reference: str
    commodity_code: str
    unit_of_measure: str
    total_amount: int
    tax_amount: int
    discount_amount: int
    url: str
    image_url: str


class PaymentSessionsRequest:
    amount: int
    currency: Currency
    billing: SessionBilling
    success_url: str
    failure_url: str
    payment_type: PaymentType
    billing_descriptor: BillingDescriptor
    reference: str
    description: str
    customer: SessionPaymentCustomerRequest
    shipping: ShippingDetails
    recipient: PaymentRecipient
    processing: ProcessingSettings
    instruction: Instruction
    processing_channel_id: str
    payment_method_configuration: SessionPaymentMethodConfiguration
    items: list  # Item
    amount_allocations: list  # AmountAllocations
    risk: RiskRequest
    display_name: str
    metadata: dict
    locale: str
    three_ds: ThreeDsRequest
    sender: PaymentSender
    capture: bool
    capture_on: datetime
    expires_on: datetime
    enabled_payment_methods: list  # PaymentMethodsType
    disabled_payment_methods: list  # PaymentMethodsType
    customer_retry: CustomerRetry
    ip_address: str


class PaymentSessionWithPaymentRequest:
    session_data: str
    amount: int
    currency: Currency
    billing: SessionBilling
    success_url: str
    failure_url: str
    payment_type: PaymentType
    billing_descriptor: BillingDescriptor
    reference: str
    description: str
    customer: SessionPaymentCustomerRequest
    shipping: ShippingDetails
    recipient: PaymentRecipient
    processing: ProcessingSettings
    instruction: Instruction
    processing_channel_id: str
    payment_method_configuration: SessionPaymentMethodConfiguration
    items: list  # Item
    amount_allocations: list  # AmountAllocations
    risk: RiskRequest
    display_name: str
    metadata: dict
    locale: str
    three_ds: ThreeDsRequest
    sender: PaymentSender
    capture: bool
    capture_on: datetime


class SubmitPaymentSessionRequest:
    session_data: str
    amount: int
    reference: str
    items: list  # Item
    three_ds: ThreeDsRequest
    ip_address: str
    payment_type: PaymentType
