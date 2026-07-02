import json

from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.accounts.accounts import (
    InstrumentDetails, InstrumentDetailsAch, InstrumentAccountType,
)


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class TestInstrumentDetailsAchSerialization:

    def test_is_instrument_details(self):
        assert isinstance(InstrumentDetailsAch(), InstrumentDetails)

    def test_serializes_all_three_fields(self):
        details = InstrumentDetailsAch()
        details.account_number = '12345100'
        details.routing_number = '026009593'
        details.account_type = InstrumentAccountType.SAVINGS

        assert _serialize(details) == {
            'account_number': '12345100',
            'routing_number': '026009593',
            'account_type': 'savings',
        }
