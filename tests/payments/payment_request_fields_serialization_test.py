import json

from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.payments.payments import AuthorizationType, PaymentPlan
from checkout_sdk.payments.hosted.hosted_payments import HostedPaymentsSessionRequest
from checkout_sdk.payments.links.payments_links import PaymentLinkRequest
from checkout_sdk.payments.sessions.sessions import PaymentSessionsRequest


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


def _payment_plan():
    plan = PaymentPlan()
    plan.days_between_payments = 30
    plan.total_number_of_payments = 12
    return plan


class TestPaymentRequestFieldsSerialization:

    def test_hosted_payments_request_serializes_authorization_type_and_payment_plan(self):
        request = HostedPaymentsSessionRequest()
        request.authorization_type = AuthorizationType.ESTIMATED
        request.payment_plan = _payment_plan()

        assert _serialize(request) == {
            'authorization_type': 'Estimated',
            'payment_plan': {'days_between_payments': 30, 'total_number_of_payments': 12},
        }

    def test_payment_link_request_serializes_authorization_type_and_payment_plan(self):
        request = PaymentLinkRequest()
        request.authorization_type = AuthorizationType.INCREMENTAL
        request.payment_plan = _payment_plan()

        assert _serialize(request) == {
            'authorization_type': 'Incremental',
            'payment_plan': {'days_between_payments': 30, 'total_number_of_payments': 12},
        }

    def test_payment_sessions_request_serializes_authorization_type_and_payment_plan(self):
        request = PaymentSessionsRequest()
        request.authorization_type = AuthorizationType.FINAL
        request.payment_plan = _payment_plan()

        assert _serialize(request) == {
            'authorization_type': 'Final',
            'payment_plan': {'days_between_payments': 30, 'total_number_of_payments': 12},
        }
