from __future__ import absolute_import

from checkout_sdk.apm.klarna import KlarnaProduct, CreditSessionRequest
from checkout_sdk.common.enums import Country, Currency
from tests.checkout_test_utils import assert_response


def test_should_create_and_get_klarna_session(default_api):
    klarna_product = KlarnaProduct()
    klarna_product.name = 'Brown leather belt'
    klarna_product.quantity = 1
    klarna_product.unit_price = 1000
    klarna_product.tax_rate = 0
    klarna_product.total_amount = 1000
    klarna_product.total_tax_amount = 0

    credit_session_request = CreditSessionRequest()
    credit_session_request.purchase_country = Country.GB
    credit_session_request.currency = Currency.GBP
    credit_session_request.locale = 'en-GB'
    credit_session_request.amount = 1000
    credit_session_request.tax_amount = 1
    credit_session_request.products = [klarna_product]

    create_response = default_api.klarna.create_credit_session(credit_session_request)
    assert_response(create_response,
                    'session_id',
                    'client_token',
                    'payment_method_categories')

    create_response = default_api.klarna.get_credit_session(create_response['session_id'])
    assert_response(create_response,
                    'client_token',
                    'purchase_country',
                    'currency',
                    'locale',
                    'amount',
                    'tax_amount',
                    'products')
