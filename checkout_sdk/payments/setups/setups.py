from __future__ import absolute_import
from datetime import datetime
from enum import Enum

from checkout_sdk.common.common import Address, Phone
from checkout_sdk.common.enums import Currency
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
    registration_date: str  # Format: yyyy-MM-dd
    last_modified: str  # Format: yyyy-MM-dd
    returning_customer: bool
    first_transaction_date: str  # Format: yyyy-MM-dd
    last_transaction_date: str  # Format: yyyy-MM-dd
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
    # readOnly: the account holder details returned by Klarna after the shopper completes
    # verification (swagger KlarnaAccountHolder).
    name: str


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
class SetupsSepaMandateType(str, Enum):
    """The type of SEPA mandate on a Payment Setup.

    The Sepa.mandate.type schema declares these values lowercase. The payment-source and
    instrument positions declare them capitalized - see common.enums.SepaMandateType.
    Named apart so the two casings cannot be mixed up.
    """
    CORE = 'core'
    B2B = 'b2b'


class SepaMandate:
    id: str
    type: SetupsSepaMandateType
    date_of_signature: str  # Format: yyyy-MM-dd


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


# Bacs entities
class BacsAccountHolderType(str, Enum):
    INDIVIDUAL = 'individual'
    CORPORATE = 'corporate'


class BacsAccountHolder:
    type: BacsAccountHolderType
    first_name: str
    last_name: str
    company_name: str
    email: str


class Bacs(PaymentMethodBase):
    instrument_id: str
    account_holder: BacsAccountHolder
    account_number: str
    bank_code: str
    country: str
    currency: Currency
    allow_partial_match: bool


# Card Present entities
class CardPresentPin:
    key_set_id: str
    block: str
    block_format: str


class CardPresent(PaymentSetupPaymentMethod):
    track2: str
    emv: str
    entry_mode: str
    pin: CardPresentPin
    store_for_future_use: bool
    name: str


# Pay by Bank entities
class PayByBankBank:
    bank_id: str
    display_name: str
    logo_url: str
    available: bool


class PayByBankActionType(str, Enum):
    SELECT_BANK = 'select_bank'


class PayByBankAction:
    type: PayByBankActionType
    banks: list  # list of PayByBankBank


class PayByBank(PaymentSetupPaymentMethod):
    bank_id: str
    action: PayByBankAction


# Stablecoin entities
class Stablecoin(PaymentSetupPaymentMethod):
    pass


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
    bacs: Bacs
    card_present: CardPresent
    pay_by_bank: PayByBank
    stablecoin: Stablecoin


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
    registration_date: str  # Format: yyyy-MM-dd


class AmountAllocationCommission:
    amount: int
    percentage: float


class PaymentSetupAmountAllocation:
    id: str  # required
    amount: int  # required
    reference: str
    commission: AmountAllocationCommission


class Order:
    items: list  # list of PaymentContextsItems
    shipping: ShippingDetails
    sub_merchants: list  # list of OrderSubMerchant
    discount_amount: int
    invoice_id: str
    shipping_amount: int
    tax_amount: int
    tipping_amount: int
    surcharge_amount: int
    amount_allocations: list  # list of PaymentSetupAmountAllocation


# Industry entities

class PaymentSetupAccommodationAddress:
    """The accommodation's address."""
    # The first line of the address.
    # [Optional]
    address_line1: str
    # The address city.
    # [Optional]
    city: str
    # The address state or county.
    # [Optional]
    state: str
    # The address country, in ISO 3166-1 alpha-2 format.
    # [Optional]
    country: str
    # The zip code or postal code.
    # [Optional]
    zip: str


class PaymentSetupAccommodationGuest:
    """A guest staying at the accommodation."""
    # The guest's first name.
    # [Optional]
    first_name: str
    # The guest's last name.
    # [Optional]
    last_name: str
    # The guest's date of birth.
    # [Optional]
    # format: date (YYYY-MM-DD)
    date_of_birth: str


class PaymentSetupAccommodationRoom:
    """A room booked by the customer."""
    # The rate or cost of the room per day.
    # [Optional]
    rate: float
    # The number of nights the room is booked for.
    # [Optional]
    number_of_nights: int
    # The room class or type booked. For example, `deluxe`. Free-form string, not an enum.
    # [Optional]
    type: str


class PaymentSetupAccommodationHost:
    """Details about the host of the accommodation."""
    # The date the host registered.
    # [Optional]
    # format: date (YYYY-MM-DD)
    registration_date: str
    # The total number of reservations the host has received.
    # [Optional]
    total_reservation_count: int


class PaymentSetupAccommodation:
    """Details about the accommodation booking. For lodging or cruise bookings."""
    # For lodging, contains the lodging name that appears on the storefront/customer receipts.
    # For cruise, contains the ship name booked for the cruise.
    # [Optional]
    name: str
    # A unique identifier for the booking.
    # [Optional]
    booking_reference: str
    # For lodging bookings, the customer's check-in date.
    # For cruise bookings, the cruise departure date (sail date).
    # [Optional]
    # format: date (YYYY-MM-DD)
    check_in_date: str
    # For lodging bookings, the customer's check-out date.
    # For cruise bookings, the cruise return date.
    # [Optional]
    # format: date (YYYY-MM-DD)
    check_out_date: str
    # The accommodation's address.
    # [Optional]
    address: PaymentSetupAccommodationAddress
    # The total number of rooms booked for the accommodation.
    # [Optional]
    number_of_rooms: int
    # The list of guests staying at the accommodation.
    # [Optional]
    guests: list  # list of PaymentSetupAccommodationGuest
    # The list of rooms booked by the customer.
    # [Optional]
    room: list  # list of PaymentSetupAccommodationRoom
    # The total number of guests on the booking.
    # [Optional]
    total_number_of_guests: int
    # Specifies whether the booking is refundable.
    # [Optional]
    refundable: bool
    # The recipient the booking confirmation is delivered to.
    # [Optional]
    delivery_recipient: str
    # Details about the host of the accommodation.
    # [Optional]
    host: PaymentSetupAccommodationHost


class PaymentSetupAirlineTicket:
    """Details about the airline ticket."""
    # The ticket's unique identifier.
    # [Optional]
    number: str
    # The date the airline ticket was issued.
    # [Optional]
    # format: date (YYYY-MM-DD)
    issue_date: str
    # The carrier code of the ticket issuer.
    # [Optional]
    issuing_carrier_code: str
    # The travel package indicator, as one of the following codes: `A` (Airline flight
    # reservation), `B` (Car rental and airline reservation), `C` (Car rental reservation),
    # `N` (Unknown). Free-form string in the spec, not a typed enum.
    # [Optional]
    travel_package_indicator: str
    # The name of the travel agency.
    # [Optional]
    travel_agency_name: str
    # The IATA or ARC unique identifier for the travel agency that issues the ticket.
    # [Optional]
    travel_agency_code: str


class PaymentSetupAirlinePassengerAddress:
    """Details about the passenger's address."""
    # The two-letter ISO country code of the passenger's country of residence.
    # [Optional]
    country: str


class PaymentSetupAirlinePassenger:
    """A passenger on the flight."""
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
    # Details about the passenger's address.
    # [Optional]
    address: PaymentSetupAirlinePassengerAddress


class PaymentSetupFlightLegDetails:
    """A flight leg booked by the customer."""
    # The flight identifier.
    # [Optional]
    flight_number: str
    # The IATA 2-letter accounting code (PAX) that identifies the carrier. Required if the
    # airline data includes leg details.
    # [Optional]
    carrier_code: str
    # A one-letter identifier for the travel class. For example: `F` (First class),
    # `J` (Business class), `W` (Premium economy class), `Y` (Economy class).
    # [Optional]
    class_of_travelling: str
    # The IATA three-letter airport code for the departure airport. Required if the
    # airline data includes leg details.
    # [Optional]
    departure_airport: str
    # The date of the scheduled take-off.
    # [Optional]
    # format: date (YYYY-MM-DD)
    departure_date: str
    # The time of the scheduled take-off.
    # [Optional]
    departure_time: str
    # The IATA three-letter airport code for the destination airport. Required if the
    # airline data includes leg details.
    # [Optional]
    arrival_airport: str
    # A one-letter code that indicates whether the passenger is entitled to make a stopover.
    # Specify `O` or a blank space if the passenger is entitled. Specify `X` if not entitled.
    # [Optional]
    stop_over_code: str
    # The alphanumeric fare basis code.
    # [Optional]
    fare_basis_code: str


class PaymentSetupAirlineInsurancePrice:
    """The price of the travel insurance."""
    # The insurance amount, in the minor currency unit.
    # [Optional]
    amount: float
    # The currency of the insurance amount, as a three-letter ISO currency code.
    # [Optional]
    currency: str


class PaymentSetupAirlineInsurance:
    """Details about the travel insurance purchased with the booking."""
    # The type of insurance.
    # [Optional]
    type: str
    # The name of the insurance company.
    # [Optional]
    company: str
    # The price of the insurance.
    # [Optional]
    price: PaymentSetupAirlineInsurancePrice


class PaymentSetupAirline:
    """Details about the airline ticket and flights the customer booked."""
    # Details about the airline ticket.
    # [Optional]
    ticket: PaymentSetupAirlineTicket
    # The list of passengers on the flight.
    # [Optional]
    passengers: list  # list of PaymentSetupAirlinePassenger
    # The list of flight legs booked by the customer.
    # [Optional]
    flight_leg_details: list  # list of PaymentSetupFlightLegDetails
    # The total number of passengers on the booking.
    # [Optional]
    total_number_of_passengers: int
    # The type of travel. For example, `domestic` or `international`. Free-form string,
    # not a typed enum.
    # [Optional]
    travel_type: str
    # The type of trip. For example, `one_way` or `round_trip`. Free-form string,
    # not a typed enum.
    # [Optional]
    trip_type: str
    # Specifies whether the booking is refundable.
    # [Optional]
    refundable: bool
    # The recipient the ticket is delivered to.
    # [Optional]
    delivery_recipient: str
    # Any additional add-ons purchased with the booking. For example, `extra_baggage`.
    # A single string per the spec, not an array, despite the plural name.
    # [Optional]
    ancillaries: str
    # Details about the travel insurance purchased with the booking.
    # [Optional]
    insurance: PaymentSetupAirlineInsurance


class Industry:
    """Industry-specific information."""
    # The list of airline bookings associated with the payment.
    # [Optional]
    airline: list  # list of PaymentSetupAirline
    # The list of accommodation bookings associated with the payment.
    # [Optional]
    accommodation: list  # list of PaymentSetupAccommodation


# Billing entity
class PaymentSetupBilling:
    address: Address


class PaymentSetupBillingDescriptor:
    name: str
    city: str
    reference: str


class PaymentSetupPresentmentDetails:
    amount: int
    currency: str


class PaymentSetupTerminal:
    id: str
    local_date_time: str


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
    billing_descriptor: PaymentSetupBillingDescriptor
    presentment_details: PaymentSetupPresentmentDetails
    terminal: PaymentSetupTerminal
    account_funding_transaction: PaymentSetupAccountFundingTransaction
