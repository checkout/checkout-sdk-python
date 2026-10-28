from __future__ import absolute_import

from datetime import datetime
from enum import Enum
from typing import List, Union

from checkout_sdk.common.common import AccountHolder, BankDetails, MarketplaceData, Address, Phone, CustomerRequest, \
    AccountHolderIdentification, QueryFilterDateRange
from checkout_sdk.common.enums import PaymentSourceType, Currency, Country, AccountType, ChallengeIndicator
from checkout_sdk.sessions.sessions import DeliveryTimeframe


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
    GOVERNMENT = 'government'


class SourceOfFunds(str, Enum):
    CREDIT = 'credit'
    DEBIT = 'debit'
    PREPAID = 'prepaid'
    DEPOSIT_ACCOUNT = 'deposit_account'
    MOBILE_MONEY_ACCOUNT = 'mobile_money_account'
    CASH = 'cash'


class PayoutSourceType(str, Enum):
    CURRENCY_ACCOUNT = 'currency_account'
    ENTITY = 'entity'


class PaymentType(str, Enum):
    REGULAR = 'Regular'
    RECURRING = 'Recurring'
    MOTO = 'MOTO'
    INSTALLMENT = 'Installment'
    PAYLATER = 'PayLater'
    UNSCHEDULED = 'Unscheduled'


class PaymentDestinationType(str, Enum):
    """The payout destination type.

    Shared by two discriminators: the card payout destination (card, network_token, id, token)
    and the bank payout destination (id, bank_account).
    """
    BANK_ACCOUNT = 'bank_account'
    CARD = 'card'
    ID = 'id'
    NETWORK_TOKEN = 'network_token'
    TOKEN = 'token'


class NetworkTokenType(str, Enum):
    """The network token type."""
    VTS = 'vts'
    MDES = 'mdes'
    APPLEPAY = 'applepay'
    GOOGLEPAY = 'googlepay'


class Exemption(str, Enum):
    LOW_VALUE = 'low_value'
    SECURE_CORPORATE_PAYMENT = 'secure_corporate_payment'
    TRUSTED_LISTING = 'trusted_listing'
    TRUSTED_LISTING_PROMPT = 'trusted_listing_prompt'
    TRANSACTION_RISK_ASSESSMENT = 'transaction_risk_assessment'
    THREE_DS_OUTAGE = '3ds_outage'
    SCA_DELEGATION = 'sca_delegation'
    OUT_OF_SCA_SCOPE = 'out_of_sca_scope'
    OTHER = 'other'
    LOW_RISK_PROGRAM = 'low_risk_program'
    DATA_SHARE = 'data_share'
    RECURRING_OPERATION = 'recurring_operation'


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


class BillingPlanType(str, Enum):
    MERCHANT_INITIATED_BILLING = 'MERCHANT_INITIATED_BILLING'
    MERCHANT_INITIATED_BILLING_SINGLE_AGREEMENT = 'MERCHANT_INITIATED_BILLING_SINGLE_AGREEMENT'
    CHANNEL_INITIATED_BILLING = 'CHANNEL_INITIATED_BILLING'
    CHANNEL_INITIATED_BILLING_SINGLE_AGREEMENT = 'CHANNEL_INITIATED_BILLING_SINGLE_AGREEMENT'
    RECURRING_PAYMENTS = 'RECURRING_PAYMENTS'
    PRE_APPROVED_PAYMENTS = 'PRE_APPROVED_PAYMENTS'


class PanPreference(str, Enum):
    FPAN = 'fpan'
    DPAN = 'dpan'


class CardFundingType(str, Enum):
    CREDIT = 'credit'
    DEBIT = 'debit'


class ServiceType(str, Enum):
    SAME_DAY = 'same_day'
    STANDARD = 'standard'


class AmountVariability(str, Enum):
    FIXED = 'Fixed'
    VARIABLE = 'Variable'


class AuthenticationExperience(str, Enum):
    GOOGLE_SPA = 'google_spa'
    THREE_DS = '3ds'


class RoutingScheme(str, Enum):
    ACCEL = 'accel'
    AMEX = 'amex'
    CARTES_BANCAIRES = 'cartes_bancaires'
    DINERS = 'diners'
    DISCOVER = 'discover'
    JCB = 'jcb'
    MADA = 'mada'
    MAESTRO = 'maestro'
    MASTERCARD = 'mastercard'
    NYCE = 'nyce'
    OMANNET = 'omannet'
    PULSE = 'pulse'
    SHAZAM = 'shazam'
    STAR = 'star'
    UPI = 'upi'
    VISA = 'visa'


class LocalCharacterSets(str, Enum):
    KANJI = 'kanji'
    KATAKANA = 'katakana'


class LocalBillingDescriptor:
    name: str
    character_set: LocalCharacterSets


class BillingDescriptor:
    name: str
    city: str
    reference: str
    local_descriptors: list  # LocalBillingDescriptor


class Remitance:
    reference: str


class PaymentInstruction:
    purpose: str
    charge_bearer: str
    repair: bool
    scheme: InstructionScheme
    remittance: Remitance
    quote_id: str
    funds_transfer_type: str


class PayoutBillingDescriptor:
    reference: str


# Payment Sender
class PaymentSender:
    type: PaymentSenderType
    reference: str

    def __init__(self, type_p: PaymentSenderType):
        self.type = type_p


class PaymentCorporateSender(PaymentSender):
    company_name: str
    address: Address
    reference: str
    reference_type: str
    source_of_funds: SourceOfFunds
    identification: AccountHolderIdentification

    def __init__(self):
        super().__init__(PaymentSenderType.CORPORATE)


# Narrow-applicability sender. The `government` type is only accepted by the
# CardPayoutRequest.sender slot in the API. Using this class on
# PaymentRequest.sender or BankPayoutRequest.sender will be rejected by the
# API with a 422, because those endpoints' sender discriminators only accept
# `individual`, `corporate`, and `instrument`. Type safety can't catch this
# today because Python's PaymentSender is shared across all three slots; a
# future split into a dedicated CardPayoutSender hierarchy would fix it.
class PaymentGovernmentSender(PaymentSender):
    company_name: str
    address: Address
    reference: str
    reference_type: str
    source_of_funds: SourceOfFunds
    identification: AccountHolderIdentification

    def __init__(self):
        super().__init__(PaymentSenderType.GOVERNMENT)


# Backward-compat alias for the misspelled class name shipped in earlier SDK
# versions. Prefer PaymentGovernmentSender in new code; this alias will be
# removed in a future major version.
PaymentGovermentSender = PaymentGovernmentSender


class PaymentIndividualSender(PaymentSender):
    first_name: str
    middle_name: str
    last_name: str
    dob: str
    address: Address
    identification: AccountHolderIdentification
    reference: str
    reference_type: str
    source_of_funds: SourceOfFunds
    date_of_birth: str
    country_of_birth: Country
    nationality: Country

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
    account_holder: AccountHolder
    allow_update: bool

    def __init__(self):
        super().__init__(PaymentSourceType.CARD)


class PaymentRequestTokenSource(PaymentRequestSource):
    token: str
    billing_address: Address
    phone: Phone
    stored: bool
    store_for_future_use: bool
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(PaymentSourceType.TOKEN)


class PaymentRequestNetworkTokenSource(PaymentRequestSource):
    """A network token payment source."""
    # The network token PAN.
    # [Required]
    token: str
    # The expiry month of the token.
    # [Required]
    # min 1
    expiry_month: int
    # The expiry year of the token.
    # [Required]
    expiry_year: int
    # The type of token.
    # [Required]
    # Enum: "vts" "mdes" "applepay" "googlepay"
    token_type: NetworkTokenType
    # The Base64 encoded cryptographic identifier (TAVV) used by card schemes to validate the token
    # verification result. Optional if previous_payment_id is specified and 3ds.enabled is false.
    # [Required]
    # max 100 characters
    cryptogram: str
    # The Electronic Commerce Indicator (ECI) security level associated with the token. Optional if
    # previous_payment_id is specified and 3ds.enabled is false.
    # [Required]
    # max 2 characters
    eci: str
    # Indicates whether this card is being submitted from your own stored card-on-file system, rather
    # than being entered by the customer at the time of payment. Set to true when you provide card details
    # that you already have on file for the customer.
    # [Optional]
    # Default: false
    stored: bool
    # This must be set to true if you intend to reuse the payment credentials in subsequent payments.
    # Setting the field as false will mean that a payment instrument will not be included in the payment
    # response.
    # [Optional]
    # Default: true
    store_for_future_use: bool
    # The customer's name.
    # [Optional]
    name: str
    # The card verification value/code. 3 digits, except for American Express (4 digits).
    # [Optional]
    # min 3 characters
    # max 4 characters
    cvv: str
    # The customer's billing address.
    # [Optional]
    billing_address: Address
    # The customer's phone number.
    # [Optional]
    phone: Phone
    # Information about the account holder of the card.
    # [Optional]
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(PaymentSourceType.NETWORK_TOKEN)


class PaymentRequestIdSource(PaymentRequestSource):
    id: str
    cvv: str
    payment_method: str
    stored: bool
    store_for_future_use: bool
    account_holder: AccountHolder
    billing_address: Address
    phone: Phone
    allow_update: bool

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


class RequestCustomerSource(PaymentRequestSource):
    id: str
    account_holder: AccountHolder
    billing_address: Address
    phone: Phone
    allow_update: bool

    def __init__(self):
        super().__init__(PaymentSourceType.CUSTOMER)


class PaymentContextsShippingMethod(str, Enum):
    DIGITAL = 'Digital'
    PICK_UP = 'PickUp'
    BILLING_ADDRESS = 'BillingAddress'
    OTHER_ADDRESS = 'OtherAddress'


class TrackingInfo:
    tracking_number: str
    tracking_uri: str
    shipping_company: str
    return_tracking_number: str
    return_tracking_uri: str
    return_shipping_company: str


class ShippingDetails:
    first_name: str
    last_name: str
    email: str
    address: Address
    phone: Phone
    from_address_zip: str
    timeframe: DeliveryTimeframe
    method: PaymentContextsShippingMethod
    delay: int
    tracking_info: list  # TrackingInfo


class InitialAuthentication:
    acs_transaction_id: str
    authentication_method: str
    authentication_timestamp: str
    authentication_data: str
    initial_session_id: str


class ThreeDsRequest:
    enabled: bool
    attempt_n3d: bool
    eci: str
    cryptogram: str
    xid: str
    version: str
    exemption: Exemption
    challenge_indicator: ChallengeIndicator
    allow_upgrade: bool
    status: str
    authentication_date: datetime
    authentication_amount: int
    flow_type: ThreeDSFlowType
    status_reason_code: str
    challenge_cancel_reason: str
    score: str
    cryptogram_algorithm: str
    authentication_id: str
    initial_authentication: InitialAuthentication


class DeviceProvider:
    id: str
    name: str


class Network:
    ipv4: str
    ipv6: str
    tor: bool
    vpn: bool
    proxy: bool


class DeviceDetails:
    user_agent: str
    network: Network
    provider: DeviceProvider
    timestamp: str
    timezone: str
    virtual_machine: bool
    incognito: bool
    jailbroken: bool
    rooted: bool
    java_enabled: bool
    javascript_enabled: bool
    language: str
    color_depth: str
    screen_height: str
    screen_width: str
    user_agent_client_hint: str
    iframe_payment_allowed: bool
    accept_header: str


class RiskRequest:
    enabled: bool
    device_session_id: str
    device: DeviceDetails


class PaymentRecipient:
    dob: str
    account_number: str
    address: Address
    zip: str
    first_name: str
    last_name: str
    country: Country


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


# Deprecated: SenderInformation is not defined in the current Checkout.com API swagger. The
# property appears under neither `senderInformation` nor `sender_information` in any spec
# available to this workspace, including the live API reference, and no processing schema declares
# a sender property of any kind. The current API carries sender details in the top level `sender`
# object on the payment request instead. Retained for backward compatibility with previous-API
# (ABC) callers; new code should not set this. Will be removed in a future major version.
class SenderInformation:
    reference: str
    first_name: str
    last_name: str
    dob: str
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    source_of_funds: str


class PartnerCustomerRiskData:
    """A key-and-value pair with merchant-specific data for the transaction."""
    # The key for the pair.
    # [Optional]
    key: str
    # The value for the pair.
    # [Optional]
    value: str


class Ticket:
    """Contains information about the airline ticket."""
    # The ticket's unique identifier.
    # [Optional]
    number: str
    # Date the airline ticket was issued.
    # [Optional]
    # format: date (YYYY-MM-DD)
    issue_date: str
    # Carrier code of the ticket issuer.
    # [Optional]
    issuing_carrier_code: str
    # C = Car rental reservation, A = Airline flight reservation, B = Both car rental and
    # airline flight reservations included, N = Unknown. Free-form string in the spec, not a
    # typed enum.
    # [Optional]
    travel_package_indicator: str
    # The name of the travel agency.
    # [Optional]
    travel_agency_name: str
    # The unique identifier from IATA or ARC for the travel agency that issues the ticket.
    # [Optional]
    travel_agency_code: str


class PassengerAddress:
    """Contains information about a passenger's address."""
    # The two-letter ISO country code of the passenger's country of residence.
    # [Optional]
    country: str


class Passenger:
    """Contains information about a passenger on the flight."""
    # The passenger's first name.
    # [Optional]
    first_name: str
    # The passenger's last name.
    # [Optional]
    last_name: str
    # The passenger's date of birth.
    # [Optional]
    # format: date (YYYY-MM-DD)
    date_of_birth: str
    # Contains information about the passenger's address. The spec defines exactly one
    # property on this object, country.
    # [Optional]
    address: PassengerAddress


class FlightLegDetails:
    """Contains information about a flight leg booked by the customer."""
    # The flight identifier.
    # [Optional]
    flight_number: str
    # The IATA 2-letter accounting code (PAX) that identifies the carrier. Required if the
    # airline data includes leg details.
    # [Optional]
    carrier_code: str
    # A one-letter travel class identifier. The following are common: F = First class,
    # J = Business class, Y = Economy class, W = Premium economy.
    # [Optional]
    class_of_travelling: str
    # The IATA three-letter airport code of the departure airport. Required if the airline
    # data includes leg details.
    # [Optional]
    departure_airport: str
    # The date of the scheduled take off.
    # [Optional]
    # format: date (YYYY-MM-DD)
    departure_date: str
    # The time of the scheduled take off.
    # [Optional]
    departure_time: str
    # The IATA 3-letter airport code of the destination airport. Required if the airline data
    # includes leg details.
    # [Optional]
    arrival_airport: str
    # A one-letter code that indicates whether the passenger is entitled to make a stopover.
    # Can be a space, O if the passenger is entitled to make a stopover, or X if they are not.
    # [Optional]
    stop_over_code: str
    # The fare basis code, alphanumeric.
    # [Optional]
    fare_basis_code: str


class AirlineData:
    """Contains information about the airline ticket and flights booked by the customer.

    Referenced by ProcessingSettings.airline_data and by the GET /payments/{id} response. The
    class did not exist before: the only AirlineData in the SDK was the legacy ABC one in
    payments_previous.py, whose shape differs, so the type comment on
    ProcessingSettings.airline_data pointed at nothing in this module.

    Import this one for the current (NAS) API. checkout_sdk.payments.payments_previous also
    defines a class called AirlineData, for the Previous (ABC) API only; its shape is different
    and the current gateway discards it.
    """
    # Contains information about the airline ticket.
    # [Optional]
    ticket: Ticket
    # Contains information about the passenger(s) on the flight.
    # [Optional]
    #
    # Accepts a single Passenger or a list of them, and the choice is not cosmetic. Every row
    # below was sent to the sandbox, the first four on 2026-09-25 and re-verified with the fifth
    # on 2026-09-28:
    #
    #   surface                  passenger: object   passenger: array
    #   POST /payments           201                 201
    #   POST /payment-sessions   201                 201
    #   POST /hosted-payments    201                 422 processing_airline_data_0_passenger_invalid
    #   POST /payment-links      201                 422 processing_airline_data_0_passenger_invalid
    #   POST /payment-contexts   201                 422 passenger_required
    #
    # So prefer a single Passenger: that is accepted on every request surface. Use a list only
    # for two or more passengers, and only against POST /payments or POST /payment-sessions,
    # which are the only surfaces that take it. ProcessingSettings is shared by POST /payments,
    # hosted payments and payment links, so a list is not a safe default even though the
    # specification declares the property array-only.
    #
    # Note that hosted payments, payment links and payment sessions all resolve to the same
    # PaymentInterfacesProcessing schema, yet the first two reject the array and the third
    # accepts it: validation is per endpoint, not per schema.
    #
    # An empty list and an explicit null are both rejected, so leave the attribute unset when
    # there are no passengers; the serializer only emits attributes that were assigned.
    # Recorded in the plan under P1.
    passenger: Union[Passenger, List[Passenger]]
    # Contains information about the flight leg(s) booked by the customer.
    # [Optional]
    flight_leg_details: list  # FlightLegDetails


class AccommodationPhone:
    """Phone contact information for an accommodation property."""
    # The phone country code.
    # [Optional]
    country_code: str
    # The phone number.
    # [Optional]
    number: str


class AccommodationAddress:
    """The address details of the accommodation."""
    # The first line of the address.
    # [Optional]
    address_line1: str
    # The postal code for the address.
    # [Optional]
    zip: str


class AccommodationGuest:
    """Contains information about a guest staying at the accommodation."""
    # The first name of the guest.
    # [Optional]
    first_name: str
    # The last name of the guest.
    # [Optional]
    last_name: str
    # The date of birth of the guest.
    # [Optional]
    # format: date (YYYY-MM-DD)
    date_of_birth: str


class AccommodationRoom:
    """Contains information about a room booked by the customer."""
    # For lodging, the nightly rate for one room. For cruise, the total cost of the cruise.
    # Declared as a string in the spec, not a number.
    # [Optional]
    rate: str
    # For lodging, the number of nights charged at the rate provided in the rate field. For
    # cruise, the length of the cruise in days. Declared as a string in the spec.
    # [Optional]
    number_of_nights_at_room_rate: str


class AccommodationData:
    """Contains information about the accommodation booked by the customer."""
    # For lodging, the lodging name that appears on the storefront/customer receipts. For
    # cruise, the ship name booked for the cruise.
    # [Optional]
    name: str
    # A unique identifier for the booking.
    # [Optional]
    booking_reference: str
    # For lodging, the actual or scheduled date the guest checked-in. For cruise, the cruise
    # departure date, also known as the sail date.
    # [Optional]
    # format: date (YYYY-MM-DD)
    check_in_date: str
    # For lodging, the actual or scheduled date the guest checked-out. For cruise, the cruise
    # return date, also known as the sail end date.
    # [Optional]
    # format: date (YYYY-MM-DD)
    check_out_date: str
    # The address details of the accommodation. The spec defines only address_line1 and zip
    # on this object.
    # [Optional]
    address: AccommodationAddress
    # The state or province of the address country (ISO 3166-2 code of up to two alphanumeric
    # characters). A free-form string, not a country code: the spec's example is "FL".
    # [Optional]
    state: str
    # The ISO country code of the address. A free-form string rather than an alpha-2 enum: the
    # spec's example is the three-letter code "USA".
    # [Optional]
    country: str
    # The address city.
    # [Optional]
    city: str
    # The total number of rooms booked for the accommodation.
    # [Optional]
    number_of_rooms: int
    # Contains information about the guests staying at the accommodation.
    # [Optional]
    guests: list  # AccommodationGuest
    # Contains information about the rooms booked by the customer.
    # [Optional]
    room: list  # AccommodationRoom
    # The property's phone information.
    # [Optional]
    property_phone: list  # AccommodationPhone
    # The customer service phone information.
    # [Optional]
    customer_service_phone: list  # AccommodationPhone


class Aggregator:
    """Information about the payment aggregator."""
    # The sub-merchant ID.
    # [Optional]
    sub_merchant_id: str
    # The Visa identifier for the payment aggregator.
    # [Optional]
    aggregator_id_visa: str
    # The Mastercard identifier for the payment aggregator.
    # [Optional]
    aggregator_id_mc: str


class ProcessingSettings:
    """Settings that control how the payment is processed.

    Shared across several request shapes. POST /payments resolves to PaymentRequestProcessing,
    while hosted payments, payment links and payment sessions resolve to the wider
    PaymentInterfacesProcessing. An attribute is therefore not necessarily read by every endpoint
    that accepts this object; the attributes below name the exceptions.
    """
    # The number provided by the cardholder. A purchase order or invoice number may be used.
    # [Optional]
    # max 15 characters
    order_id: str
    # The total amount of sales tax on the total purchase amount.
    # [Optional]
    # minimum 0
    tax_amount: float
    # The discount amount applied to the transaction by the merchant.
    # [Optional]
    # minimum 0
    discount_amount: float
    # The total charges for any import or export duty included in the transaction.
    # [Optional]
    # minimum 0
    duty_amount: float
    # The total freight or shipping and handling charges for the transaction.
    # [Optional]
    # minimum 0
    shipping_amount: float
    # The tax amount of the freight or shipping and handling charges for the transaction.
    # [Optional]
    # minimum 0
    shipping_tax_amount: float
    # Indicates if the payment is an Account Funding Transaction.
    # [Optional]
    aft: bool
    # The preferred scheme for co-badged card payment processing. If performing 3DS through a
    # third party, set this to the scheme that processed 3DS.
    # [Optional]
    # One of: mastercard, visa, cartes_bancaires
    preferred_scheme: PreferredSchema
    # Indicates the reason for a merchant-initiated payment request.
    # [Optional]
    # One of: Delayed_charge, Resubmission, No_show, Reauthorization
    merchant_initiated_reason: MerchantInitiatedReason
    # Unique number of the campaign this payment runs in. Only required for Afterpay campaign
    # invoices.
    # [Optional]
    campaign_id: int
    # Product type of the payment. Required when source.type is wechatpay.
    # [Optional]
    product_type: ProductType
    # Value obtained from the WeChat Web Authorization API before initiating Official Account or
    # Mini Program payments. Required if source.type is wechatpay.
    # [Optional]
    open_id: str
    # The payment for a merchant's order may be split; the original order price indicates the
    # transaction amount of the entire order.
    # [Optional]
    # minimum 0
    original_order_amount: float
    # Merchant receipt ID.
    # [Optional]
    # max 32 characters
    receipt_id: str
    # The client-side terminal type: a website opened in a desktop browser, a mobile browser, or
    # a mobile application.
    # [Optional]
    # One of: APP, WAP, WEB
    terminal_type: TerminalType
    # The operating system type. Required when terminal_type is not WEB.
    # [Optional]
    # One of: ANDROID, IOS
    os_type: OsType
    # Invoice ID number.
    # [Optional]
    # max 127 characters
    invoice_id: str
    # The label that overrides the business name in the PayPal account on the PayPal pages.
    # [Optional]
    # max 127 characters
    brand_name: str
    # The language and region of the customer in ISO 639-2 language code; the value consists of
    # language-country.
    # [Optional]
    # pattern ^[a-z]{2}(?:-[A-Z][a-z]{3})?(?:-(?:[A-Z]{2}))?$
    # 2 to 10 characters
    locale: str
    # Shipping preference. Declared on PaymentContextProcessing only, so it is read by
    # POST /payment-contexts and not by POST /payments, hosted payments or payment links.
    # [Optional]
    # One of: no_shipping, set_provided_address, get_from_file
    shipping_preference: ShippingPreference
    # Property required by PayPal to have an appropriate payment flow. Declared on
    # PaymentContextProcessing only.
    # [Optional]
    # One of: pay_now, continue
    user_action: UserAction
    # Not in the current specification, neither NAS nor Previous (ABC). The gateway discards it.
    # Retained for backwards compatibility.
    # [Optional]
    set_transaction_context: list  # dict
    # Contains information about the airline ticket and flights booked by the customer.
    # [Optional]
    airline_data: list  # AirlineData
    # One time password sent to the customer by SMS. Declared on the payment contexts payment
    # request and on the capture request, not on PaymentRequestProcessing.
    # [Optional]
    # max 50 characters
    otp_value: str
    # The two-letter ISO country code of the purchase country.
    # [Optional]
    # max 2 characters
    purchase_country: Country
    # Promo codes. They define which of the configured payment options within a payment category
    # (pay_later, pay_over_time, and so on) are shown for this purchase.
    # [Optional]
    custom_payment_method_ids: list  # str
    # A URL you can use to notify the customer that the order has been created.
    # [Optional]
    merchant_callback_url: str
    # The line of business for the payment. Beta.
    # [Optional]
    line_of_business: str
    # Not in the current specification, neither NAS nor Previous (ABC). The gateway discards it.
    # Retained for backwards compatibility.
    # [Optional]
    shipping_delay: int
    # Not in the current specification, neither NAS nor Previous (ABC). The gateway discards it.
    # Retained for backwards compatibility.
    # [Optional]
    shipping_info: list  # ShippingInfo
    # Previous API (ABC) only; absent from the NAS processing schemas.
    # [Optional]
    dlocal: DLocalProcessingSettings
    # Previous API (ABC) only, and not in any available specification. See the SenderInformation
    # class. Left exactly as it was on purpose: the serializer sends this as sender_information,
    # and there is no evidence establishing which key, if either, the gateway reads, so no
    # _KEYS_TRANSFORMATIONS entry overrides it.
    # [Optional]
    sender_information: SenderInformation
    # Not declared on any processing schema in either specification. The name appears elsewhere
    # in the spec on unrelated objects. The gateway discards it here.
    # [Optional]
    purpose: str
    # Key-and-value pairs with merchant-specific data for the transaction.
    # [Optional]
    # The specification declares this as a single object with `key` and `value`, even though
    # its description calls it "an array of key-and-value pairs". The sandbox accepts both a
    # bare object and an array; Java, .NET, Go and Ruby all model the declared single object,
    # so this follows them rather than keeping a third shape in the family.
    partner_customer_risk_data: PartnerCustomerRiskData
    # Contains information about the accommodation booked by the customer.
    # [Optional]
    accommodation_data: list  # AccommodationData
    # Surcharge amount applied to the transaction by the merchant, in the minor currency unit.
    # [Optional]
    # minimum 0
    surcharge_amount: int
    # Specifies the preferred type of Primary Account Number (PAN) for the payment. Only applies
    # when source.type is a card, instrument or token.
    # [Optional]
    # One of: fpan, dpan
    pan_preference: PanPreference
    # Indicates whether to provision a network token for the payment.
    # [Optional]
    provision_network_token: bool
    # The unique identifier for Visa-registered ramp providers. Required if you are a
    # Visa-registered ramp provider operating with affiliates.
    # [Optional]
    # pattern ^[a-zA-Z0-9]{1,15}$
    # max 15 characters
    affiliate_id: str
    # The affiliate URL. Required if you are a Visa-registered ramp provider operating with
    # affiliates.
    # [Optional]
    affiliate_url: str
    # Information about the payment aggregator.
    # [Optional]
    aggregator: Aggregator
    # Specifies whether to process the payment as a credit or debit transaction, if a combo card
    # is used. Required for domestic payments in Brazil.
    # [Optional]
    # One of: credit, debit
    card_type: CardFundingType
    # The foreign retailer amount the merchant applied to the transaction, in the minor currency
    # unit.
    # [Optional]
    # minimum 0
    foreign_retailer_amount: int
    # The transaction identifier used to track a payment request.
    # [Optional]
    reconciliation_id: str
    # Specifies which ACH service to use for the payment, if you set source.type to ach.
    # [Optional]
    # One of: same_day, standard
    service_type: ServiceType
    # The customer's 6-digit Blik code. Required when source.type is blik and merchant_initiated
    # is false (for example, for Regular payments and the initial payment of a Recurring
    # agreement).
    # [Optional]
    # pattern ^\d{6}$
    # 6 characters
    partner_code: str
    # The speed at which the payout or the unreferenced refund is processed. Only applicable for
    # unreferenced refunds. Not declared on any processing component schema; it appears only in
    # the inline processing objects of card payouts and unreferenced refunds.
    # [Optional]
    # Enum: "fast"
    processing_speed: str
    # The scheme transaction link identifier.
    # [Optional]
    scheme_transaction_link_id: str


class ItemType(str, Enum):
    DIGITAL = 'digital'
    DISCOUNT = 'discount'
    PHYSICAL = 'physical'


class ProductSubType(str, Enum):
    BLOCKCHAIN = 'blockchain'
    CBDC = 'cbdc'
    CRYPTOCURRENCY = 'cryptocurrency'
    NFT = 'nft'
    STABLECOIN = 'stablecoin'


class Product:
    type: ItemType = None
    sub_type: ProductSubType = None
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


class PaymentSegment:
    """The dimension details about business segment for payment request. At least one dimension
    required.
    """
    # The brand of business segment.
    # [Optional]
    # max 50 characters
    brand: str
    # The category of business segment.
    # [Optional]
    # max 50 characters
    business_category: str
    # The market of business segment.
    # [Optional]
    # max 50 characters
    market: str


class DowntimeRetryRequest:
    enabled: bool


class DunningRetryRequest:
    enabled: bool
    max_attempts: int
    end_after_days: int


class PaymentRetryRequest:
    enabled: bool
    max_attempts: int
    end_after_days: int
    downtime: DowntimeRetryRequest
    dunning: DunningRetryRequest


# Request Payment
class PartialAuthorization:
    enabled: bool


class PaymentAuthenticationRequest:
    preferred_experiences: list  # AuthenticationExperience


class PaymentRoutingAttempt:
    scheme: RoutingScheme


class PaymentRouting:
    attempts: list  # PaymentRoutingAttempt


class PaymentSubscription:
    id: str


class PaymentPlan:
    days_between_payments: int
    total_number_of_payments: int
    current_payment_number: int
    expiry: str
    amount: int
    name: str
    start_date: str


class PlanInstallment(PaymentPlan):
    financing: bool
    amount: str


class PlanRecurring(PaymentPlan):
    amount_variability: AmountVariability


class PaymentRequest:
    payment_context_id: str
    source: PaymentRequestSource
    fallback_source: PaymentRequestSource
    amount: int
    currency: Currency
    payment_type: PaymentType
    merchant_initiated: bool
    reference: str
    description: str
    authorization_type: AuthorizationType
    partial_authorization: PartialAuthorization
    capture: bool
    capture_on: datetime
    expire_on: datetime
    customer: PaymentCustomerRequest
    billing_descriptor: BillingDescriptor
    shipping: ShippingDetails
    segment: PaymentSegment
    three_ds: ThreeDsRequest
    authentication: PaymentAuthenticationRequest
    processing_channel_id: str
    previous_payment_id: str
    risk: RiskRequest
    success_url: str
    failure_url: str
    payment_ip: str
    sender: PaymentSender
    recipient: PaymentRecipient
    # @deprecated marketplace property will be removed in the future, and should be used amount_allocations instead
    marketplace: MarketplaceData
    amount_allocations: list  # values of AmountAllocations
    processing: ProcessingSettings
    metadata: dict
    items: list  # payments.Product
    retry: PaymentRetryRequest
    instruction: PaymentInstruction
    payment_plan: PaymentPlan
    routing: PaymentRouting
    subscription: PaymentSubscription


# Payout Request Source
class PayoutRequestSource:
    """The source of a card payout, bank payout or unreferenced refund."""
    # The payout or unreferenced refund source type. Set by each subclass.
    # [Required]
    type: PayoutSourceType

    def __init__(self, type_p: PayoutSourceType):
        self.type = type_p


class PayoutRequestCurrencyAccountSource(PayoutRequestSource):
    """A currency account source (type currency_account).

    Used by card payouts, bank payouts and unreferenced refunds.
    """
    # The ID of the currency account that will fund the payout or the unreferenced refund. For
    # bank payouts, its holding currency must match the payout's currency.
    # [Required]
    # ^(ca)_(\w{26})$
    # min 29 characters
    # max 29 characters
    id: str

    def __init__(self):
        super().__init__(PayoutSourceType.CURRENCY_ACCOUNT)


class PayoutRequestEntitySource(PayoutRequestSource):
    id: str

    def __init__(self):
        super().__init__(PayoutSourceType.ENTITY)


# Payment Request Destination
class PaymentRequestDestination:
    """The destination of the payout or of the unreferenced refund.

    You can encrypt this field by using the Cko-Encryption-Key-Id and Cko-Encrypted-Properties
    headers.
    """
    # The payout or unreferenced refund destination type. Set by each subclass.
    # [Required]
    type: PaymentDestinationType

    def __init__(self, type_p: PaymentDestinationType):
        self.type = type_p


class PaymentBankAccountDestination(PaymentRequestDestination):
    """A bank account payout destination (bank payout, type bank_account)."""
    # The type of the bank account. Note that some beneficiary banks do not accept payouts to
    # savings accounts.
    # [Required]
    account_type: AccountType
    # Number (which can contain letters) that identifies the local account.
    # [Optional]
    account_number: str
    # Code that identifies the bank. Also referred as Routing Number in the United States.
    # [Optional]
    bank_code: str
    # The combination of bank code and/or branch code and account number.
    # [Optional]
    bban: str
    # Code that identifies the bank branch.
    # [Optional]
    branch_code: str
    # Internationally agreed standard for identifying bank accounts. Lengths vary per
    # destination_country.
    # [Optional]
    iban: str
    # 8 or 11 character code which identifies the bank or bank branch.
    # [Optional]
    swift_bic: str
    # The two-letter ISO country code of where the account is based. Note that not all
    # countries are available.
    # [Required]
    # min 2 characters
    # max 2 characters
    country: Country
    # The account holder details.
    # [Optional]
    account_holder: AccountHolder
    # The bank details.
    # [Optional]
    # Deprecated: not in the current specification of the bank account payout destination, so the
    # API does not define it. Retained for backwards compatibility. Will be removed in the next
    # major version.
    bank: BankDetails

    def __init__(self):
        super().__init__(PaymentDestinationType.BANK_ACCOUNT)


class PaymentRequestIdDestination(PaymentRequestDestination):
    """A payment instrument payout destination (type id).

    Valid for card payouts, bank payouts and unreferenced refunds.
    """
    # The payment source ID. This will be an ID with the prefix src_.
    # [Required]
    # ^(src)_(\w{26})$
    # min 30 characters
    # max 30 characters
    id: str
    # The payout destination account holder. Required for card payouts, where this position
    # accepts only type and first_name, middle_name, last_name (individual) or company_name
    # (corporate, government). Optional for unreferenced refunds, where this position accepts
    # type (individual, corporate, government); first_name, middle_name and last_name (max 50
    # characters each), date_of_birth (YYYY-MM-DD) and country_of_birth for individual;
    # company_name for corporate and government; and billing_address, phone, identification and
    # email (max 255 characters) for all three.
    # [Optional]
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(PaymentDestinationType.ID)


class PaymentRequestCardDestination(PaymentRequestDestination):
    """A card destination (type card), for card payouts and unreferenced refunds."""
    # The card number. You can encrypt this field by using the Cko-Encryption-Key-Id and
    # Cko-Encrypted-Properties headers.
    # [Required]
    # max 19 characters
    number: str
    # The card's expiration month.
    # [Required]
    expiry_month: int
    # The card's expiration year.
    # [Required]
    expiry_year: int
    # The destination account holder, for card payouts and unreferenced refunds. This position
    # accepts type (individual, corporate, government); first_name, middle_name and last_name
    # (max 50 characters each), date_of_birth (YYYY-MM-DD) and country_of_birth for individual;
    # company_name for corporate and government; and billing_address, phone, identification and
    # email (max 255 characters) for all three. For unreferenced refunds, first_name and
    # last_name are required for individual, and company_name for corporate and government.
    # [Required]
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(PaymentDestinationType.CARD)


class PaymentRequestNetworkTokenDestination(PaymentRequestDestination):
    """A network token destination (type network_token), for card payouts and unreferenced refunds.

    Leave cryptogram and eci unset when not used: assigning None sends null.
    """
    # The network token's Primary Account Number (PAN).
    # [Required]
    token: str
    # The network token's expiration month.
    # [Required]
    # min 1
    expiry_month: int
    # The network token's expiration year.
    # [Required]
    expiry_year: int
    # The network token type.
    # [Required]
    token_type: NetworkTokenType
    # The network token's Base64-encoded cryptographic identifier (TAVV). The cryptogram is
    # used by card schemes to validate the token verification result.
    # [Optional]
    # max 50 characters
    cryptogram: str
    # The network token's Electronic Commerce Indicator (ECI) security level.
    # [Optional]
    # max 2 characters
    eci: str
    # The destination account holder, for card payouts and unreferenced refunds. This position
    # accepts type (individual, corporate, government); first_name, middle_name and last_name
    # (max 50 characters each), date_of_birth (YYYY-MM-DD) and country_of_birth for individual;
    # company_name for corporate and government; and billing_address, phone, identification and
    # email (max 255 characters) for all three. For unreferenced refunds, first_name and
    # last_name are required for individual, and company_name for corporate and government.
    # [Required]
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(PaymentDestinationType.NETWORK_TOKEN)


class PaymentRequestTokenDestination(PaymentRequestDestination):
    """A token destination (type token), for card payouts and unreferenced refunds."""
    # The Checkout.com card token ID. This will be an ID with the prefix tok_.
    # [Required]
    # ^(tok)_(\w{26})$
    # min 30 characters
    # max 30 characters
    token: str
    # The destination account holder. Required for card payouts, where this position accepts
    # only type and first_name, middle_name, last_name (individual) or company_name (corporate,
    # government). Optional for unreferenced refunds, where this position accepts type
    # (individual, corporate, government); first_name, middle_name and last_name (max 50
    # characters each), date_of_birth (YYYY-MM-DD) and country_of_birth for individual;
    # company_name for corporate and government; and billing_address, phone, identification and
    # email (max 255 characters) for all three.
    # [Required] for card payouts, [Optional] for unreferenced refunds
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(PaymentDestinationType.TOKEN)


# Request Payout
class PayoutRequest:
    """A card payout or bank payout request, sent to POST /payments."""
    # The source of the payout. For bank payouts, the source from which the payout is funded.
    # [Required]
    source: PayoutRequestSource
    # The destination of the payout. You can encrypt this field by using the Cko-Encryption-Key-Id
    # and Cko-Encrypted-Properties headers. Card payouts take PaymentRequestCardDestination,
    # PaymentRequestNetworkTokenDestination, PaymentRequestIdDestination or
    # PaymentRequestTokenDestination; bank payouts take PaymentRequestIdDestination or
    # PaymentBankAccountDestination.
    # [Required]
    destination: PaymentRequestDestination
    # The amount to pay out, in minor units.
    # [Optional] for card payouts, [Required] for bank payouts
    # min 0
    amount: int
    # The three-letter ISO 4217 code for the currency you want to pay out to the recipient. For bank
    # payouts, it should match the currency of the destination account.
    # [Required]
    currency: Currency
    # A custom reference to identify the payout. For example, an order number.
    # [Optional]
    # max 50 characters for card payouts
    reference: str
    # The billing descriptor for bank payouts. Beneficiary banks typically construct it using the
    # billing descriptor reference and the sender information.
    # [Required] for bank payouts, not used by card payouts
    billing_descriptor: PayoutBillingDescriptor
    # The sender of the payout. Required for money transfer card payouts. For bank payouts, the
    # ultimate sender of the payout, that is, your customer; not supported for Platform or Direct
    # Seller Checkout.com clients.
    # [Optional]
    sender: PaymentSender
    # Additional details about the payout instruction.
    # [Required] for card payouts, [Optional] for bank payouts
    instruction: PaymentInstruction
    # The unique identifier for the processing channel.
    # [Required]
    # ^(pc)_(\w{26})$
    # min 29 characters
    # max 29 characters
    processing_channel_id: str
    # The dimension details about business segment for payment request. At least one dimension
    # required.
    # [Optional]
    segment: PaymentSegment
    # The order's line items. Card payouts only.
    # [Optional]
    items: list  # payments.Product
    # Stores additional information about the transaction with custom fields. Card payouts only.
    # [Optional]
    metadata: dict
    # The identifier of an existing payment from the recurring series, if the payout is a recurring
    # payment that uses stored card details. Card payouts only.
    # [Optional]
    previous_payment_id: str
    # Information related to the processing of the payout. Card payouts only.
    # [Optional]
    processing: ProcessingSettings


# Request Unreferenced Refund
class UnreferencedRefundRequest:
    """An unreferenced refund request, sent to POST /payments.

    payment_type is set to UnreferencedRefund by the constructor.
    """
    # The source of the unreferenced refund. Takes PayoutRequestCurrencyAccountSource.
    # [Required]
    source: PayoutRequestSource
    # The destination of the unreferenced refund. Takes PaymentRequestCardDestination,
    # PaymentRequestNetworkTokenDestination, PaymentRequestIdDestination or
    # PaymentRequestTokenDestination.
    # [Required]
    destination: PaymentRequestDestination
    # Additional details about the unreferenced refund instruction. Uses purpose and
    # funds_transfer_type. funds_transfer_type is required if processing.processing_speed is
    # fast; its value should be based on the destination card scheme: for Visa, use MI; for
    # Mastercard, use C60. purpose is required if the card's issuer_country is one of AR, BD,
    # CL, CO, EG, IN or MX; Enum: "family_support" "expatriation" "travel_and_tourism"
    # "education" "medical_treatment" "emergency_need" "leisure" "savings" "gifts" "donations"
    # "financial_services" "it_services" "investment" "insurance" "loan_payment" "pension"
    # "royalties" "other" "income".
    # [Optional]
    instruction: PaymentInstruction
    # The amount in minor currency.
    # [Required]
    # Format: int64
    # min 1
    # max 9999999999
    amount: int
    # The three-letter ISO currency code of the payment.
    # [Required]
    # min 3 characters
    # max 3 characters
    currency: Currency
    # The type of the payment. Set to UnreferencedRefund by the constructor.
    # [Required]
    # Enum: "UnreferencedRefund"
    payment_type: str
    # The processing channel identifier.
    # [Required]
    # ^(pc)_(\w{26})$
    processing_channel_id: str
    # An internal reference you can later use to identify this payment.
    # [Optional]
    reference: str
    # A set of key-value pairs that you can attach to the refund request. It can be useful for
    # storing additional information in a structured format. This object only allows one level
    # of depth, so cannot accept non-primitive data types such as objects or arrays.
    # [Optional]
    metadata: dict
    # The previous related payment identifier. This could be the ID of the payment that you want
    # to refund.
    # [Optional]
    previous_payment_id: str
    # The dimension details about business segment for payment request. At least one dimension
    # required.
    # [Optional]
    segment: PaymentSegment
    # Returns information related to the processing of the payment. Uses processing_speed.
    # [Optional]
    processing: ProcessingSettings

    def __init__(self):
        self.payment_type = 'UnreferencedRefund'


# Query
class PaymentsQueryFilter:
    limit: int
    skip: int
    reference: str


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
    # @deprecated marketplace property will be removed in the future, and should be used amount_allocations instead
    marketplace: MarketplaceData
    amount_allocations: list  # values of AmountAllocations
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
    # Not available on Previous
    amount_allocations: list  # values of AmountAllocations
    capture_action_id: str
    destination: PaymentBankAccountDestination
    items: list  # payments.Product


# Voids
class VoidRequest:
    # If not specified, the full payment amount is voided (min 0, max 9999999999)
    amount: int
    reference: str
    metadata: dict


# Cancellations
class CancelScheduledRetryRequest:
    reference: str


# Reversals
class ReversePaymentRequest:
    reference: str
    metadata: dict


# Search
class PaymentsSearchRequest(QueryFilterDateRange):
    query: str
    limit: int


class BillingPlan:
    type: BillingPlanType
    skip_shipping_address: bool
    immutable_shipping_address: bool


class FawryProduct:
    product_id: str
    quantity: int
    price: int
    description: str


class PaymentMethodDetails:
    display_name: str
    type: str
    network: str
