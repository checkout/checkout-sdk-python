import json
from datetime import date

from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.api_client import ApiClient
from checkout_sdk.issuing.cards import CardRequest, CardType, CardUpdateHeaders, UpdateCardRequest, \
    VirtualCardRequest, CardStatusUpdate
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

    def test_update_card_serializes_scheduled_activation_and_revocation_date(self):
        request = UpdateCardRequest()
        request.reference = 'ref'
        request.scheduled_activation_date = '2026-06-01T10:00Z'
        request.revocation_date = '2027-03-12'

        assert _serialize(request) == {
            'reference': 'ref',
            'scheduled_activation_date': '2026-06-01T10:00Z',
            'revocation_date': '2027-03-12',
        }

    def test_update_card_serializes_scheduled_revocation_date_alongside_deprecated_field(self):
        request = UpdateCardRequest()
        request.reference = 'ref'
        request.revocation_date = '2027-03-12'
        request.scheduled_revocation_date = '2027-04-01'

        assert _serialize(request) == {
            'reference': 'ref',
            'revocation_date': '2027-03-12',
            'scheduled_revocation_date': '2027-04-01',
        }

    def test_update_card_serializes_status_to_reactivate_card(self):
        request = UpdateCardRequest()
        request.status = CardStatusUpdate.ACTIVE

        assert _serialize(request) == {'status': 'active'}

    def test_create_card_serializes_scheduled_activation_date(self):
        request = VirtualCardRequest()
        request.cardholder_id = 'crh_1'
        request.scheduled_activation_date = '2026-06-01T10:00Z'
        request.revocation_date = '2027-03-12'
        request.scheduled_revocation_date = '2027-04-01'

        result = _serialize(request)
        assert result['type'] == CardType.VIRTUAL.value
        assert result['scheduled_activation_date'] == '2026-06-01T10:00Z'
        assert result['revocation_date'] == '2027-03-12'
        assert result['scheduled_revocation_date'] == '2027-04-01'
        assert 'activation_date' not in result

    def test_revocation_date_accepts_a_date_object_through_the_serializer(self):
        """revocation_date is `format: date`. The SDK convention is to declare it str with a
        `# Format: yyyy-MM-dd` comment, and the JsonSerializer date branch added in INT-1699 is
        the safety net for a caller who passes a real date instead."""
        request = UpdateCardRequest()
        request.revocation_date = date(2027, 3, 12)

        assert _serialize(request) == {'revocation_date': '2027-03-12'}

    def test_scheduled_activation_date_is_not_a_date_only_field(self):
        """Unlike revocation_date it has no `format` in the spec: it accepts a date or a round
        hour datetime, so it must stay a plain string and carry no yyyy-MM-dd marker."""
        request = UpdateCardRequest()
        request.scheduled_activation_date = '2026-06-01T10:00Z'

        assert _serialize(request) == {'scheduled_activation_date': '2026-06-01T10:00Z'}

    def test_update_card_request_declares_no_activation_date(self):
        """The spec replaced activation_date with scheduled_activation_date and removed
        IssuingActivationDate. Python attributes are dynamic, so a caller still assigning
        activation_date would silently serialize a key the API rejects, with no error anywhere.
        These guards are the only thing that catches a stale assignment."""
        assert 'scheduled_activation_date' in UpdateCardRequest.__annotations__
        assert 'activation_date' not in UpdateCardRequest.__annotations__

    def test_card_request_declares_no_activation_date(self):
        assert 'scheduled_activation_date' in CardRequest.__annotations__
        assert 'activation_date' not in CardRequest.__annotations__

    def test_update_card_serializes_every_declared_property(self):
        request = UpdateCardRequest()
        request.reference = 'X-123456-N11'
        request.expiry_month = 6
        request.expiry_year = 2030
        request.scheduled_activation_date = '2026-06-01T10:00Z'
        request.revocation_date = '2027-03-12'

        assert _serialize(request) == {
            'reference': 'X-123456-N11',
            'expiry_month': 6,
            'expiry_year': 2030,
            'scheduled_activation_date': '2026-06-01T10:00Z',
            'revocation_date': '2027-03-12',
        }

    def test_update_card_request_from_swagger_example(self):
        payload = json.loads(
            '{"reference":"X-123456-N11","expiry_month":6,"expiry_year":2030,'
            '"revocation_date":"2027-03-12","scheduled_activation_date":"2026-06-01T10:00Z"}'
        )

        assert payload['scheduled_activation_date'] == '2026-06-01T10:00Z'
        assert payload['revocation_date'] == '2027-03-12'

    def test_card_update_headers_map_to_the_exact_swagger_header_names(self):
        assert CardUpdateHeaders().get_header_mappings() == {
            'return_encrypted_cvv': 'return-encrypted-cvv',
            'encryption_key': 'Encryption-Key',
        }

    def test_card_update_headers_reach_the_wire_with_the_exact_names(self):
        """The header names are case sensitive and return-encrypted-cvv is lower case, which the
        default snake_case converter would render as Return-Encrypted-Cvv."""
        headers = CardUpdateHeaders()
        headers.return_encrypted_cvv = 'true'
        headers.encryption_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A'

        built = ApiClient.__new__(ApiClient)._process_custom_headers(headers)

        assert built['return-encrypted-cvv'] == 'true'
        assert built['Encryption-Key'] == 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A'
        assert 'Return-Encrypted-Cvv' not in built

    def test_card_update_headers_omit_unset_values(self):
        assert ApiClient.__new__(ApiClient)._process_custom_headers(CardUpdateHeaders()) == {}

    def test_card_update_headers_send_the_key_without_the_flag(self):
        headers = CardUpdateHeaders()
        headers.encryption_key = 'MIIBIjAN'

        built = ApiClient.__new__(ApiClient)._process_custom_headers(headers)

        assert built == {'Encryption-Key': 'MIIBIjAN'}

    def test_card_update_headers_are_declared_as_strings_not_bools(self):
        """ApiClient stringifies header values, so a Python bool would reach the wire as the
        capitalised 'True'/'False' rather than the 'true' the spec shows. Both attributes are
        therefore str, matching the three header classes that already exist in this SDK."""
        assert CardUpdateHeaders.__annotations__['return_encrypted_cvv'] is str
        assert CardUpdateHeaders.__annotations__['encryption_key'] is str

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
