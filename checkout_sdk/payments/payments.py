from __future__ import absolute_import

from datetime import datetime
from enum import Enum

from checkout_sdk.common.common import Address, Phone, CustomerRequest
from checkout_sdk.common.enums import Currency, PaymentSourceType, ChallengeIndicator, Country


class Exemption(str, Enum):
    LOW_VALUE = 'low_value',
    SECURE_CORPORATE_PAYMENT = 'secure_corporate_payment'
    TRUSTED_LISTING = 'trusted_listing'
    TRANSACTION_RISK_ASSESSMENT = 'transaction_risk_assessment'


class PaymentDestinationType(str, Enum):
    BANK_ACCOUNT = 'bank_account',
    CARD = 'card'
    ID = 'id'
    TOKEN = 'token'


class PaymentType(str, Enum):
    REGULAR = 'Regular',
    RECURRING = 'Recurring'
    MOTO = 'MOTO'
    INSTALLMENT = 'Installment'


class Purpose(str, Enum):
    DONATIONS = 'donations',
    EDUCATION = 'education'
    EMERGENCY_NEED = 'emergency_need'
    EXPATRIATION = 'expatriation'
    FAMILY_SUPPORT = 'family_support',
    GIFTS = 'gifts'
    INCOME = 'income'
    INSURANCE = 'insurance'
    INVESTMENT = 'investment',
    IT_SERVICES = 'it_services'
    LEISURE = 'leisure'
    LOAN_PAYMENT = 'loan_payment'
    OTHER = 'other',
    PENSION = 'pension'
    ROYALTIES = 'royalties'
    SAVINGS = 'savings'
    TRAVEL_AND_TOURISM = 'travel_and_tourism',
    FINANCIAL_SERVICES = 'financial_services'
    MEDICAL_TREATMENT = 'medical_treatment'


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
    first_name: str
    last_name: str
    country: Country


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


class ProcessingSettings:
    aft: bool


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
