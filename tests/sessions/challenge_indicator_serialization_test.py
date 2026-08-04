import json

import pytest

from checkout_sdk.common.enums import ChallengeIndicator
from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.payments.payments import ThreeDsRequest
from checkout_sdk.sessions.sessions import SessionChallengeIndicator, SessionRequest

# The nine values accepted by SessionRequest.challenge_indicator, per the API Reference
# ChallengeIndicator schema, in spec order.
SESSION_VALUES = [
    'no_preference',
    'no_challenge_requested',
    'challenge_requested',
    'challenge_requested_mandate',
    'low_value',
    'trusted_listing',
    'trusted_listing_prompt',
    'transaction_risk_assessment',
    'data_share',
]

# The four values accepted by the 3ds.challenge_indicator field on payments, hosted payments,
# payment links and payment sessions.
PAYMENT_VALUES = [
    'no_preference',
    'no_challenge_requested',
    'challenge_requested',
    'challenge_requested_mandate',
]


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class TestChallengeIndicatorSerialization:
    """Covers the two challenge-indicator enums and their call sites: the nine-value sessions enum
    used by POST /sessions, and the four-value shared enum used by the payments 3ds field.
    """

    def test_session_enum_exposes_all_nine_spec_values_in_order(self):
        assert [member.value for member in SessionChallengeIndicator] == SESSION_VALUES

    def test_shared_enum_exposes_only_the_four_payment_values(self):
        assert [member.value for member in ChallengeIndicator] == PAYMENT_VALUES

    @pytest.mark.parametrize('value', SESSION_VALUES)
    def test_every_session_value_serializes_on_session_request(self, value):
        request = SessionRequest()
        request.challenge_indicator = SessionChallengeIndicator(value)

        assert _serialize(request)['challenge_indicator'] == value

    def test_session_request_defaults_to_no_preference(self):
        request = SessionRequest()

        assert request.challenge_indicator == SessionChallengeIndicator.NO_PREFERENCE
        assert _serialize(request)['challenge_indicator'] == 'no_preference'

    @pytest.mark.parametrize('value', PAYMENT_VALUES)
    def test_every_payment_value_serializes_on_three_ds_request(self, value):
        request = ThreeDsRequest()
        request.challenge_indicator = ChallengeIndicator(value)

        assert _serialize(request)['challenge_indicator'] == value

    @pytest.mark.parametrize('value', SESSION_VALUES)
    def test_every_session_value_round_trips_through_the_enum(self, value):
        assert SessionChallengeIndicator(value).value == value

    def test_the_five_exemption_values_are_absent_from_the_shared_enum(self):
        """The exemption values must not leak onto the payments enum: the API rejects them on
        3ds.challenge_indicator. This is the guard the split exists to provide.
        """
        exemptions = {
            'low_value',
            'trusted_listing',
            'trusted_listing_prompt',
            'transaction_risk_assessment',
            'data_share',
        }
        shared = {member.value for member in ChallengeIndicator}

        assert exemptions.isdisjoint(shared)
        assert exemptions.issubset({member.value for member in SessionChallengeIndicator})
