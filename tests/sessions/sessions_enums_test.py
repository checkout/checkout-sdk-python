import inspect
import re
from enum import Enum

import pytest

from checkout_sdk.sessions import sessions as sessions_module
from checkout_sdk.sessions.sessions import (
    AuthenticationType,
    BrowserSession,
    Category,
    ChannelData,
    SessionCardSource,
    SessionScheme,
    SessionSource,
    SessionsBillingDescriptor,
    ShippingIndicator,
    ThreeDsMethodCompletion,
    TransactionType,
)

# Value sets defined by the Checkout.com API Reference. These enums carry the raw wire values sent
# to and returned by the API, so a typo is invisible at development time and only fails against the
# live API.
SPEC_VALUES = {
    'Category': ['payment', 'non_payment'],
    'TransactionType': [
        'goods_service',
        'check_acceptance',
        'account_funding',
        'quasi_card_transaction',
        'prepaid_activation_and_load',
    ],
    'AuthenticationType': ['regular', 'recurring', 'installment', 'maintain_card', 'add_card'],
    'SessionScheme': [
        'visa',
        'mastercard',
        'jcb',
        'amex',
        'diners',
        'cartes_bancaires',
        'discover',
        'upi',
    ],
    'ThreeDsMethodCompletion': ['Y', 'N', 'U'],
    'ShippingIndicator': [
        'billing_address',
        'another_address_on_file',
        'not_on_file',
        'store_pick_up',
        'digital_goods',
        'travel_and_event_no_shipping',
        'other',
    ],
}

ENUMS_UNDER_TEST = {
    'Category': Category,
    'TransactionType': TransactionType,
    'AuthenticationType': AuthenticationType,
    'SessionScheme': SessionScheme,
    'ThreeDsMethodCompletion': ThreeDsMethodCompletion,
    'ShippingIndicator': ShippingIndicator,
}

# An API value is snake_case, or a single uppercase letter for the Y/N/U style codes.
VALID_VALUE = re.compile(r'^([a-z0-9_]+|[A-Z])$')


class TestSessionsEnums:
    """Spec-conformance guards for the sessions enums."""

    @pytest.mark.parametrize('name', sorted(SPEC_VALUES))
    def test_enum_matches_spec_value_set(self, name):
        expected = sorted(SPEC_VALUES[name])
        actual = sorted(member.value for member in ENUMS_UNDER_TEST[name])

        assert actual == expected

    def test_shipping_indicator_covers_all_seven_spec_values(self):
        """Guards a regression where this enum held a single wrong member, VISA = 'visa', leaving
        MerchantRiskInfo.shipping_indicator unusable.
        """
        assert len(list(ShippingIndicator)) == 7
        assert 'visa' not in {member.value for member in ShippingIndicator}

    def test_three_ds_method_completion_is_uppercase(self):
        """The spec enum is Y/N/U. Lowercase values are rejected by the API."""
        assert [member.value for member in ThreeDsMethodCompletion] == ['Y', 'N', 'U']

    def test_browser_session_covers_every_spec_field(self):
        """The spec Browser schema has 14 properties. iframe_payment_allowed and
        user_agent_client_hint were previously missing, so Google SPA support could not be signalled.
        """
        expected = {
            'channel',
            'three_ds_method_completion',
            'accept_header',
            'java_enabled',
            'javascript_enabled',
            'language',
            'color_depth',
            'screen_height',
            'screen_width',
            'timezone',
            'user_agent',
            'ip_address',
            'iframe_payment_allowed',
            'user_agent_client_hint',
        }
        declared = set(BrowserSession.__annotations__) | set(ChannelData.__annotations__)

        assert declared == expected

    def test_sessions_billing_descriptor_declares_only_name(self):
        """The sessions schema defines only `name`. city and reference belong to the payments
        billing descriptor and are not accepted here.
        """
        assert set(SessionsBillingDescriptor.__annotations__) == {'name'}

    def test_session_card_source_does_not_declare_store_for_future_use(self):
        """The sessions CardSource schema has no store_for_future_use; that field belongs to the
        payments sources, which create an instrument.
        """
        declared = set(SessionCardSource.__annotations__) | set(SessionSource.__annotations__)

        assert 'store_for_future_use' not in declared
        assert declared == {'type', 'scheme', 'billing_address', 'home_phone', 'mobile_phone',
                            'work_phone', 'email', 'number', 'expiry_month', 'expiry_year',
                            'name', 'stored'}

    def test_every_sessions_enum_value_is_snake_case_or_single_uppercase_code(self):
        """Structural guard across every enum in the sessions module. Catches camelCase or wrong
        casing leaking into a wire value.
        """
        checked = 0

        for _, obj in inspect.getmembers(sessions_module, inspect.isclass):
            if not issubclass(obj, Enum) or obj is Enum:
                continue
            if obj.__module__ != sessions_module.__name__:
                continue

            for member in obj:
                checked += 1
                assert VALID_VALUE.match(member.value), (
                    f'{obj.__name__}.{member.name} = {member.value!r} is not a valid API value'
                )

        assert checked > 50, f'expected to check more than 50 session enum values, checked {checked}'
