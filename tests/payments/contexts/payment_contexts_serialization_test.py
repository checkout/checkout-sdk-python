import json

from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.payments.contexts.contexts import (
    PaymentContextsFlightLegDetails, PaymentContextsPassenger, PaymentContextsTicket,
)


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class TestDateFieldTypes:
    """The specification declares these fields `format: date`.

    The serializer renders anything with strftime through isoformat(), so a datetime emits a full
    ISO timestamp. Only a yyyy-MM-dd string produces the declared format, so these attributes are
    annotated `str` -- the same convention as BacsNotificationRequest.collection_date and
    SepaInstrumentData.date_of_signature.
    """

    def test_airline_date_fields_are_annotated_as_strings(self):
        assert PaymentContextsTicket.__annotations__['issue_date'] is str
        assert PaymentContextsPassenger.__annotations__['date_of_birth'] is str
        assert PaymentContextsFlightLegDetails.__annotations__['departure_date'] is str

    def test_ticket_issue_date_serializes_in_the_declared_format(self):
        ticket = PaymentContextsTicket()
        ticket.number = '045-21351455613'
        ticket.issue_date = '2023-05-20'

        serialized = _serialize(ticket)

        assert serialized['number'] == '045-21351455613'
        assert serialized['issue_date'] == '2023-05-20'

    def test_passenger_date_of_birth_serializes_in_the_declared_format(self):
        passenger = PaymentContextsPassenger()
        passenger.first_name = 'John'
        passenger.date_of_birth = '1990-05-26'

        assert _serialize(passenger)['date_of_birth'] == '1990-05-26'

    def test_flight_leg_departure_date_serializes_in_the_declared_format(self):
        leg = PaymentContextsFlightLegDetails()
        leg.flight_number = '101'
        leg.departure_date = '2023-06-19'

        assert _serialize(leg)['departure_date'] == '2023-06-19'

    def test_unset_date_fields_are_absent(self):
        ticket = PaymentContextsTicket()
        ticket.number = '045-21351455613'

        assert 'issue_date' not in _serialize(ticket)

    def test_a_datetime_would_not_serialize_in_the_declared_format(self):
        # Documents why the annotation is str: this is what a datetime produces. These fields were
        # annotated `datetime`, so following the annotation put a timestamp on a date-only field.
        from datetime import datetime
        ticket = PaymentContextsTicket()
        ticket.issue_date = datetime(2023, 5, 20)

        assert _serialize(ticket)['issue_date'] == '2023-05-20T00:00:00'
