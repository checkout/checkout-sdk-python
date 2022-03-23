from __future__ import absolute_import

from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.payment_apm_four import RequestIdealSource
from checkout_sdk.payments.payments_apm import RequestSofortSource
from checkout_sdk.payments.payments_four import PaymentRequest
from tests.checkout_test_utils import assert_response, SUCCESS_URL, FAILURE_URL, retriable


def test_should_request_ideal_payment(four_api):
    request_source = RequestIdealSource()
    request_source.bic = 'INGBNL2A'
    request_source.description = 'ORD50234E89'
    request_source.language = 'nl'

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 1000
    payment_request.currency = Currency.EUR
    payment_request.capture = True
    payment_request.success_url = SUCCESS_URL
    payment_request.failure_url = FAILURE_URL

    payment_response = retriable(callback=four_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    'status',
                    '_links',
                    '_links.self',
                    '_links.redirect')

    payment_details = retriable(callback=four_api.payments.get_payment_details,
                                payment_id=payment_response['id'])
    assert_response(payment_details,
                    'id',
                    'requested_on',
                    'source',
                    'amount',
                    'currency',
                    'payment_type',
                    'status')


def test_should_request_sofort_payment(four_api):
    payment_request = PaymentRequest()
    payment_request.source = RequestSofortSource()
    payment_request.amount = 100
    payment_request.currency = Currency.EUR
    payment_request.capture = True
    payment_request.success_url = SUCCESS_URL
    payment_request.failure_url = FAILURE_URL

    payment_response = retriable(callback=four_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    'status',
                    '_links',
                    '_links.self',
                    '_links.redirect')

    payment_details = retriable(callback=four_api.payments.get_payment_details,
                                payment_id=payment_response['id'])
    assert_response(payment_details,
                    'id',
                    'requested_on',
                    'source',
                    'amount',
                    'currency',
                    'payment_type',
                    'status')
