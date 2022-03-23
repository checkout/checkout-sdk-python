from __future__ import absolute_import

from datetime import datetime, timezone

from tests.checkout_test_utils import assert_response, retriable
from tests.payments.four.payments_four_test_utils import make_card_payment


def test_should_get_payment_details(four_api):
    payment_response = make_card_payment(four_api, capture_on=datetime.now(timezone.utc))

    payment = retriable(callback=four_api.payments.get_payment_details,
                        payment_id=payment_response['id'])
    assert_response(payment,
                    'id',
                    'requested_on',
                    'amount',
                    'currency',
                    'payment_type',
                    'reference',
                    'status',
                    'approved',
                    'scheme_id',
                    'source.id',
                    'source.type',
                    'source.fingerprint',
                    'source.card_type',
                    'customer.id',
                    'customer.name')
