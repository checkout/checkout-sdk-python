import json

from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.payments.payments import VoidRequest


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class TestVoidRequestSerialization:

    def test_void_request_serializes_amount_when_set(self):
        request = VoidRequest()
        request.amount = 500
        request.reference = 'partial-void-reference'

        assert _serialize(request) == {
            'amount': 500,
            'reference': 'partial-void-reference',
        }

    def test_void_request_omits_amount_when_not_set(self):
        request = VoidRequest()
        request.reference = 'full-void-reference'

        serialized = _serialize(request)

        assert 'amount' not in serialized
        assert serialized == {'reference': 'full-void-reference'}
