from __future__ import absolute_import

from datetime import datetime
from enum import Enum

from checkout_sdk.common.common import AccountHolder, BankDetails, MarketplaceData, Address, Phone, CustomerRequest
from checkout_sdk.common.enums import PaymentSourceType, Currency, Country, AccountType, ChallengeIndicator


class AuthorizationType(str, Enum):
    FINAL = 'Final'
    ESTIMATED = 'Estimated'
    INCREMENTAL = 'Incremental'


class CaptureType(str, Enum):
    NON_FINAL = 'NonFinal'
    FINAL = 'Final'


class InstructionScheme(str, Enum):
    SWIFT = 'swift'
    LOCAL = 'local'
    INSTANT = 'instant'


class PaymentSenderType(str, Enum):
    INDIVIDUAL = 'individual'
    CORPORATE = 'corporate'
    INSTRUMENT = 'instrument'


class IdentificationType(str, Enum):
    PASSPORT = 'passport'
    DRIVING_LICENSE = 'driving_licence'
    NATIONAL_ID = 'national_id'


class PayoutSourceType(str, Enum):
    CURRENCY_ACCOUNT = 'currency_account'


class PaymentType(str, Enum):
    REGULAR = 'Regular'
    RECURRING = 'Recurring'
    MOTO = 'MOTO'
    INSTALLMENT = 'Installment'
    UNSCHEDULED = 'Unscheduled'


class PaymentDestinationType(str, Enum):
    BANK_ACCOUNT = 'bank_account'
    CARD = 'card'
    ID = 'id'
    TOKEN = 'token'


class Exemption(str, Enum):
    LOW_VALUE = 'low_value'
    SECURE_CORPORATE_PAYMENT = 'secure_corporate_payment'
    TRUSTED_LISTING = 'trusted_listing'
    TRANSACTION_RISK_ASSESSMENT = 'transaction_risk_assessment'
    THREE_DS_OUTAGE = '3ds_outage'
    SCA_DELEGATION = 'sca_delegation'
    OUT_OF_SCA_SCOPE = 'out_of_sca_scope'
    OTHER = 'other'
    LOW_RISK_PROGRAM = 'low_risk_program'


class ThreeDSFlowType(str, Enum):
    CHALLENGED = 'challenged'
    FRICTIONLESS = 'frictionless'
    FRICTIONLESS_DELEGATED = 'frictionless_delegated'


class MerchantInitiatedReason(str, Enum):
    DELAYED_CHARGE = 'Delayed_charge'
    RESUBMISSION = 'Resubmission'
    NO_SHOW = 'No_show'
    REAUTHORIZATION = 'Reauthorization'


class PreferredSchema(str, Enum):
    VISA = 'visa'
    MASTERCARD = 'mastercard'
    CARTES_BANCAIRES = 'cartes_bancaires'


class ProductType(str, Enum):
    QR_CODE = 'QR Code'
    IN_APP = 'In-App'
    OFFICIAL_ACCOUNT = 'Official Account'
    MINI_PROGRAM = 'Mini Program'


class TerminalType(str, Enum):
    APP = 'APP'
    WAP = 'WAP'
    WEB = 'WEB'


class OsType(str, Enum):
    ANDROID = 'ANDROID'
    IOS = 'IOS'


class ShippingPreference(str, Enum):
    NO_SHIPPING = 'NO_SHIPPING'
    SET_PROVIDED_ADDRESS = 'SET_PROVIDED_ADDRESS'
    GET_FROM_FILE = 'GET_FROM_FILE'


class UserAction(str, Enum):
    PAY_NOW = 'PAY_NOW'
    CONTINUE = 'CONTINUE'


class BillingDescriptor:
    name: str
    city: str
    # Not available on previous
    reference: str


class PaymentInstruction:
    purpose: str
    charge_bearer: str
    repair: bool
    scheme: InstructionScheme
    quote_id: str


class PayoutBillingDescriptor:
    reference: str


class Identification:
    type: IdentificationType
    number: str
    issuing_country: Country


# Payment Sender
class PaymentSender:
    type: PaymentSenderType

    def __init__(self, type_p: PaymentSenderType):
        self.type = type_p


class PaymentCorporateSender(PaymentSender):
    company_name: str
    address: Address

    def __init__(self):
        super().__init__(PaymentSenderType.CORPORATE)


class PaymentIndividualSender(PaymentSender):
    first_name: str
    last_name: str
    address: Address
    identification: Identification

    def __init__(self):
        super().__init__(PaymentSenderType.INDIVIDUAL)


class PaymentInstrumentSender(PaymentSender):

    def __init__(self):
        super().__init__(PaymentSenderType.INSTRUMENT)


# Payment Request Source
class PaymentRequestSource:
    type: PaymentSourceType

    def __init__(self, type_p: PaymentSourceType):
        self.type = type_p


class PaymentRequestCardSource(PaymentRequestSource):
    number: str
    expiry_month: int
    expiry_year: int
    name: str
    cvv: str
    stored: bool
    store_for_future_use: bool
    billing_address: Address
    phone: Phone

    def __init__(self):
        super().__init__(PaymentSourceType.CARD)


class PaymentRequestTokenSource(PaymentRequestSource):
    token: str
    billing_address: Address
    phone: Phone
    store_for_future_use: bool

    def __init__(self):
        super().__init__(PaymentSourceType.TOKEN)


class PaymentRequestNetworkTokenSource(PaymentRequestSource):
    token: str
    expiry_month: int
    expiry_year: int
    token_type: str
    cryptogram: str
    eci: str
    stored: bool
    name: str
    cvv: str
    billing_address: Address
    phone: Phone

    def __init__(self):
        super().__init__(PaymentSourceType.NETWORK_TOKEN)


class PaymentRequestIdSource(PaymentRequestSource):
    id: str
    cvv: str

    def __init__(self):
        super().__init__(PaymentSourceType.ID)


class RequestProviderTokenSource(PaymentRequestSource):
    payment_method: str
    token: str
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(PaymentSourceType.PROVIDER_TOKEN)


class RequestBankAccountSource(PaymentRequestSource):
    payment_method: str
    account_type: str
    country: Country
    account_number: str
    bank_code: str
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(PaymentSourceType.BANK_ACCOUNT)


class ShippingDetails:
    address: Address
    phone: Phone
    from_address_zip: str


class ThreeDsRequest:
    enabled: bool
    attempt_n3d: bool
    eci: str
    cryptogram: str
    xid: str
    version: str
    exemption: Exemption
    challenge_indicator: ChallengeIndicator
    # Not available on Previous
    status: str
    authentication_date: datetime
    authentication_amount: int
    flow_type: ThreeDSFlowType
    status_reason_code: str
    challenge_cancel_reason: str
    score: str
    cryptogram_algorithm: str


class RiskRequest:
    enabled: bool


class PaymentRecipient:
    dob: str
    account_number: str
    zip: str
    last_name: str


class Payer:
    name: str
    email: str
    document: str


class Installments:
    count: str


class DLocalProcessingSettings:
    country: Country
    payer: Payer
    installments: Installments


class ProcessingSettings:
    order_id: str
    tax_amount: int
    discount_amount: int
    duty_amount: int
    shipping_amount: int
    shipping_tax_amount: int
    aft: bool
    preferred_scheme: PreferredSchema
    merchant_initiated_reason: MerchantInitiatedReason
    campaign_id: int
    product_type: ProductType
    open_id: str
    original_order_amount: int
    receipt_id: str
    terminal_type: TerminalType
    os_type: OsType
    invoice_id: str
    brand_name: str
    locale: str
    shipping_preference: ShippingPreference
    user_action: UserAction
    set_transaction_context: list  # dict
    airline_data: list  # AirlineData
    dlocal: DLocalProcessingSettings


class Product:
    name: str
    quantity: int
    unit_price: int
    reference: str
    commodity_code: str
    unit_of_measure: str
    total_amount: int
    tax_amount: int
    discount_amount: int
    wxpay_goods_id: str
    image_url: str
    url: str
    sku: str


class PaymentCustomerRequest(CustomerRequest):
    tax_number: str


# Request Payment
class PaymentRequest:
    source: PaymentRequestSource
    amount: int
    currency: Currency
    payment_type: PaymentType
    merchant_initiated: bool
    reference: str
    description: str
    authorization_type: AuthorizationType
    capture: bool
    capture_on: datetime
    customer: PaymentCustomerRequest
    billing_descriptor: BillingDescriptor
    shipping: ShippingDetails
    three_ds: ThreeDsRequest
    processing_channel_id: str
    previous_payment_id: str
    risk: RiskRequest
    success_url: str
    failure_url: str
    payment_ip: str
    sender: PaymentSender
    recipient: PaymentRecipient
    marketplace: MarketplaceData
    processing: ProcessingSettings
    metadata: dict
    items: list  # payments.Product


# Payout Request Source
class PayoutRequestSource:
    type: PayoutSourceType

    def __init__(self, type_p: PayoutSourceType):
        self.type = type_p


class PayoutRequestCurrencyAccountSource(PayoutRequestSource):
    id: str

    def __init__(self):
        super().__init__(PayoutSourceType.CURRENCY_ACCOUNT)


# Payment Request Destination
class PaymentRequestDestination:
    type: PaymentDestinationType

    def __init__(self, type_p: PaymentDestinationType):
        self.type = type_p


class PaymentBankAccountDestination(PaymentRequestDestination):
    account_type: AccountType
    account_number: str
    bank_code: str
    branch_code: str
    iban: str
    swift_bic: str
    country: Country
    account_holder: AccountHolder
    bank: BankDetails

    def __init__(self):
        super().__init__(PaymentDestinationType.BANK_ACCOUNT)


class PaymentRequestIdDestination(PaymentRequestDestination):
    id: str

    def __init__(self):
        super().__init__(PaymentDestinationType.ID)


# Request Payout
class PayoutRequest:
    source: PayoutRequestSource
    destination: PaymentRequestDestination
    amount: int
    currency: Currency
    reference: str
    billing_descriptor: PayoutBillingDescriptor
    sender: PaymentSender
    instruction: PaymentInstruction
    processing_channel_id: str


# Captures
class CaptureRequest:
    amount: int
    capture_type: CaptureType
    reference: str
    customer: PaymentCustomerRequest
    description: str
    billing_descriptor: BillingDescriptor
    shipping: ShippingDetails
    items: list  # payments.Product
    marketplace: MarketplaceData
    processing: ProcessingSettings
    metadata: dict


# Authorization
class AuthorizationRequest:
    amount: int
    reference: str
    metadata: dict


# Refunds
class RefundRequest:
    amount: int
    reference: str
    metadata: dict


# Voids
class VoidRequest:
    reference: str
    metadata: dict
