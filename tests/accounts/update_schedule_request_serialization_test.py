import json

from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.accounts.accounts import (
    DaySchedule, ScheduleFrequencyWeeklyRequest, UpdateScheduleRequest,
)


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class TestUpdateScheduleRequestSerialization:

    def test_serializes_isv_fields_when_set(self):
        recurrence = ScheduleFrequencyWeeklyRequest()
        recurrence.by_day = [DaySchedule.MONDAY]

        request = UpdateScheduleRequest()
        request.enabled = True
        request.threshold = 100
        request.balance_minimum = 500
        request.carry_forward_enabled = True
        request.payment_instrument_id = 'ppi_w4jelhppmfiufdnatam37wrfc4'
        request.recurrence = recurrence

        assert _serialize(request) == {
            'enabled': True,
            'threshold': 100,
            'balance_minimum': 500,
            'carry_forward_enabled': True,
            'payment_instrument_id': 'ppi_w4jelhppmfiufdnatam37wrfc4',
            'recurrence': {
                'frequency': 'weekly',
                'by_day': ['monday'],
            },
        }

    def test_omits_isv_fields_when_unset(self):
        request = UpdateScheduleRequest()
        request.enabled = False

        serialized = _serialize(request)
        assert serialized == {'enabled': False}
        assert 'balance_minimum' not in serialized
        assert 'carry_forward_enabled' not in serialized
        assert 'payment_instrument_id' not in serialized
