import json

from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.common.common import AmountAllocations, Commission
from checkout_sdk.payments.sessions.sessions import SubmitPaymentSessionRequest


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class TestSubmitPaymentSessionRequestSerialization:
    """amount_allocations was added to SubmitPaymentSessionsRequest by the 2026-08-21 spec change.

    These tests are the only thing that proves the wire name is amount_allocations and that an
    unset field stays out of the body. The SDK serializes by reflecting over instance attributes,
    so a declared-but-unset attribute can leak as null depending on the serializer's null
    handling; the API rejects an explicit null on this field.

    Values are the field-level examples from shared/swagger-latest.json.
    """

    def test_should_serialize_amount_allocations_with_all_item_fields(self):
        commission = Commission()
        commission.amount = 10
        commission.percentage = 12.5

        allocation = AmountAllocations()
        allocation.id = 'ent_w4jelhppmfiufdnatam37wrfc4'
        allocation.amount = 1
        allocation.reference = 'ORD-123A'
        allocation.commission = commission

        request = SubmitPaymentSessionRequest()
        request.session_data = 'session_data_token'
        request.amount_allocations = [allocation]

        assert _serialize(request) == {
            'session_data': 'session_data_token',
            'amount_allocations': [{
                'id': 'ent_w4jelhppmfiufdnatam37wrfc4',
                'amount': 1,
                'reference': 'ORD-123A',
                'commission': {'amount': 10, 'percentage': 12.5},
            }]
        }

    def test_should_serialize_amount_allocations_with_only_required_item_fields(self):
        # The item's `required` list is [id, amount]; reference and commission must not appear
        # as nulls when they are not set.
        allocation = AmountAllocations()
        allocation.id = 'ent_w4jelhppmfiufdnatam37wrfc4'
        allocation.amount = 1

        request = SubmitPaymentSessionRequest()
        request.amount_allocations = [allocation]

        assert _serialize(request) == {
            'amount_allocations': [{'id': 'ent_w4jelhppmfiufdnatam37wrfc4', 'amount': 1}]
        }

    def test_should_omit_amount_allocations_when_unset(self):
        # The field is optional with minItems 1: sending `"amount_allocations": null` or an empty
        # array is not the same as omitting it, and the API rejects both.
        request = SubmitPaymentSessionRequest()
        request.session_data = 'session_data_token'

        serialized = _serialize(request)

        assert serialized == {'session_data': 'session_data_token'}
        assert 'amount_allocations' not in serialized
