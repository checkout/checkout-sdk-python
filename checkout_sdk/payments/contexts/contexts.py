from datetime import datetime

from checkout_sdk.common.common import Address
from checkout_sdk.common.enums import Currency, PaymentSourceType
from checkout_sdk.payments.payments import PaymentRequestSource, PaymentType, ShippingDetails, BillingPlan, \
    ShippingPreference, UserAction


class PaymentContextsPartnerCustomerRiskData:
    key: str
    value: str


class PaymentContextsTicket:
    number: str
    issue_date: datetime
    issuing_carrier_code: str
    travel_package_indicator: str
    travel_agency_name: str
    travel_agency_code: str


class PaymentContextsPassenger:
    first_name: str
    last_name: str
    date_of_birth: datetime
    address: Address


class PaymentContextsFlightLegDetails:
    flight_number: str
    carrier_code: str
    class_of_travelling: str
    departure_airport: str
    departure_date: datetime
    departure_time: str
    arrival_airport: str
    stop_over_code: str
    fare_basis_code: str


class PaymentContextsAirlineData:
    ticket: list  # payment.contexts.PaymentContextsTicket
    passenger: list  # payment.contexts.PaymentContextsPassenger
    flight_leg_details: list  # payment.contexts.PaymentContextsFlightLegDetails


class PaymentContextsProcessing:
    plan: BillingPlan
    shipping_amount: int
    invoice_id: str
    brand_name: str
    locale: str
    shipping_preference: ShippingPreference
    user_action: UserAction
    partner_customer_risk_data: PaymentContextsPartnerCustomerRiskData
    airline_data: list  # payment.contexts.PaymentContextsAirlineData


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
    capture: bool
    shipping: ShippingDetails
    processing: PaymentContextsProcessing
    processing_channel_id: str
    reference: str
    description: str
    success_url: str
    failure_url: str
    items: list  # payments.contexts.PaymentContextsItems


class PaymentContextPayPalSource(PaymentRequestSource):

    def __init__(self):
        super().__init__(PaymentSourceType.PAYPAL)
