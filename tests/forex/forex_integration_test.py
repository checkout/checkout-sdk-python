from __future__ import absolute_import

import pytest

from checkout_sdk.common.enums import Currency
from checkout_sdk.forex.forex import QuoteRequest, RatesQueryFilter, ForexSource
from tests.checkout_test_utils import assert_response


def test_should_request_quote(oauth_api):
    quote_request = QuoteRequest()
    quote_request.source_currency = Currency.GBP
    quote_request.source_amount = 30000
    quote_request.destination_currency = Currency.USD
    quote_request.process_channel_id = 'pc_abcdefghijklmnopqrstuvwxyz'

    response = oauth_api.forex.request_quote(quote_request)
    assert_response(response,
                    'http_metadata',
                    'id',
                    'source_currency',
                    'source_amount',
                    'destination_currency',
                    'destination_amount',
                    'rate',
                    'expires_on')
    assert quote_request.source_currency == response.source_currency
    assert quote_request.source_amount == response.source_amount
    assert quote_request.destination_currency == response.destination_currency


@pytest.mark.skip(reason='not available')
def test_should_get_rates(oauth_api):
    rates_query = RatesQueryFilter()
    rates_query.product = 'card_payouts'
    rates_query.source = ForexSource.VISA
    rates_query.currency_pairs = 'GBPEUR,USDNOK,JPNCAD'
    rates_query.process_channel_id = 'pc_abcdefghijklmnopqrstuvwxyz'

    response = oauth_api.forex.get_rates(rates_query)
    assert_response(response,
                    'http_metadata',
                    'product',
                    'source',
                    'rates')
    assert rates_query.product == response.product
    assert rates_query.source == response.source
