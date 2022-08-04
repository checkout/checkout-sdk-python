from __future__ import absolute_import

from datetime import datetime
from enum import Enum
from checkout_sdk.common.common import Address, Phone, CustomerRequest
from checkout_sdk.common.enums import Currency, PaymentSourceType, Country
from checkout_sdk.payments.payments import PaymentType, PaymentDestinationType, ShippingDetails, ThreeDsRequest, \
    RiskRequest, PaymentRecipient, ProcessingSettings, BillingDescriptor


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


class BillingInformation:
    address: Address
    phone: Phone


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
    payment_method: str

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
