from __future__ import absolute_import

from datetime import datetime, timezone

from tests.checkout_test_utils import assert_response, retriable
from tests.payments.payments_test_utils import make_card_payment


def test_should_get_payment_details(default_api):
    payment_response = make_card_payment(default_api, capture_on=datetime.now(timezone.utc))

    payment = retriable(callback=default_api.payments.get_payment_details,
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
