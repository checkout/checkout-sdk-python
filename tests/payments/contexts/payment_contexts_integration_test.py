from __future__ import absolute_import

import os

from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.contexts.contexts import PaymentContextsRequest, PaymentContextPayPalSource, \
    PaymentContextsItems
from checkout_sdk.payments.payments import PaymentType
from tests.checkout_test_utils import assert_response


def test_should_create_and_get_payment_context_details(default_api):
    request = create_payment_contexts_request()

    response = default_api.contexts.create_payment_contexts(request)

    assert_response(response,
                    'http_metadata',
                    'id',
                    'partner_metadata.order_id')

    payment_contexts_details = default_api.contexts.get_payment_context_details(response.id)

    assert_response(payment_contexts_details,
                    'http_metadata',
                    'payment_request',
                    'payment_request.source',
                    'payment_request.amount',
                    'payment_request.currency',
                    'payment_request.payment_type',
                    'payment_request.capture',
                    'payment_request.items',
                    'payment_request.success_url',
                    'payment_request.failure_url',
                    'partner_metadata',
                    'partner_metadata.order_id')


def create_payment_contexts_request():
    source = PaymentContextPayPalSource()

    items = PaymentContextsItems()
    items.name = 'mask'
    items.unit_price = 2000
    items.quantity = 1

    request = PaymentContextsRequest()
    request.source = source
    request.amount = 2000
    request.currency = Currency.EUR
    request.payment_type = PaymentType.REGULAR
    request.capture = True
    request.processing_channel_id = os.environ.get('CHECKOUT_PROCESSING_CHANNEL_ID')
    request.success_url = 'https://example.com/payments/success'
    request.failure_url = 'https://example.com/payments/failure'
    request.items = [items]

    return request
