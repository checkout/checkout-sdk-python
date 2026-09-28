import json

from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.payments.payments import (
    AccommodationData, AccommodationRoom, BillingPlan, PassengerAddress,
)
from checkout_sdk.payments.contexts.contexts import (
    PaymentContextsAirlineData, PaymentContextsFlightLegDetails,
    PaymentContextsPartnerCustomerRiskData, PaymentContextsPassenger,
    PaymentContextsProcessing, PaymentContextsTicket,
)


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class TestPaymentContextsAirlineSerialization:
    """Serialization tests for the payment contexts airline and accommodation sub-tree."""

    def test_ticket_serializes_as_an_object_not_a_list(self):
        # The spec declares airline_data[].ticket as a single object. It was annotated as a
        # list, so the SDK sent an array, a shape the API does not accept.
        airline = PaymentContextsAirlineData()
        airline.ticket = PaymentContextsTicket()
        airline.ticket.number = '045-21351455613'
        airline.ticket.travel_package_indicator = 'B'

        result = _serialize(airline)

        assert isinstance(result['ticket'], dict)
        assert result['ticket'] == {
            'number': '045-21351455613',
            'travel_package_indicator': 'B',
        }

    def test_single_passenger_serializes_as_an_object(self):
        # POST /payment-contexts rejects the list form with 422 passenger_required and accepts a
        # single object, verified against the sandbox on 2026-09-25.
        passenger = PaymentContextsPassenger()
        passenger.first_name = 'John'
        passenger.last_name = 'White'
        passenger.address = PassengerAddress()
        passenger.address.country = 'GB'

        airline = PaymentContextsAirlineData()
        airline.passenger = passenger

        result = _serialize(airline)

        assert isinstance(result['passenger'], dict)
        assert result['passenger'] == {
            'first_name': 'John',
            'last_name': 'White',
            # The spec defines exactly one property on passenger.address. This shares
            # payments.PassengerAddress rather than the wider common Address.
            'address': {'country': 'GB'},
        }

    def test_unset_passenger_is_absent(self):
        # An empty list and a null are both rejected, so an unset passenger must be absent.
        airline = PaymentContextsAirlineData()
        airline.ticket = PaymentContextsTicket()
        airline.ticket.number = '045'

        assert 'passenger' not in _serialize(airline)

    def test_airline_data_serializes_every_spec_key(self):
        ticket = PaymentContextsTicket()
        ticket.number = '045-21351455613'
        ticket.issue_date = '2023-05-20'
        ticket.issuing_carrier_code = 'AI'
        ticket.travel_package_indicator = 'B'
        ticket.travel_agency_name = 'World Tours'
        ticket.travel_agency_code = '01'

        passenger = PaymentContextsPassenger()
        passenger.first_name = 'John'
        passenger.date_of_birth = '1990-05-26'

        leg = PaymentContextsFlightLegDetails()
        leg.flight_number = '101'
        leg.carrier_code = 'BA'
        leg.class_of_travelling = 'J'
        leg.departure_airport = 'LHR'
        leg.departure_date = '2023-06-19'
        leg.departure_time = '15:30'
        leg.arrival_airport = 'LAX'
        leg.stop_over_code = 'X'
        leg.fare_basis_code = 'SPRSVR'

        airline = PaymentContextsAirlineData()
        airline.ticket = ticket
        airline.passenger = passenger
        airline.flight_leg_details = [leg]

        assert _serialize(airline) == {
            'ticket': {
                'number': '045-21351455613',
                'issue_date': '2023-05-20',
                'issuing_carrier_code': 'AI',
                'travel_package_indicator': 'B',
                'travel_agency_name': 'World Tours',
                'travel_agency_code': '01',
            },
            'passenger': {'first_name': 'John', 'date_of_birth': '1990-05-26'},
            'flight_leg_details': [{
                'flight_number': '101',
                'carrier_code': 'BA',
                'class_of_travelling': 'J',
                'departure_airport': 'LHR',
                'departure_date': '2023-06-19',
                'departure_time': '15:30',
                'arrival_airport': 'LAX',
                'stop_over_code': 'X',
                'fare_basis_code': 'SPRSVR',
            }],
        }

    def test_processing_carries_every_spec_field(self):
        plan = BillingPlan()
        plan.skip_shipping_address = True

        risk = PaymentContextsPartnerCustomerRiskData()
        risk.key = 'risk_score'
        risk.value = '42'

        room = AccommodationRoom()
        room.rate = '70'
        room.number_of_nights_at_room_rate = '3'

        accommodation = AccommodationData()
        accommodation.name = 'The Sea View Hotel'
        accommodation.state = 'FL'
        accommodation.country = 'USA'
        accommodation.room = [room]

        airline = PaymentContextsAirlineData()
        airline.ticket = PaymentContextsTicket()
        airline.ticket.number = '045'

        processing = PaymentContextsProcessing()
        processing.plan = plan
        processing.discount_amount = 5
        processing.shipping_amount = 300
        processing.tax_amount = 3000
        processing.invoice_id = 'INV-1'
        processing.brand_name = 'Acme Corporation'
        processing.locale = 'en-US'
        processing.partner_customer_risk_data = [risk]
        processing.custom_payment_method_ids = ['cpm_001', 'cpm_002']
        processing.airline_data = [airline]
        # accommodation_data uses the shared payments.AccommodationData, because payment
        # contexts, POST /payments and the GET /payments/{id} response all resolve it to the
        # same specification schema.
        processing.accommodation_data = [accommodation]

        assert _serialize(processing) == {
            'plan': {'skip_shipping_address': True},
            'discount_amount': 5,
            'shipping_amount': 300,
            'tax_amount': 3000,
            'invoice_id': 'INV-1',
            'brand_name': 'Acme Corporation',
            'locale': 'en-US',
            'partner_customer_risk_data': [{'key': 'risk_score', 'value': '42'}],
            'custom_payment_method_ids': ['cpm_001', 'cpm_002'],
            'airline_data': [{'ticket': {'number': '045'}}],
            'accommodation_data': [{
                'name': 'The Sea View Hotel',
                'state': 'FL',
                'country': 'USA',
                'room': [{'rate': '70', 'number_of_nights_at_room_rate': '3'}],
            }],
        }
