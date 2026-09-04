import json

from checkout_sdk.apm.bacs import BacsNotificationRequest, BacsNotificationType
from checkout_sdk.common.enums import Currency
from checkout_sdk.json_serializer import JsonSerializer


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


def _full_request():
    request = BacsNotificationRequest()
    request.source_id = 'src_wmlfc3zyhqzehihu7giusaaawu'
    request.notification_type = BacsNotificationType.ADVANCE_NOTICE
    request.collection_date = '2026-07-15'
    request.amount = 4999
    request.currency = Currency.GBP
    request.reference = 'INV-12345'
    request.customer_email = 'customer@example.com'
    request.billing_descriptor = 'CHECKOUT'
    request.support_email = 'support@test.com'
    request.support_phone = '+447700900123'
    return request


class TestBacsNotificationSerialization:
    """Schema validation tests for BacsNotificationRequest against the swagger schema of
    POST /apms/bacs/notifications. Covers all 10 properties."""

    def test_serializes_every_property_from_the_swagger_example(self):
        assert _serialize(_full_request()) == {
            'source_id': 'src_wmlfc3zyhqzehihu7giusaaawu',
            'notification_type': 'advance_notice',
            'collection_date': '2026-07-15',
            'amount': 4999,
            'currency': 'GBP',
            'reference': 'INV-12345',
            'customer_email': 'customer@example.com',
            'billing_descriptor': 'CHECKOUT',
            'support_email': 'support@test.com',
            'support_phone': '+447700900123',
        }

    def test_omits_the_two_optional_properties_when_unset(self):
        request = _full_request()
        del request.reference
        del request.support_phone

        serialized = _serialize(request)

        assert 'reference' not in serialized
        assert 'support_phone' not in serialized
        assert len(serialized) == 8

    def test_notification_type_carries_the_single_declared_value(self):
        assert [e.value for e in BacsNotificationType] == ['advance_notice']
