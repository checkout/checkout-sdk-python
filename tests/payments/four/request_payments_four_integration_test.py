from __future__ import absolute_import

from tests.checkout_test_utils import assert_response, new_idempotency_key
from tests.payments.four.payments_four_test_utils import make_card_payment, make_token_payment, make_3ds_card_payment


def test_should_request_card_payment(four_api):
    payment_response = make_card_payment(four_api)

    assert_response(payment_response,
                    'http_metadata',
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
                    'source.id',
                    'source.avs_check',
                    'source.cvv_check',
                    'source.bin',
                    'source.card_category',
                    'source.card_type',
                    'source.expiry_month',
                    'source.expiry_year',
                    'source.last4',
                    'source.scheme',
                    'source.name',
                    'source.fingerprint',
                    # 'source.issuer',
                    'source.issuer_country',
                    'source.product_id',
                    'source.product_type',
                    'customer',
                    'customer.id',
                    'customer.name',
                    'processing',
                    'processing.acquirer_transaction_id',
                    'processing.retrieval_reference_number')

    assert payment_response.source.type == 'card'


def test_should_request_card_3ds_payment(four_api):
    payment_response = make_3ds_card_payment(four_api, False)

    assert_response(payment_response,
                    'http_metadata',
                    'id',
                    'reference',
                    'status',
                    '3ds',
                    '3ds.enrolled',
                    'customer',
                    'customer.id',
                    'customer.name',
                    'customer.email')


def test_should_request_card_3ds_payment_n3d(four_api):
    payment_response = make_3ds_card_payment(four_api, True)

    assert_response(payment_response,
                    'http_metadata',
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
                    'source.id',
                    'source.avs_check',
                    'source.cvv_check',
                    'source.bin',
                    'source.card_category',
                    'source.card_type',
                    'source.expiry_month',
                    'source.expiry_year',
                    'source.last4',
                    'source.scheme',
                    'source.name',
                    'source.fingerprint',
                    # 'source.issuer',
                    'source.issuer_country',
                    'source.product_id',
                    'source.product_type',
                    'customer',
                    'customer.id',
                    'customer.name',
                    'processing',
                    'processing.acquirer_transaction_id',
                    'processing.retrieval_reference_number')

    assert payment_response.source.type == 'card'


def test_should_request_token_payment(four_api):
    payment_response = make_token_payment(four_api)

    assert_response(payment_response,
                    'http_metadata',
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
                    'source.id',
                    'source.avs_check',
                    'source.cvv_check',
                    'source.bin',
                    'source.card_category',
                    'source.card_type',
                    'source.expiry_month',
                    'source.expiry_year',
                    'source.last4',
                    'source.scheme',
                    'source.name',
                    'source.fingerprint',
                    # 'source.issuer',
                    'source.issuer_country',
                    'source.product_id',
                    'source.product_type',
                    'customer',
                    'customer.id',
                    'processing',
                    'processing.acquirer_transaction_id',
                    'processing.retrieval_reference_number')

    assert payment_response.source.type == 'card'


def test_should_request_payment_idempotently(four_api):
    idempotency_key = new_idempotency_key()

    payment_response_1 = make_card_payment(four_api, capture_on=None, idempotency_key=idempotency_key)
    assert_response(payment_response_1)
    payment_response_2 = make_card_payment(four_api, capture_on=None, idempotency_key=idempotency_key)
    assert_response(payment_response_2)

    assert payment_response_1.action_id == payment_response_2.action_id
