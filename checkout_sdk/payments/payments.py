from __future__ import absolute_import

from datetime import datetime
from enum import Enum

from checkout_sdk.common.common import Address, Phone, CustomerRequest
from checkout_sdk.common.enums import Currency, PaymentSourceType, ChallengeIndicator, Country


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


class PaymentDestinationType(str, Enum):
    BANK_ACCOUNT = 'bank_account'
    CARD = 'card'
    ID = 'id'
    TOKEN = 'token'


class PaymentType(str, Enum):
    REGULAR = 'Regular'
    RECURRING = 'Recurring'
    MOTO = 'MOTO'
    INSTALLMENT = 'Installment'


class Purpose(str, Enum):
    DONATIONS = 'donations'
    EDUCATION = 'education'
    EMERGENCY_NEED = 'emergency_need'
    EXPATRIATION = 'expatriation'
    FAMILY_SUPPORT = 'family_support'
    GIFTS = 'gifts'
    INCOME = 'income'
    INSURANCE = 'insurance'
    INVESTMENT = 'investment'
    IT_SERVICES = 'it_services'
    LEISURE = 'leisure'
    LOAN_PAYMENT = 'loan_payment'
    OTHER = 'other'
    PENSION = 'pension'
    ROYALTIES = 'royalties'
    SAVINGS = 'savings'
    TRAVEL_AND_TOURISM = 'travel_and_tourism'
    FINANCIAL_SERVICES = 'financial_services'
    MEDICAL_TREATMENT = 'medical_treatment'


class FundTransferType(str, Enum):
    AA = 'AA'
    PP = 'PP'
    FT = 'FT'
    FD = 'FD'
    PD = 'PD'
    LO = 'LO'
    OG = 'OG'


class PreferredSchema(str, Enum):
    VISA = 'visa'
    MASTERCARD = 'mastercard'
    CARTES_BANCAIRES = 'cartes_bancaires'


class ProductType(str, Enum):
    QR_CODE = 'QR Code'
    IN_APP = 'In-App'
    OFFICIAL_ACCOUNT = 'Official Account'
    MINI_PROGRAM = 'Mini Program'


class ThreeDSFlowType(str, Enum):
    CHALLENGED = 'challenged'
    FRICTIONLESS = 'frictionless'
    FRICTIONLESS_DELEGATED = 'frictionless_delegated'


class ShippingPreference(str, Enum):
    NO_SHIPPING = 'NO_SHIPPING'
    SET_PROVIDED_ADDRESS = 'SET_PROVIDED_ADDRESS'
    GET_FROM_FILE = 'GET_FROM_FILE'


class UserAction(str, Enum):
    PAY_NOW = 'PAY_NOW'
    CONTINUE = 'CONTINUE'


class MerchantInitiatedReason(str, Enum):
    DELAYED_CHARGE = 'Delayed_charge'
    RESUBMISSION = 'Resubmission'
    NO_SHOW = 'No_show'
    REAUTHORIZATION = 'Reauthorization'


class TerminalType(str, Enum):
    APP = 'APP'
    WAP = 'WAP'
    WEB = 'WEB'


class OsType(str, Enum):
    ANDROID = 'ANDROID'
    IOS = 'IOS'


class BillingDescriptor:
    name: str
    city: str


class BillingInformation:
    address: Address
    phone: Phone


class PaymentRecipient:
    dob: str
    account_number: str
    zip: str
    last_name: str


class ShippingDetails:
    address: Address
    phone: Phone


class RiskRequest:
    enabled: bool


class ThreeDsRequest:
    enabled: bool
    attempt_n3d: bool
    eci: str
    cryptogram: str
    xid: str
    version: str
    exemption: Exemption
    challenge_indicator: ChallengeIndicator
    # Only available in Four
    status: str
    authentication_date: datetime
    authentication_amount: int
    flow_type: ThreeDSFlowType
    status_reason_code: str
    challenge_cancel_reason: str
    score: str
    cryptogram_algorithm: str


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


class AirlineTicket:
    number: str
    issue_date: str
    issuing_carrier_code: str
    travel_agency_name: str
    travel_agency_code: str


class AirlinePassengerName:
    full_name: str


class AirlinePassenger:
    name: AirlinePassengerName
    date_of_birth: str
    country_code: Country


class AirlineFlightLegDetails:
    flight_number: int
    carrier_code: str
    service_class: str
    departure_date: str
    departure_time: str
    departure_airport: str
    arrival_airport: str
    stopover_code: str
    fare_basis_code: str


class AirlineData:
    ticket: AirlineTicket
    passenger: AirlinePassenger
    flight_leg_details: list  # AirlineFlightLegDetails


class ProcessingSettings:
    aft: bool
    merchant_initiated_reason: MerchantInitiatedReason
    dlocal: DLocalProcessingSettings
    # Only available on Four
    tax_amount: int
    shipping_amount: int
    preferred_scheme: PreferredSchema
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


# Request Source
class RequestSource:
    type: PaymentSourceType

    def __init__(self, type_p: PaymentSourceType):
        self.type = type_p


class RequestCardSource(RequestSource):
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


class RequestCustomerSource(RequestSource):
    id: str

    def __init__(self):
        super().__init__(PaymentSourceType.ID)


class RequestDLocalSource(RequestSource):
    number: str
    expiry_month: int
    expiry_year: int
    name: str
    cvv: str
    stored: bool
    billing_address: Address
    phone: Phone

    def __init__(self):
        super().__init__(PaymentSourceType.D_LOCAL)


class RequestIdSource(RequestSource):
    id: str
    cvv: str

    def __init__(self):
        super().__init__(PaymentSourceType.ID)


class RequestNetworkTokenSource(RequestSource):
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


class RequestTokenSource(RequestSource):
    token: str
    billing_address: Address
    phone: Phone
    store_for_future_use: bool

    def __init__(self):
        super().__init__(PaymentSourceType.TOKEN)


# Request Destination
class RequestDestination:
    type: PaymentDestinationType
    first_name: str
    last_name: str

    def __init__(self, type_p: PaymentDestinationType):
        self.type = type_p


class PaymentRequestCardDestination(RequestDestination):
    number: str
    expiry_month: int
    expiry_year: int
    name: str
    billing_address: Address
    phone: Phone

    def __init__(self):
        super().__init__(PaymentDestinationType.CARD)


class PaymentRequestIdDestination(RequestDestination):
    id: str

    def __init__(self):
        super().__init__(PaymentDestinationType.ID)


class PaymentRequestTokenDestination(RequestDestination):
    token: str
    billing_address: Address
    phone: Phone

    def __init__(self):
        super().__init__(PaymentDestinationType.TOKEN)


# Request
class PaymentRequest:
    source: RequestSource
    amount: int
    currency: Currency
    payment_type: PaymentType
    merchant_initiated: bool
    reference: str
    description: str
    capture: bool
    capture_on: datetime
    customer: CustomerRequest
    billing_descriptor: BillingDescriptor
    shipping: ShippingDetails
    previous_payment_id: str
    risk: RiskRequest
    success_url: str
    failure_url: str
    payment_ip: str
    three_ds: ThreeDsRequest
    recipient: PaymentRecipient
    metadata: dict
    processing: ProcessingSettings


class PayoutRequest:
    destination: RequestDestination
    amount: int
    fund_transfer_type: FundTransferType
    currency: Currency
    payment_type: PaymentType
    reference: str
    description: str
    capture: bool
    capture_on: datetime
    customer: CustomerRequest
    billing_descriptor: BillingDescriptor
    shipping: ShippingDetails
    three_ds: ThreeDsRequest
    previous_payment_id: str
    risk: RiskRequest
    success_url: str
    failure_url: str
    payment_ip: str
    recipient: PaymentRecipient
    metadata: dict
    processing: dict


# Captures
class CaptureRequest:
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
