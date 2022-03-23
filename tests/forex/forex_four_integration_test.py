from __future__ import absolute_import

from checkout_sdk.common.enums import Currency
from checkout_sdk.forex.forex import QuoteRequest
from tests.checkout_test_utils import assert_response


def test_should_request_quote(oauth_api):
    quote_request = QuoteRequest()
    quote_request.source_currency = Currency.GBP
    quote_request.source_amount = 30000
    quote_request.destination_currency = Currency.USD
    quote_request.process_channel_id = 'pc_abcdefghijklmnopqrstuvwxyz'

    response = oauth_api.forex.request_quote(quote_request)
    assert_response(response,
                    'id',
                    'source_currency',
                    'source_amount',
                    'destination_currency',
                    'destination_amount',
                    'rate',
                    'expires_on')
    assert quote_request.source_currency == response['source_currency']
    assert quote_request.source_amount == response['source_amount']
    assert quote_request.destination_currency == response['destination_currency']
