from __future__ import absolute_import

from datetime import datetime, timezone

from tests.checkout_test_utils import assert_response, new_idempotency_key
from tests.payments.payments_test_utils import make_card_payment, make_3ds_card_payment, make_token_payment


def test_should_request_card_payment(default_api):
    payment_response = make_card_payment(default_api, capture_on=datetime.now(timezone.utc))

    assert_response(payment_response,
                    'id',
                    'processed_on',
                    'reference',
                    'action_id',
                    'response_code',
                    'scheme_id',
                    'response_summary',
                    'status',
                    'amount',
                    'approved',
                    'auth_code',
                    'currency',
                    'source.type',
                    # 'source.id',
                    # 'source.avs_check',
                    # 'source.cvv_check',
                    # 'source.bin',
                    # 'source.card_category',
                    # 'source.card_type',
                    'source.expiry_month',
                    'source.expiry_year',
                    'source.last4',
                    # 'source.scheme',
                    # 'source.name',
                    # 'source.fast_funds',
                    'source.fingerprint',
                    # 'source.issuer',
                    # 'source.issuer_country',
                    # 'source.payouts',
                    # 'source.product_id',
                    # 'source.product_type',
                    'customer',
                    'customer.id',
                    'customer.name',
                    'processing',
                    'processing.acquirer_transaction_id',
                    'processing.retrieval_reference_number')

    assert payment_response['source']['type'] == 'card'


def test_should_request_card_3ds_payment(default_api):
    payment_response = make_3ds_card_payment(default_api, False)

    assert_response(payment_response,
                    'id',
                    'reference',
                    'status',
                    '3ds',
                    '3ds.enrolled',
                    'customer',
                    'customer.id',
                    'customer.name',
                    'customer.email')


def test_should_request_card_3ds_payment_n3d(default_api):
    payment_response = make_3ds_card_payment(default_api, True)

    assert_response(payment_response,
                    'id',
                    'processed_on',
                    'reference',
                    'action_id',
                    'response_code',
                    'scheme_id',
                    'response_summary',
                    'status',
                    'amount',
                    'approved',
                    'auth_code',
                    'currency',
                    'source.type',
                    # 'source.id',
                    # 'source.avs_check',
                    # 'source.cvv_check',
                    # 'source.bin',
                    # 'source.card_category',
                    # 'source.card_type',
                    'source.expiry_month',
                    'source.expiry_year',
                    'source.last4',
                    # 'source.scheme',
                    # 'source.name',
                    # 'source.fast_funds',
                    'source.fingerprint',
                    # 'source.issuer',
                    # 'source.issuer_country',
                    # 'source.payouts',
                    # 'source.product_id',
                    # 'source.product_type',
                    'customer',
                    'customer.id',
                    'customer.name',
                    'processing',
                    'processing.acquirer_transaction_id',
                    'processing.retrieval_reference_number')

    assert payment_response['source']['type'] == 'card'


def test_should_request_token_payment(default_api):
    payment_response = make_token_payment(default_api)

    assert_response(payment_response,
                    'id',
                    'processed_on',
                    'reference',
                    'action_id',
                    'response_code',
                    'scheme_id',
                    'response_summary',
                    'status',
                    'amount',
                    'approved',
                    'auth_code',
                    'currency',
                    'source.type',
                    # 'source.id',
                    # 'source.avs_check',
                    # 'source.cvv_check',
                    # 'source.bin',
                    # 'source.card_category',
                    # 'source.card_type',
                    'source.expiry_month',
                    'source.expiry_year',
                    'source.last4',
                    # 'source.scheme',
                    # 'source.name',
                    # 'source.fast_funds',
                    'source.fingerprint',
                    # 'source.issuer',
                    # 'source.issuer_country',
                    # 'source.payouts',
                    # 'source.product_id',
                    # 'source.product_type',
                    'customer',
                    'customer.id',
                    'processing',
                    'processing.acquirer_transaction_id',
                    'processing.retrieval_reference_number')

    assert payment_response['source']['type'] == 'card'


def test_should_request_payment_idempotently(default_api):
    idempotency_key = new_idempotency_key()

    payment_response_1 = make_card_payment(default_api, capture_on=None, idempotency_key=idempotency_key)
    assert_response(payment_response_1)
    payment_response_2 = make_card_payment(default_api, capture_on=None, idempotency_key=idempotency_key)
    assert_response(payment_response_2)

    assert payment_response_1['action_id'] == payment_response_2['action_id']
