from __future__ import absolute_import

from datetime import datetime, timezone

from tests.checkout_test_utils import assert_response, retriable
from tests.payments.previous.payments_previous_test_utils import make_card_payment


def test_should_get_payment_details(previous_api):
    payment_response = make_card_payment(previous_api, capture_on=datetime.now(timezone.utc))

    payment = retriable(callback=previous_api.payments.get_payment_details,
                        payment_id=payment_response.id)
    assert_response(payment,
                    'id',
                    'requested_on',
                    'amount',
                    'currency',
                    'payment_type',
                    'reference',
                    'status',
                    'approved',
                    # 'eci',
                    'scheme_id',
                    'source.id',
                    'source.type',
                    'source.fingerprint',
                    # 'source.card_type',
                    'customer.id',
                    'customer.name')
