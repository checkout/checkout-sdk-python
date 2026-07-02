import json

from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.issuing.cards import CardType, VirtualCardRequest, UpdateCardRequest
from checkout_sdk.issuing.disputes import (
    IssuingDisputeFraudType, IssuingDisputeFraudDetails, CreateDisputeRequest,
    EscalateDisputeRequest, AmendDisputeRequest, SubmitDisputeRequest,
)


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class TestIssuingSerialization:

    def test_fraud_type_enum_matches_swagger_strings(self):
        expected = {
            'CARD_LOST': 'card_lost',
            'CARD_STOLEN': 'card_stolen',
            'CARD_NEVER_RECEIVED': 'card_never_received',
            'FRAUDULENT_ACCOUNT': 'fraudulent_account',
            'COUNTERFEIT_CARD': 'counterfeit_card',
            'ACCOUNT_TAKEOVER': 'account_takeover',
            'CARD_NOT_PRESENT_FRAUD': 'card_not_present_fraud',
            'MERCHANT_MISREPRESENTATION': 'merchant_misrepresentation',
            'CARDHOLDER_MANIPULATION': 'cardholder_manipulation',
            'INCORRECT_PROCESSING': 'incorrect_processing',
            'OTHER': 'other',
        }
        actual = {member.name: member.value for member in IssuingDisputeFraudType}
        assert actual == expected

    def test_update_card_serializes_activation_and_revocation_date(self):
        request = UpdateCardRequest()
        request.reference = 'ref'
        request.activation_date = '2026-06-01T10:00Z'
        request.revocation_date = '2027-03-12'

        assert _serialize(request) == {
            'reference': 'ref',
            'activation_date': '2026-06-01T10:00Z',
            'revocation_date': '2027-03-12',
        }

    def test_create_card_serializes_activation_date(self):
        request = VirtualCardRequest()
        request.cardholder_id = 'crh_1'
        request.activation_date = '2026-06-01T10:00Z'
        request.revocation_date = '2027-03-12'

        result = _serialize(request)
        assert result['type'] == CardType.VIRTUAL.value
        assert result['activation_date'] == '2026-06-01T10:00Z'
        assert result['revocation_date'] == '2027-03-12'

    def test_create_dispute_serializes_fraud_details(self):
        fraud_details = IssuingDisputeFraudDetails()
        fraud_details.fraud_type = IssuingDisputeFraudType.COUNTERFEIT_CARD
        fraud_details.description = 'duplicate card used'

        request = CreateDisputeRequest()
        request.transaction_id = 'txn_1'
        request.reason = '4808'
        request.fraud_details = fraud_details

        assert _serialize(request) == {
            'transaction_id': 'txn_1',
            'reason': '4808',
            'fraud_details': {'fraud_type': 'counterfeit_card', 'description': 'duplicate card used'},
        }

    def test_escalate_dispute_serializes_fraud_details(self):
        fraud_details = IssuingDisputeFraudDetails()
        fraud_details.fraud_type = IssuingDisputeFraudType.ACCOUNT_TAKEOVER

        request = EscalateDisputeRequest()
        request.justification = 'reason'
        request.fraud_details = fraud_details

        assert _serialize(request) == {
            'justification': 'reason',
            'fraud_details': {'fraud_type': 'account_takeover'},
        }

    def test_amend_dispute_serializes_all_fields(self):
        fraud_details = IssuingDisputeFraudDetails()
        fraud_details.fraud_type = IssuingDisputeFraudType.OTHER

        request = AmendDisputeRequest()
        request.reason = '4807'
        request.amount = 1500
        request.evidence = [{'evidence_type': 'proof_of_purchase'}]
        request.fraud_details = fraud_details
        request.reason_change_justification = 'updated reason'
        request.action_response = 'answering requested changes'

        assert _serialize(request) == {
            'reason': '4807',
            'amount': 1500,
            'evidence': [{'evidence_type': 'proof_of_purchase'}],
            'fraud_details': {'fraud_type': 'other'},
            'reason_change_justification': 'updated reason',
            'action_response': 'answering requested changes',
        }

    def test_submit_dispute_serializes_fields(self):
        request = SubmitDisputeRequest()
        request.reason = '4807'
        request.amount = 100

        assert _serialize(request) == {'reason': '4807', 'amount': 100}
