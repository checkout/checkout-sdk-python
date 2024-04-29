from __future__ import absolute_import

import os

from checkout_sdk.common.common import AccountHolder, Address
from checkout_sdk.common.enums import Currency, Country
from checkout_sdk.payments.contexts.contexts import PaymentContextsRequest, PaymentContextsItems, \
    PaymentContextPaypalSource, PaymentContextKlarnaSource, PaymentContextsProcessing
from checkout_sdk.payments.payments import PaymentType
from tests.checkout_test_utils import assert_response, APM_SERVICE_UNAVAILABLE, check_error_item


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


def test_create_payment_contexts_klarna_request(default_api):
    processing = PaymentContextsProcessing()
    processing.locale = "en-GB"

    billing_address = Address()
    billing_address.country = Country.DE

    account_holder = AccountHolder()
    account_holder.billing_address = billing_address

    source = PaymentContextKlarnaSource()
    source.account_holder = account_holder

    items = PaymentContextsItems()
    items.name = 'mask'
    items.unit_price = 1000
    items.quantity = 1
    items.total_amount = 1000

    request = PaymentContextsRequest()
    request.source = source
    request.amount = 1000
    request.currency = Currency.EUR
    request.payment_type = PaymentType.REGULAR
    request.processing_channel_id = os.environ.get('CHECKOUT_PROCESSING_CHANNEL_ID')
    request.items = [items]
    request.processing = processing

    check_error_item(callback=default_api.contexts.create_payment_contexts,
                     error_item=APM_SERVICE_UNAVAILABLE,
                     payment_contexts_request=request)


def create_payment_contexts_request():
    source = PaymentContextPaypalSource()

    items = PaymentContextsItems()
    items.name = 'mask'
    items.unit_price = 1000
    items.quantity = 1
    items.total_amount = 1000

    request = PaymentContextsRequest()
    request.source = source
    request.amount = 1000
    request.currency = Currency.EUR
    request.payment_type = PaymentType.REGULAR
    request.capture = True
    request.processing_channel_id = os.environ.get('CHECKOUT_PROCESSING_CHANNEL_ID')
    request.success_url = 'https://example.com/payments/success'
    request.failure_url = 'https://example.com/payments/failure'
    request.items = [items]

    return request
