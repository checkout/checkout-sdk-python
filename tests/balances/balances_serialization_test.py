"""Serialization tests for the balances query filter.

BalancesQuery's attributes are snake_case, but the swagger declares the two query parameters in
camelCase (withCurrencyAccountId, balancesAt). The mapping lives in
JsonSerializer._KEYS_TRANSFORMATIONS, so these tests pin the exact wire names: if an entry is
removed from that table, the API silently ignores the parameters and these tests fail instead.
"""
import json
from datetime import datetime, timezone

from checkout_sdk.balances.balances import BalancesQuery
from checkout_sdk.checkout_response import ResponseWrapper
from checkout_sdk.json_serializer import JsonSerializer


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class TestBalancesQuerySerialization:

    def test_should_map_with_currency_account_id_to_camel_case(self):
        query = BalancesQuery()
        query.with_currency_account_id = True

        encoded = _serialize(query)

        assert encoded['withCurrencyAccountId'] is True
        assert 'with_currency_account_id' not in encoded

    def test_should_map_balances_at_to_camel_case_and_iso_format(self):
        query = BalancesQuery()
        query.balances_at = datetime(2026, 5, 6, 13, 59, 59, tzinfo=timezone.utc)

        encoded = _serialize(query)

        assert 'balances_at' not in encoded
        assert encoded['balancesAt'].startswith('2026-05-06T13:59:59')

    def test_should_serialize_query_unchanged(self):
        query = BalancesQuery()
        query.query = 'currency:GBP'

        assert _serialize(query)['query'] == 'currency:GBP'

    def test_should_serialize_all_three_parameters(self):
        query = BalancesQuery()
        query.query = 'currency:GBP'
        query.with_currency_account_id = True
        query.balances_at = datetime(2026, 5, 6, 13, 59, 59, tzinfo=timezone.utc)

        encoded = _serialize(query)

        assert encoded['query'] == 'currency:GBP'
        assert encoded['withCurrencyAccountId'] is True
        assert 'balancesAt' in encoded

class TestTopUpInstructionsResponseShape:
    """Response-shape tests for GET .../top-up-instructions.

    Python has no typed response classes; ApiClient wraps parsed JSON in ResponseWrapper, which
    recursively wraps nested dicts (see ResponseWrapper._wrap). These tests build a wrapper from
    the spec's payloads and assert the attribute surface callers actually get.

    They cover plan tests 2, 3, 4 and 6. The plan assigned Python only tests 1 and 7 on the
    assumption that a response layer was needed for them, but ResponseWrapper provides exactly the
    present/absent semantics the rail-optionality criterion requires -- and without these the
    "both rails optional" acceptance criterion has no Python coverage at all, because the sandbox
    returns 403 so the integration test's success branch never executes.

    Every value is a field-level "example" from shared/swagger-latest.json.
    """

    FULL_RAIL = {
        'beneficiary_account_name': 'Acme Inc',
        'beneficiary_address': '1 Example Street, Exampleville, EX, 00000, US',
        'bank_name': 'Example Bank',
        'bank_address': '1 Example Street, Exampleville, EX, 00000, US',
        'account_number': '1234567890',
        'sort_code': '000000',
        'routing_number': '000000000',
        'iban': 'GB00EXAM00000000000000',
        'swift_code': 'TESTUS00XXX',
    }

    @staticmethod
    def _wrap(bank_details):
        return ResponseWrapper(None, {
            'currency_account_id': 'ca_g5y7d6jo4e2urgforcbf2ey5jm',
            'currency': 'USD',
            'payment_reference': 'TP-ABC123',
            'bank_details': bank_details,
        })

    def _assert_full_rail(self, rail):
        assert rail.beneficiary_account_name == 'Acme Inc'
        assert rail.beneficiary_address == '1 Example Street, Exampleville, EX, 00000, US'
        assert rail.bank_name == 'Example Bank'
        assert rail.bank_address == '1 Example Street, Exampleville, EX, 00000, US'
        assert rail.account_number == '1234567890'
        assert rail.sort_code == '000000'
        assert rail.routing_number == '000000000'
        assert rail.iban == 'GB00EXAM00000000000000'
        assert rail.swift_code == 'TESTUS00XXX'

    def test_should_expose_both_rails_and_all_fields(self):
        response = self._wrap({'domestic': dict(self.FULL_RAIL),
                               'international': dict(self.FULL_RAIL)})

        assert response.currency_account_id == 'ca_g5y7d6jo4e2urgforcbf2ey5jm'
        assert response.currency == 'USD'
        assert response.payment_reference == 'TP-ABC123'
        self._assert_full_rail(response.bank_details.domestic)
        self._assert_full_rail(response.bank_details.international)

    def test_should_expose_domestic_only(self):
        # A United States domestic rail, per "Returned for United States domestic transfers".
        response = self._wrap({'domestic': {
            'beneficiary_account_name': 'Acme Inc',
            'bank_name': 'Example Bank',
            'account_number': '1234567890',
            'routing_number': '000000000',
        }})

        assert not hasattr(response.bank_details, 'international')
        assert response.bank_details.domestic.routing_number == '000000000'
        assert not hasattr(response.bank_details.domestic, 'sort_code')
        assert not hasattr(response.bank_details.domestic, 'iban')
        assert not hasattr(response.bank_details.domestic, 'swift_code')

    def test_should_expose_international_only(self):
        # An international rail, per "Returned for international transfers".
        response = self._wrap({'international': {
            'beneficiary_account_name': 'Acme Inc',
            'bank_name': 'Example Bank',
            'iban': 'GB00EXAM00000000000000',
            'swift_code': 'TESTUS00XXX',
        }})

        assert not hasattr(response.bank_details, 'domestic')
        assert response.bank_details.international.swift_code == 'TESTUS00XXX'
        assert not hasattr(response.bank_details.international, 'account_number')
        assert not hasattr(response.bank_details.international, 'routing_number')

    def test_should_accept_empty_bank_details(self):
        # TopUpBankDetails declares no required properties, so an empty object is a legal 200 body.
        response = self._wrap({})

        assert response.payment_reference == 'TP-ABC123'
        assert not hasattr(response.bank_details, 'domestic')
        assert not hasattr(response.bank_details, 'international')
