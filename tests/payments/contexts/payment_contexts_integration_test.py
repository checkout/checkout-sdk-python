from __future__ import absolute_import

import os
import pytest

from checkout_sdk.common.common import AccountHolder, Address
from checkout_sdk.common.enums import Currency, Country
from checkout_sdk.payments.contexts.contexts import PaymentContextsRequest, PaymentContextsItems, \
    PaymentContextPaypalSource, PaymentContextKlarnaSource, PaymentContextsProcessing, \
    PaymentContextsAirlineData, PaymentContextsFlightLegDetails, PaymentContextsPassenger, \
    PaymentContextsTicket
from checkout_sdk.payments.payments import PaymentType, PassengerAddress
from tests.checkout_test_utils import assert_response, APM_SERVICE_UNAVAILABLE, check_error_item


@pytest.mark.skip(reason='PayPal APM service unavailable in sandbox: apm_service_unavailable')
def test_should_create_and_get_payment_context_details(default_api):
    request = create_payment_contexts_request()

    response = default_api.contexts.create_payment_contexts(request)

    assert_response(response,
                    'http_metadata',
                    'id',
                    'partner_metadata.order_id')

    payment_contexts_details = default_api.contexts.get_payment_context_details(response.id)

    assert_response(payment_contexts_details,
                    'http_metadata',
                    'payment_request',
                    'payment_request.source',
                    'payment_request.amount',
                    'payment_request.currency',
                    'payment_request.payment_type',
                    'payment_request.capture',
                    'payment_request.items',
                    'payment_request.success_url',
                    'payment_request.failure_url',
                    'partner_metadata',
                    'partner_metadata.order_id')


def test_create_payment_contexts_klarna_request(default_api):
    processing = PaymentContextsProcessing()
    processing.locale = "en-GB"

    billing_address = Address()
    billing_address.country = Country.DE

    account_holder = AccountHolder()
    account_holder.billing_address = billing_address

    source = PaymentContextKlarnaSource()
    source.account_holder = account_holder

    items = PaymentContextsItems()
    items.name = 'mask'
    items.unit_price = 1000
    items.quantity = 1
    items.total_amount = 1000

    request = PaymentContextsRequest()
    request.source = source
    request.amount = 1000
    request.currency = Currency.EUR
    request.payment_type = PaymentType.REGULAR
    request.processing_channel_id = os.environ.get('CHECKOUT_PROCESSING_CHANNEL_ID')
    request.items = [items]
    request.processing = processing

    check_error_item(callback=default_api.contexts.create_payment_contexts,
                     error_item=APM_SERVICE_UNAVAILABLE,
                     payment_contexts_request=request)


def test_create_payment_contexts_with_airline_data(default_api):
    """Sends processing.airline_data to a live endpoint.

    POST /payment-contexts rejects the array form of passenger with 422 passenger_required and
    accepts a single object, which is the opposite of what the specification declares. Nothing
    else in this suite sends airline data anywhere, and the equivalent test in the Go SDK is what
    caught that mistake before it reached a merchant. A 422 here means the guidance documented on
    AirlineData.passenger no longer matches what the endpoint accepts.

    stop_over_code is deliberately omitted: this endpoint rejects it with
    flight_leg_detail_stop_over_code_invalid for every value tried, including the three its own
    description names and the one in the swagger example. Raised as a spec/API defect.
    """
    ticket = PaymentContextsTicket()
    ticket.number = '045-21351455613'
    ticket.issuing_carrier_code = 'AI'
    ticket.travel_package_indicator = 'B'

    # A single object, not a one-element list. See payments.AirlineData.passenger.
    passenger = PaymentContextsPassenger()
    passenger.first_name = 'John'
    passenger.last_name = 'White'
    passenger.address = PassengerAddress()
    passenger.address.country = Country.GB

    leg = PaymentContextsFlightLegDetails()
    leg.flight_number = '101'
    leg.carrier_code = 'BA'
    leg.class_of_travelling = 'J'
    leg.departure_airport = 'LHR'
    leg.arrival_airport = 'LAX'

    airline = PaymentContextsAirlineData()
    airline.ticket = ticket
    airline.passenger = passenger
    airline.flight_leg_details = [leg]

    processing = PaymentContextsProcessing()
    processing.airline_data = [airline]

    request = create_payment_contexts_request()
    request.processing = processing

    response = default_api.contexts.create_payment_contexts(request)

    assert_response(response, 'http_metadata', 'id')


def create_payment_contexts_request():
    source = PaymentContextPaypalSource()

    items = PaymentContextsItems()
    items.name = 'mask'
    items.unit_price = 1000
    items.quantity = 1
    items.total_amount = 1000

    request = PaymentContextsRequest()
    request.source = source
    request.amount = 1000
    request.currency = Currency.EUR
    request.payment_type = PaymentType.REGULAR
    request.capture = True
    request.processing_channel_id = os.environ.get('CHECKOUT_PROCESSING_CHANNEL_ID')
    request.success_url = 'https://example.com/payments/success'
    request.failure_url = 'https://example.com/payments/failure'
    request.items = [items]

    return request
