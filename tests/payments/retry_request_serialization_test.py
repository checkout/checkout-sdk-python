import json

from checkout_sdk.common.common import CustomerRetry
from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.payments.hosted.hosted_payments import HostedPaymentsSessionRequest
from checkout_sdk.payments.links.payments_links import PaymentLinkRequest
from checkout_sdk.payments.payments import PaymentRetryRequest, DunningRetryRequest, DowntimeRetryRequest, \
    PaymentRequest
from checkout_sdk.payments.sessions import sessions as payment_sessions
from checkout_sdk.payments.sessions.sessions import PaymentSessionsRequest


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


def _build_retry(enabled=True):
    dunning = DunningRetryRequest()
    dunning.enabled = enabled
    dunning.max_attempts = 6
    dunning.end_after_days = 30
    downtime = DowntimeRetryRequest()
    downtime.enabled = enabled
    retry = PaymentRetryRequest()
    retry.enabled = enabled
    retry.dunning = dunning
    retry.downtime = downtime
    return retry


class TestRetryRequestSerialization:

    def test_should_serialize_all_retry_properties_on_payment_request(self):
        request = PaymentRequest()
        request.retry = _build_retry()
        body = _serialize(request)
        assert body['retry'] == {
            'enabled': True,
            'dunning': {'enabled': True, 'max_attempts': 6, 'end_after_days': 30},
            'downtime': {'enabled': True},
        }

    def test_should_serialize_enabled_false(self):
        body = _serialize(_build_retry(enabled=False))
        assert body['enabled'] is False
        assert body['dunning']['enabled'] is False
        assert body['downtime']['enabled'] is False

    def test_should_serialize_sdk_objects_key_by_key(self):
        body = _serialize(_build_retry())
        assert set(body.keys()) == {'enabled', 'dunning', 'downtime'}
        assert body['enabled'] is True
        assert set(body['dunning'].keys()) == {'enabled', 'max_attempts', 'end_after_days'}
        assert body['dunning']['enabled'] is True
        assert body['dunning']['max_attempts'] == 6
        assert body['dunning']['end_after_days'] == 30
        assert body['downtime'] == {'enabled': True}

    def test_should_serialize_deprecated_top_level_fields_with_dunning(self):
        retry = _build_retry()
        retry.max_attempts = 3
        retry.end_after_days = 10
        assert _serialize(retry) == {
            'enabled': True,
            'max_attempts': 3,
            'end_after_days': 10,
            'dunning': {'enabled': True, 'max_attempts': 6, 'end_after_days': 30},
            'downtime': {'enabled': True},
        }

    def test_should_not_send_unset_deprecated_top_level_fields(self):
        body = _serialize(_build_retry())
        assert 'max_attempts' not in body
        assert 'end_after_days' not in body


class TestCustomerRetrySerialization:

    def _customer_retry(self):
        # swagger example: max_attempts = 2
        customer_retry = CustomerRetry()
        customer_retry.max_attempts = 2
        return customer_retry

    def test_should_serialize_on_hosted_payments(self):
        request = HostedPaymentsSessionRequest()
        request.customer_retry = self._customer_retry()
        assert _serialize(request)['customer_retry'] == {'max_attempts': 2}

    def test_should_serialize_on_payment_links(self):
        request = PaymentLinkRequest()
        request.customer_retry = self._customer_retry()
        assert _serialize(request)['customer_retry'] == {'max_attempts': 2}

    def test_should_serialize_on_payment_sessions(self):
        request = PaymentSessionsRequest()
        request.customer_retry = self._customer_retry()
        assert _serialize(request)['customer_retry'] == {'max_attempts': 2}

    def test_should_serialize_zero_attempts(self):
        customer_retry = CustomerRetry()
        customer_retry.max_attempts = 0
        assert _serialize(customer_retry) == {'max_attempts': 0}

    def test_sessions_module_exposes_shared_type(self):
        assert payment_sessions.CustomerRetry is CustomerRetry

    def test_should_roundtrip_customer_retry(self):
        body = _serialize(self._customer_retry())
        restored = CustomerRetry()
        for key, value in body.items():
            setattr(restored, key, value)
        assert restored.max_attempts == 2
        assert _serialize(restored) == body == {'max_attempts': 2}


class TestPaymentRetryRequestRoundtrip:

    def test_should_roundtrip_payment_retry_request(self):
        # swagger has no property examples for RetryRequest; values use the DunningRetryRequest defaults
        body = _serialize(_build_retry())
        restored = PaymentRetryRequest()
        restored.enabled = body['enabled']
        restored.dunning = DunningRetryRequest()
        for key, value in body['dunning'].items():
            setattr(restored.dunning, key, value)
        restored.downtime = DowntimeRetryRequest()
        for key, value in body['downtime'].items():
            setattr(restored.downtime, key, value)
        assert restored.enabled is True
        assert restored.dunning.enabled is True
        assert restored.dunning.max_attempts == 6
        assert restored.dunning.end_after_days == 30
        assert restored.downtime.enabled is True
        assert _serialize(restored) == body == {
            'enabled': True,
            'dunning': {'enabled': True, 'max_attempts': 6, 'end_after_days': 30},
            'downtime': {'enabled': True},
        }
