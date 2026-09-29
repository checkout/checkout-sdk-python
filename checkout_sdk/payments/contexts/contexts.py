from deprecated import deprecated

from checkout_sdk.common.common import CustomerRequest, AccountHolder
from checkout_sdk.common.enums import Currency, PaymentSourceType
from checkout_sdk.payments.payments import PaymentRequestSource, PaymentType, ShippingDetails, BillingPlan, \
    ShippingPreference, UserAction, PassengerAddress


class PaymentContextsPartnerCustomerRiskData:
    """A key-and-value pair with merchant-specific data for the transaction."""
    # The key for the pair.
    # [Optional]
    key: str
    # The value for the pair.
    # [Optional]
    value: str


class PaymentContextsTicket:
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
    # airline flight reservations included, N = Unknown.
    # [Optional]
    travel_package_indicator: str
    # The name of the travel agency.
    # [Optional]
    travel_agency_name: str
    # The unique identifier from IATA or ARC for the travel agency that issues the ticket.
    # [Optional]
    travel_agency_code: str


class PaymentContextsPassenger:
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
    # Contains information about the passenger's address.
    # [Optional]
    #
    # The spec defines exactly one property on this object, country. This was the wider common
    # Address, whose other members the API does not read here. It now shares
    # payments.PassengerAddress so one spec shape maps to one class.
    address: PassengerAddress


class PaymentContextsFlightLegDetails:
    """Contains information about a flight leg booked by the customer."""
    # The flight identifier.
    # [Optional]
    flight_number: str
    # The IATA 2-letter accounting code (PAX) that identifies the carrier.
    # [Optional]
    carrier_code: str
    # A one-letter travel class identifier. The following are common: F = First class,
    # J = Business class, Y = Economy class, W = Premium economy.
    # [Optional]
    class_of_travelling: str
    # The IATA three-letter airport code of the departure airport.
    # [Optional]
    departure_airport: str
    # The date of the scheduled take off.
    # [Optional]
    # format: date (YYYY-MM-DD)
    departure_date: str
    # The time of the scheduled take off.
    # [Optional]
    departure_time: str
    # The IATA 3-letter airport code of the destination airport.
    # [Optional]
    arrival_airport: str
    # A one-letter code that indicates whether the passenger is entitled to make a stopover.
    # Can be a space, O if the passenger is entitled to make a stopover, or X if they are not.
    # [Optional]
    stop_over_code: str
    # The fare basis code, alphanumeric.
    # [Optional]
    fare_basis_code: str


class PaymentContextsAirlineData:
    """Contains information about the airline ticket and flights booked by the customer."""
    # Contains information about the airline ticket.
    # [Optional]
    #
    # The spec declares this as a single object. It was annotated as a list, so the SDK sent an
    # array, a shape the API does not accept.
    ticket: PaymentContextsTicket
    # Contains information about the passenger(s) on the flight.
    # [Optional]
    #
    # Assign a single PaymentContextsPassenger, not a one-element list. POST /payment-contexts
    # rejects the list form with 422 passenger_required and accepts a single object, verified
    # against the sandbox on 2026-09-25. See payments.AirlineData.passenger for the full
    # cross-surface matrix.
    passenger: PaymentContextsPassenger
    # Contains information about the flight leg(s) booked by the customer.
    # [Optional]
    flight_leg_details: list  # PaymentContextsFlightLegDetails


class PaymentContextsProcessing:
    """Settings that control how the payment context is processed."""
    # The plan details for a recurring payment with PayPal. Required when payment_type is
    # recurring.
    # [Optional]
    plan: BillingPlan
    # The total freight or shipping and handling charges for the transaction.
    # [Optional]
    shipping_amount: float
    # Invoice ID number.
    # [Optional]
    invoice_id: str
    # The label that overrides the business name in the PayPal account on the PayPal pages.
    # [Optional]
    brand_name: str
    # The language and region of the customer in ISO 639-2 language code; the value consists of
    # language-country.
    # [Optional]
    locale: str
    # Shipping preference.
    # [Optional]
    # One of: no_shipping, set_provided_address, get_from_file
    shipping_preference: ShippingPreference
    # Property required by PayPal to have an appropriate payment flow.
    # [Optional]
    # One of: pay_now, continue
    user_action: UserAction
    # Key-and-value pairs with merchant-specific data for the transaction.
    # [Optional]
    partner_customer_risk_data: list  # PaymentContextsPartnerCustomerRiskData
    # Contains information about the airline ticket and flights booked by the customer.
    # [Optional]
    airline_data: list  # PaymentContextsAirlineData
    # Contains information about the accommodation booked by the customer. Uses the shared
    # payments.AccommodationData: payment contexts, POST /payments and the GET /payments/{id}
    # response all resolve accommodation_data to the same specification schema.
    # [Optional]
    accommodation_data: list  # payments.AccommodationData
    # Promo codes. They define which of the configured payment options within a payment
    # category (pay_later, pay_over_time, and so on) are shown for this purchase.
    # [Optional]
    custom_payment_method_ids: list  # str
    # The discount amount the merchant applied to the transaction.
    # [Optional]
    discount_amount: float
    # The total tax amount for the transaction, in the minor currency unit.
    # [Optional]
    tax_amount: float


class PaymentContextsItems:
    name: str
    quantity: int
    unit_price: int
    reference: str
    total_amount: int
    tax_amount: int
    discount_amount: int
    url: str
    image_url: str


class PaymentContextsRequest:
    source: PaymentRequestSource
    amount: int
    currency: Currency
    payment_type: PaymentType
    authorization_type: str
    capture: bool
    customer: CustomerRequest
    shipping: ShippingDetails
    processing: PaymentContextsProcessing
    processing_channel_id: str
    reference: str
    description: str
    success_url: str
    failure_url: str
    items: list  # payments.contexts.PaymentContextsItems
    metadata: dict


@deprecated("This class will be removed in the future. Use PaymentContextPaypalSource instead")
class PaymentContextPayPalSource(PaymentRequestSource):

    def __init__(self):
        super().__init__(PaymentSourceType.PAYPAL)


class PaymentContextPaypalSource(PaymentRequestSource):

    def __init__(self):
        super().__init__(PaymentSourceType.PAYPAL)


class PaymentContextKlarnaSource(PaymentRequestSource):
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(PaymentSourceType.KLARNA)
