import json

from checkout_sdk.common.common import AccountHolder, BankDetails
from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.payments.payments import InstructionScheme, PaymentBankAccountDestination, PaymentInstruction, \
    PayoutRequest


# Deprecated payout members are retained for backwards compatibility until the next major version, so
# they must keep serializing under their wire keys.
def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class TestDeprecatedPayoutMembersSerialization:

    def test_deprecated_instruction_members_still_serialize(self):
        instruction = PaymentInstruction()
        instruction.charge_bearer = 'OUR'
        instruction.repair = True
        instruction.quote_id = 'qte_mbabizu24mvu3mela5njyhpit4'
        instruction.scheme = InstructionScheme.SWIFT
        request = PayoutRequest()
        request.instruction = instruction

        assert _serialize(request)['instruction'] == {
            'charge_bearer': 'OUR',
            'repair': True,
            'quote_id': 'qte_mbabizu24mvu3mela5njyhpit4',
            'scheme': 'swift'
        }

    def test_deprecated_bank_account_destination_bank_still_serializes(self):
        bank = BankDetails()
        bank.name = 'Lloyds TSB'
        bank.branch = 'Bournemouth'
        destination = PaymentBankAccountDestination()
        destination.bank = bank
        request = PayoutRequest()
        request.destination = destination

        decoded = _serialize(request)['destination']

        assert decoded['bank'] == {'name': 'Lloyds TSB', 'branch': 'Bournemouth'}
        assert decoded['type'] == 'bank_account'

    def test_deprecated_account_holder_full_name_and_gender_still_serialize(self):
        account_holder = AccountHolder()
        account_holder.full_name = 'John Smith'
        account_holder.gender = 'male'

        assert _serialize(account_holder) == {'full_name': 'John Smith', 'gender': 'male'}
