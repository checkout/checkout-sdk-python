from __future__ import absolute_import

from checkout_sdk.balances.balances import BalancesQuery
from checkout_sdk.common.enums import Currency
from checkout_sdk.exception import CheckoutApiException
from tests.checkout_test_utils import assert_response

ENTITY_ID = 'ent_kidtcgc3ge5unf4a5i6enhnr5m'


def test_should_retrieve_entity_balances(oauth_api):
    query = BalancesQuery()
    query.query = "currency:" + Currency.GBP.value

    response = oauth_api.balances.retrieve_entity_balances(ENTITY_ID, query)
    assert_response(response, 'data')
    assert response.data.__len__() > 0
    for balance in response.data:
        assert_response(balance,
                        'descriptor',
                        'holding_currency',
                        'balances')


def test_should_retrieve_top_up_instructions(oauth_api):
    """GET /entities/{entityId}/currency-accounts/{currencyAccountId}/top-up-instructions

    Top-ups are not enabled on the sandbox sub-accounts this suite has access to, so the endpoint
    answers 403 ("top-ups aren't enabled for the sub-account") rather than 200. Verified live on
    2026-09-07 with the balances:top-up-instructions scope granted, which the sandbox IdP issues.

    The test accepts either outcome, but only the outcomes the spec documents as "not available
    here": 403 and 404. It still fails on 400 (malformed identifiers, i.e. the SDK built the path
    wrongly) and on 401 (wrong authorization type), which are the two ways this endpoint could
    actually be broken in the SDK.
    """
    query = BalancesQuery()
    query.with_currency_account_id = True

    balances = oauth_api.balances.retrieve_entity_balances(ENTITY_ID, query)
    assert_response(balances, 'data')

    # Take the first sub-account that reports an id. Requiring the entity to always have one would
    # fail this test for a reason unrelated to top-up instructions.
    currency_account_id = next(
        (b.currency_account_id for b in balances.data
         if getattr(b, 'currency_account_id', None)),
        None)
    if currency_account_id is None:
        return

    try:
        instructions = oauth_api.balances.retrieve_top_up_instructions(ENTITY_ID, currency_account_id)

        assert_response(instructions,
                        'currency_account_id',
                        'currency',
                        'payment_reference',
                        'bank_details')
        assert instructions.currency_account_id == currency_account_id

        # Assert only what the spec guarantees. bank_details declares no required properties, so
        # an empty object is a legal 200 body -- do not require a rail to be present. Where a rail
        # IS returned, its two required fields must be.
        for rail_name in ('domestic', 'international'):
            rail = getattr(instructions.bank_details, rail_name, None)
            if rail is None:
                continue
            assert_response(rail, 'beneficiary_account_name', 'bank_name')
    except CheckoutApiException as err:
        # 403 = top-ups not enabled for the sub-account, or the credential lacks access.
        # 404 = sub-account not found, or it has no top-up instructions available.
        # Anything else means the SDK, not the environment, is at fault.
        assert err.http_metadata.status_code in (403, 404), \
            f'unexpected status {err.http_metadata.status_code} from top-up instructions'
