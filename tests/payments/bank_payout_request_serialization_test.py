import json

from checkout_sdk.common.common import AccountHolder, AccountHolderIdentification, Address, Phone, \
    ResidentialStatusType
from checkout_sdk.common.enums import AccountHolderIdentificationType, AccountHolderType, AccountType, Country, \
    Currency
from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.payments.payments import InstructionScheme, PaymentBankAccountDestination, \
    PaymentIndividualSender, PaymentInstruction, PaymentSegment, PayoutBillingDescriptor, PayoutRequest, \
    PayoutRequestEntitySource, Remitance

# The spec has no request example for BankPayoutRequest; values below come from the per-property
# examples where the schema declares one and otherwise satisfy the property's pattern and length.
# The spec examples for date_of_birth and dob carry a time part although the description asks for
# YYYY-MM-DD, so the date part is used.
BILLING_ADDRESS_FIXTURE = {
    'address_line1': '123 High St.',
    'address_line2': 'Flat 456',
    'city': 'London',
    'zip': 'SW1A 1AA',
    'country': 'GB'
}

REQUEST_FIXTURE = {
    'source': {'type': 'entity', 'id': 'ent_w4jelhppmfiufdnatam37wrfc4'},
    'destination': {
        'type': 'bank_account',
        'account_type': 'savings',
        'account_number': '13654567455',
        'bank_code': '123-456',
        'branch_code': '6443',
        'bban': '3704 0044 0532 0130 00',
        'iban': 'HU93116000060000000012345676',
        'swift_bic': '37040044',
        'country': 'GB',
        'account_holder': {
            'type': 'individual',
            'first_name': 'John',
            'last_name': 'Smith',
            'tax_id': '123456',
            'date_of_birth': '1986-01-01',
            'country_of_birth': 'GB',
            'residential_status': 'resident',
            'billing_address': BILLING_ADDRESS_FIXTURE,
            'phone': {'country_code': '+1', 'number': '415 555 2671'},
            'identification': {'type': 'passport', 'number': 'E12345678', 'issuing_country': 'GB'}
        }
    },
    'amount': 6540,
    'currency': 'USD',
    'reference': 'Withdrawal',
    'billing_descriptor': {'reference': 'WITHDRAWAL01'},
    'sender': {
        'type': 'individual',
        'reference': '8285282045818',
        'first_name': 'John',
        'last_name': 'Jones',
        'dob': '1985-05-15',
        'address': BILLING_ADDRESS_FIXTURE,
        'identification': {'type': 'driving_licence', 'number': '1234', 'issuing_country': 'GT'}
    },
    'instruction': {'scheme': 'local', 'remittance': {'reference': 'INV-2026-0001'}},
    'processing_channel_id': 'pc_q4dbxom5jbgudnjzjpz7j2z6uq',
    'segment': {'brand': 'Acme Corporation', 'business_category': 'Inward Payments', 'market': 'UK'}
}

REQUEST_KEYS = {'source', 'destination', 'amount', 'currency', 'reference', 'billing_descriptor', 'sender',
                'instruction', 'processing_channel_id', 'segment'}


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


def _address():
    address = Address()
    address.address_line1 = '123 High St.'
    address.address_line2 = 'Flat 456'
    address.city = 'London'
    address.zip = 'SW1A 1AA'
    address.country = Country.GB
    return address


def _destination():
    phone = Phone()
    phone.country_code = '+1'
    phone.number = '415 555 2671'

    identification = AccountHolderIdentification()
    identification.type = AccountHolderIdentificationType.PASSPORT
    identification.number = 'E12345678'
    identification.issuing_country = Country.GB

    account_holder = AccountHolder()
    account_holder.type = AccountHolderType.INDIVIDUAL
    account_holder.first_name = 'John'
    account_holder.last_name = 'Smith'
    account_holder.tax_id = '123456'
    account_holder.date_of_birth = '1986-01-01'
    account_holder.country_of_birth = Country.GB
    account_holder.residential_status = ResidentialStatusType.RESIDENT
    account_holder.billing_address = _address()
    account_holder.phone = phone
    account_holder.identification = identification

    destination = PaymentBankAccountDestination()
    destination.account_type = AccountType.SAVINGS
    destination.account_number = '13654567455'
    destination.bank_code = '123-456'
    destination.branch_code = '6443'
    destination.bban = '3704 0044 0532 0130 00'
    destination.iban = 'HU93116000060000000012345676'
    destination.swift_bic = '37040044'
    destination.country = Country.GB
    destination.account_holder = account_holder
    return destination


def _sender():
    identification = AccountHolderIdentification()
    identification.type = AccountHolderIdentificationType.DRIVING_LICENSE
    identification.number = '1234'
    identification.issuing_country = Country.GT

    sender = PaymentIndividualSender()
    sender.reference = '8285282045818'
    sender.first_name = 'John'
    sender.last_name = 'Jones'
    sender.dob = '1985-05-15'
    sender.address = _address()
    sender.identification = identification
    return sender


def _full_request():
    source = PayoutRequestEntitySource()
    source.id = 'ent_w4jelhppmfiufdnatam37wrfc4'

    billing_descriptor = PayoutBillingDescriptor()
    billing_descriptor.reference = 'WITHDRAWAL01'

    remittance = Remitance()
    remittance.reference = 'INV-2026-0001'
    instruction = PaymentInstruction()
    instruction.scheme = InstructionScheme.LOCAL
    instruction.remittance = remittance

    segment = PaymentSegment()
    segment.brand = 'Acme Corporation'
    segment.business_category = 'Inward Payments'
    segment.market = 'UK'

    request = PayoutRequest()
    request.source = source
    request.destination = _destination()
    request.amount = 6540
    request.currency = Currency.USD
    request.reference = 'Withdrawal'
    request.billing_descriptor = billing_descriptor
    request.sender = _sender()
    request.instruction = instruction
    request.processing_channel_id = 'pc_q4dbxom5jbgudnjzjpz7j2z6uq'
    request.segment = segment
    return request


class TestBankPayoutRequestSerialization:

    def test_request_serializes_literal_wire_keys(self):
        serialized = _serialize(_full_request())

        assert set(serialized.keys()) == REQUEST_KEYS
        assert all(key == key.lower() for key in serialized.keys())

    def test_request_matches_fixture(self):
        serialized = _serialize(_full_request())

        assert serialized == REQUEST_FIXTURE
        assert isinstance(serialized['amount'], int)

    def test_request_round_trip(self):
        request = _full_request()

        decoded = json.loads(json.dumps(request, cls=JsonSerializer))

        assert decoded['source'] == {'type': request.source.type.value, 'id': request.source.id}
        destination = request.destination
        decoded_destination = decoded['destination']
        assert decoded_destination['type'] == destination.type.value
        assert decoded_destination['account_type'] == destination.account_type.value
        assert decoded_destination['account_number'] == destination.account_number
        assert decoded_destination['bank_code'] == destination.bank_code
        assert decoded_destination['branch_code'] == destination.branch_code
        assert decoded_destination['bban'] == destination.bban
        assert decoded_destination['iban'] == destination.iban
        assert decoded_destination['swift_bic'] == destination.swift_bic
        assert decoded_destination['country'] == destination.country.value
        holder = destination.account_holder
        decoded_holder = decoded_destination['account_holder']
        assert decoded_holder['type'] == holder.type.value
        assert decoded_holder['first_name'] == holder.first_name
        assert decoded_holder['last_name'] == holder.last_name
        assert decoded_holder['tax_id'] == holder.tax_id
        assert decoded_holder['date_of_birth'] == holder.date_of_birth
        assert decoded_holder['country_of_birth'] == holder.country_of_birth.value
        assert decoded_holder['residential_status'] == holder.residential_status.value
        assert decoded_holder['billing_address']['address_line1'] == holder.billing_address.address_line1
        assert decoded_holder['phone'] == {'country_code': holder.phone.country_code, 'number': holder.phone.number}
        assert decoded_holder['identification'] == {
            'type': holder.identification.type.value,
            'number': holder.identification.number,
            'issuing_country': holder.identification.issuing_country.value}
        assert decoded['amount'] == request.amount
        assert decoded['currency'] == request.currency.value
        assert decoded['reference'] == request.reference
        assert decoded['billing_descriptor'] == {'reference': request.billing_descriptor.reference}
        sender = request.sender
        assert decoded['sender']['type'] == sender.type.value
        assert decoded['sender']['reference'] == sender.reference
        assert decoded['sender']['first_name'] == sender.first_name
        assert decoded['sender']['last_name'] == sender.last_name
        assert decoded['sender']['dob'] == sender.dob
        assert decoded['sender']['address']['city'] == sender.address.city
        assert decoded['sender']['identification'] == {
            'type': sender.identification.type.value,
            'number': sender.identification.number,
            'issuing_country': sender.identification.issuing_country.value}
        assert decoded['instruction'] == {
            'scheme': request.instruction.scheme.value,
            'remittance': {'reference': request.instruction.remittance.reference}}
        assert decoded['processing_channel_id'] == request.processing_channel_id
        assert decoded['segment'] == {
            'brand': request.segment.brand,
            'business_category': request.segment.business_category,
            'market': request.segment.market}
