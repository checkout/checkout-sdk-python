import json

from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.payments.payments import (
    AccommodationAddress, AccommodationData, AccommodationGuest, AccommodationPhone,
    AccommodationRoom, AirlineData, FlightLegDetails, Passenger, PassengerAddress,
    ProcessingSettings, Ticket,
)


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class TestAirlineDataSerialization:
    """Serialization tests for the processing.airline_data and accommodation_data sub-tree.

    The Python SDK returns responses as a ResponseWrapper over a parsed dict, so it cannot hit
    the typed deserialization failure a merchant reported against another SDK. What it can get
    wrong is the request: the serializer reflects assigned attributes, so an unset attribute is
    absent and the shape of a value is whatever the caller assigned.

    Before this row there were no airline classes in checkout_sdk.payments.payments at all.
    ProcessingSettings.airline_data carried the comment `# AirlineData`, naming a class that
    existed only in payments_previous.py with the legacy ABC shape.
    """

    def test_unset_attributes_are_absent(self):
        # The serializer only emits attributes that were assigned, which is what makes the
        # "leave passenger unset when there are none" guidance work: an empty list and a null
        # are both rejected with processing_airline_data_0_passenger_invalid.
        assert _serialize(AirlineData()) == {}
        assert _serialize(Ticket()) == {}
        assert _serialize(Passenger()) == {}

    def test_single_passenger_serializes_as_an_object(self):
        # Verified against the sandbox on 2026-09-25: a single object is accepted on every
        # request surface, a list only on POST /payments. hosted payments, payment links and
        # payment contexts all reject the list form. See AirlineData.passenger.
        airline = AirlineData()
        airline.ticket = Ticket()
        airline.ticket.number = '045-21351455613'
        airline.passenger = Passenger()
        airline.passenger.first_name = 'John'
        airline.passenger.last_name = 'White'

        result = _serialize(airline)

        assert isinstance(result['passenger'], dict)
        assert result['passenger'] == {'first_name': 'John', 'last_name': 'White'}

    def test_several_passengers_serialize_as_a_list(self):
        # Several passengers can only be expressed as a list, which only POST /payments accepts.
        first, second = Passenger(), Passenger()
        first.first_name = 'John'
        second.first_name = 'Jane'

        airline = AirlineData()
        airline.passenger = [first, second]

        result = _serialize(airline)

        assert isinstance(result['passenger'], list)
        assert result['passenger'] == [{'first_name': 'John'}, {'first_name': 'Jane'}]

    def test_airline_data_serializes_every_spec_key(self):
        ticket = Ticket()
        ticket.number = '045-21351455613'
        ticket.issue_date = '2023-05-20'
        ticket.issuing_carrier_code = 'AI'
        ticket.travel_package_indicator = 'B'
        ticket.travel_agency_name = 'World Tours'
        ticket.travel_agency_code = '01'

        passenger = Passenger()
        passenger.first_name = 'John'
        passenger.last_name = 'White'
        passenger.date_of_birth = '1990-05-26'
        passenger.address = PassengerAddress()
        passenger.address.country = 'US'

        leg = FlightLegDetails()
        leg.flight_number = '101'
        leg.carrier_code = 'BA'
        leg.class_of_travelling = 'J'
        leg.departure_airport = 'LHR'
        leg.departure_date = '2023-06-19'
        leg.departure_time = '15:30'
        leg.arrival_airport = 'LAX'
        leg.stop_over_code = 'X'
        leg.fare_basis_code = 'SPRSVR'

        airline = AirlineData()
        airline.ticket = ticket
        airline.passenger = passenger
        airline.flight_leg_details = [leg]

        result = _serialize(airline)

        # A whole-dict == ignores key order, so order is pinned separately. Note this SDK emits
        # keys ALPHABETICALLY, not in declaration or specification order, because JsonSerializer
        # reflects with inspect.getmembers() which sorts by name. That is harmless (JSON object
        # order is not semantic and the API accepts it) but it is a real difference from the
        # other SDKs, whose serializers preserve declaration order. Pinned here so a change to
        # the encoder -- for example reflecting __dict__, which preserves insertion order --
        # shows up as a test failure rather than a silent change in every payload.
        assert list(result.keys()) == ['flight_leg_details', 'passenger', 'ticket']
        assert list(result['ticket'].keys()) == [
            'issue_date', 'issuing_carrier_code', 'number', 'travel_agency_code',
            'travel_agency_name', 'travel_package_indicator',
        ]
        assert list(result['passenger'].keys()) == [
            'address', 'date_of_birth', 'first_name', 'last_name',
        ]
        assert list(result['flight_leg_details'][0].keys()) == [
            'arrival_airport', 'carrier_code', 'class_of_travelling', 'departure_airport',
            'departure_date', 'departure_time', 'fare_basis_code', 'flight_number',
            'stop_over_code',
        ]

        # Asserted as a whole dict, so a wrong or extra key fails here rather than passing
        # because the assertion happened not to look at it.
        assert result == {
            'ticket': {
                'number': '045-21351455613',
                'issue_date': '2023-05-20',
                'issuing_carrier_code': 'AI',
                'travel_package_indicator': 'B',
                'travel_agency_name': 'World Tours',
                'travel_agency_code': '01',
            },
            'passenger': {
                'first_name': 'John',
                'last_name': 'White',
                'date_of_birth': '1990-05-26',
                'address': {'country': 'US'},
            },
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

    def test_passenger_address_carries_only_country(self):
        # The spec defines exactly one property on passenger.address.
        passenger = Passenger()
        passenger.address = PassengerAddress()
        passenger.address.country = 'US'

        assert _serialize(passenger) == {'address': {'country': 'US'}}

    def test_accommodation_data_serializes_every_spec_key(self):
        guest = AccommodationGuest()
        guest.first_name = 'Jane'
        guest.last_name = 'Doe'
        guest.date_of_birth = '1985-07-14'

        room = AccommodationRoom()
        room.rate = '70'
        room.number_of_nights_at_room_rate = '3'

        property_phone = AccommodationPhone()
        property_phone.country_code = '44'
        property_phone.number = '7123456789'

        service_phone = AccommodationPhone()
        service_phone.country_code = '44'
        service_phone.number = '7987654321'

        accommodation = AccommodationData()
        accommodation.name = 'The Sea View Hotel'
        accommodation.booking_reference = 'HOTEL123'
        accommodation.check_in_date = '2023-06-20'
        accommodation.check_out_date = '2023-06-23'
        accommodation.address = AccommodationAddress()
        accommodation.address.address_line1 = '123 Beach Road'
        accommodation.address.zip = '10001'
        accommodation.state = 'FL'
        accommodation.country = 'USA'
        accommodation.city = 'Los Angeles'
        accommodation.number_of_rooms = 2
        accommodation.guests = [guest]
        accommodation.room = [room]
        accommodation.property_phone = [property_phone]
        accommodation.customer_service_phone = [service_phone]

        result = _serialize(accommodation)

        # Alphabetical, per the note in test_airline_data_serializes_every_spec_key.
        assert list(result.keys()) == [
            'address', 'booking_reference', 'check_in_date', 'check_out_date', 'city', 'country',
            'customer_service_phone', 'guests', 'name', 'number_of_rooms', 'property_phone',
            'room', 'state',
        ]

        assert result == {
            'name': 'The Sea View Hotel',
            'booking_reference': 'HOTEL123',
            'check_in_date': '2023-06-20',
            'check_out_date': '2023-06-23',
            'address': {'address_line1': '123 Beach Road', 'zip': '10001'},
            # state and country are free-form strings: "FL" is a US state and "USA" is three
            # letters, so neither fits an ISO 3166-1 alpha-2 enum.
            'state': 'FL',
            'country': 'USA',
            'city': 'Los Angeles',
            'number_of_rooms': 2,
            'guests': [{'first_name': 'Jane', 'last_name': 'Doe', 'date_of_birth': '1985-07-14'}],
            'room': [{'rate': '70', 'number_of_nights_at_room_rate': '3'}],
            # property_phone and customer_service_phone were missing from the class entirely.
            'property_phone': [{'country_code': '44', 'number': '7123456789'}],
            'customer_service_phone': [{'country_code': '44', 'number': '7987654321'}],
        }

    def test_processing_settings_carries_the_airline_sub_tree(self):
        # ProcessingSettings is the object POST /payments, hosted payments and payment links all
        # embed as "processing", so this covers every request surface at once.
        passenger = Passenger()
        passenger.first_name = 'John'

        airline = AirlineData()
        airline.ticket = Ticket()
        airline.ticket.number = '045'
        airline.passenger = passenger

        processing = ProcessingSettings()
        processing.airline_data = [airline]

        result = _serialize(processing)

        assert result['airline_data'] == [
            {'ticket': {'number': '045'}, 'passenger': {'first_name': 'John'}}
        ]
        assert isinstance(result['airline_data'][0]['passenger'], dict)
