from __future__ import absolute_import

from checkout_sdk.balances.balances import BalancesQuery
from checkout_sdk.common.enums import Currency
from tests.checkout_test_utils import assert_response


def test_should_retrieve_entity_balances(oauth_api):
    query = BalancesQuery()
    query.query = "currency:" + Currency.GBP.value

    response = oauth_api.balances.retrieve_entity_balances('ent_kidtcgc3ge5unf4a5i6enhnr5m', query)
    assert_response(response, 'data')
    assert response.data.__len__() > 0
    for balance in response.data:
        assert_response(balance,
                        'descriptor',
                        'holding_currency',
                        'balances')
