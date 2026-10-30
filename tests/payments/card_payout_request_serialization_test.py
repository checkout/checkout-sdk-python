import json

from checkout_sdk.common.common import AccountHolderIdentification, Address
from checkout_sdk.common.enums import AccountHolderIdentificationType, Country, Currency
from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.payments.payments import CardPayoutItem, CardPayoutProcessing, ItemType, \
    PaymentIndividualSender, PaymentInstruction, PaymentRequestCardDestination, PaymentSegment, PayoutRequest, \
    PayoutRequestCurrencyAccountSource, ProductSubType, SourceOfFunds
from tests.payments.card_payout_fixtures import ACCOUNT_HOLDER_FIXTURE, rich_account_holder

# The spec has no request example for CardPayoutRequest; values below come from the per-property
# examples where the schema declares one (items, previous_payment_id, segment, affiliate_url,
# purchase_country) and otherwise satisfy the property's pattern and length.
REQUEST_FIXTURE = {
    'source': {'type': 'currency_account', 'id': 'ca_y3oqhf46pyzuxjbcn2giaqnb44'},
    'destination': {
        'type': 'card',
        'number': '4242424242424242',
        'expiry_month': 6,
        'expiry_year': 2025,
        'account_holder': ACCOUNT_HOLDER_FIXTURE
    },
    'amount': 1000,
    'currency': 'GBP',
    'instruction': {'purpose': 'family_support', 'funds_transfer_type': 'FD'},
    'items': [{'type': 'digital', 'sub_type': 'stablecoin'}],
    'processing_channel_id': 'pc_q4dbxom5jbgudnjzjpz7j2z6uq',
    'sender': {
        'type': 'individual',
        'first_name': 'John',
        'last_name': 'Jones',
        'address': {
            'address_line1': '123 High St.',
            'city': 'London',
            'country': 'GB'
        },
        'reference': 'CUST8285282045',
        'reference_type': 'other',
        'source_of_funds': 'debit',
        'identification': {
            'type': 'passport',
            'number': 'E12345678',
            'issuing_country': 'GB',
            'date_of_expiry': '2030-01-01'
        },
        'date_of_birth': '1985-05-15',
        'country_of_birth': 'GB',
        'nationality': 'GB'
    },
    'reference': 'ORD-5023-4E89',
    'previous_payment_id': 'pay_fun26akvvjjerahhctaq2uzhu4',
    'metadata': {'coupon_code': 'NY2018', 'partner_id': 123989},
    'segment': {'brand': 'Acme Corporation', 'business_category': 'Inward Payments', 'market': 'UK'},
    'processing': {
        'affiliate_id': 'AFF12345',
        'affiliate_url': 'www.mycrypto.com',
        'purchase_country': 'GB'
    }
}

REQUEST_KEYS = {'source', 'destination', 'amount', 'currency', 'instruction', 'items', 'processing_channel_id',
                'sender', 'reference', 'previous_payment_id', 'metadata', 'segment', 'processing'}


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


def _sender():
    address = Address()
    address.address_line1 = '123 High St.'
    address.city = 'London'
    address.country = Country.GB

    identification = AccountHolderIdentification()
    identification.type = AccountHolderIdentificationType.PASSPORT
    identification.number = 'E12345678'
    identification.issuing_country = Country.GB
    identification.date_of_expiry = '2030-01-01'

    sender = PaymentIndividualSender()
    sender.first_name = 'John'
    sender.last_name = 'Jones'
    sender.address = address
    sender.reference = 'CUST8285282045'
    sender.reference_type = 'other'
    sender.source_of_funds = SourceOfFunds.DEBIT
    sender.identification = identification
    sender.date_of_birth = '1985-05-15'
    sender.country_of_birth = Country.GB
    sender.nationality = Country.GB
    return sender


def _full_request():
    source = PayoutRequestCurrencyAccountSource()
    source.id = 'ca_y3oqhf46pyzuxjbcn2giaqnb44'

    destination = PaymentRequestCardDestination()
    destination.number = '4242424242424242'
    destination.expiry_month = 6
    destination.expiry_year = 2025
    destination.account_holder = rich_account_holder()

    instruction = PaymentInstruction()
    instruction.purpose = 'family_support'
    instruction.funds_transfer_type = 'FD'

    item = CardPayoutItem()
    item.type = ItemType.DIGITAL
    item.sub_type = ProductSubType.STABLECOIN

    segment = PaymentSegment()
    segment.brand = 'Acme Corporation'
    segment.business_category = 'Inward Payments'
    segment.market = 'UK'

    processing = CardPayoutProcessing()
    processing.affiliate_id = 'AFF12345'
    processing.affiliate_url = 'www.mycrypto.com'
    processing.purchase_country = Country.GB

    request = PayoutRequest()
    request.source = source
    request.destination = destination
    request.amount = 1000
    request.currency = Currency.GBP
    request.instruction = instruction
    request.items = [item]
    request.processing_channel_id = 'pc_q4dbxom5jbgudnjzjpz7j2z6uq'
    request.sender = _sender()
    request.reference = 'ORD-5023-4E89'
    request.previous_payment_id = 'pay_fun26akvvjjerahhctaq2uzhu4'
    request.metadata = {'coupon_code': 'NY2018', 'partner_id': 123989}
    request.segment = segment
    request.processing = processing
    return request


class TestCardPayoutRequestSerialization:

    def test_request_serializes_literal_wire_keys(self):
        serialized = _serialize(_full_request())

        assert set(serialized.keys()) == REQUEST_KEYS
        assert all(key == key.lower() for key in serialized.keys())

    def test_request_matches_fixture(self):
        serialized = _serialize(_full_request())

        assert serialized == REQUEST_FIXTURE
        assert isinstance(serialized['amount'], int)

    def test_card_payout_processing_serializes_every_property(self):
        processing = CardPayoutProcessing()
        processing.affiliate_id = 'AFF12345'
        processing.affiliate_url = 'www.mycrypto.com'
        processing.processing_speed = 'fast'
        processing.purchase_country = Country.GB

        assert _serialize(processing) == {'affiliate_id': 'AFF12345', 'affiliate_url': 'www.mycrypto.com',
                                          'processing_speed': 'fast', 'purchase_country': 'GB'}

    def test_card_payout_processing_omits_unset_fields_instead_of_sending_null(self):
        assert _serialize(CardPayoutProcessing()) == {}

    def test_request_round_trip(self):
        request = _full_request()

        decoded = json.loads(json.dumps(request, cls=JsonSerializer))

        assert decoded['source'] == {'type': request.source.type.value, 'id': request.source.id}
        assert decoded['destination']['type'] == request.destination.type.value
        assert decoded['destination']['number'] == request.destination.number
        assert decoded['destination']['account_holder']['first_name'] == request.destination.account_holder.first_name
        assert decoded['amount'] == request.amount
        assert decoded['currency'] == request.currency.value
        assert decoded['instruction'] == {
            'purpose': request.instruction.purpose,
            'funds_transfer_type': request.instruction.funds_transfer_type}
        assert decoded['items'] == [{'type': request.items[0].type.value, 'sub_type': request.items[0].sub_type.value}]
        assert decoded['processing_channel_id'] == request.processing_channel_id
        sender = request.sender
        assert decoded['sender'] == {
            'type': sender.type.value,
            'first_name': sender.first_name,
            'last_name': sender.last_name,
            'address': {
                'address_line1': sender.address.address_line1,
                'city': sender.address.city,
                'country': sender.address.country.value},
            'reference': sender.reference,
            'reference_type': sender.reference_type,
            'source_of_funds': sender.source_of_funds.value,
            'identification': {
                'type': sender.identification.type.value,
                'number': sender.identification.number,
                'issuing_country': sender.identification.issuing_country.value,
                'date_of_expiry': sender.identification.date_of_expiry},
            'date_of_birth': sender.date_of_birth,
            'country_of_birth': sender.country_of_birth.value,
            'nationality': sender.nationality.value}
        assert decoded['reference'] == request.reference
        assert decoded['previous_payment_id'] == request.previous_payment_id
        assert decoded['metadata'] == request.metadata
        assert decoded['segment'] == {
            'brand': request.segment.brand,
            'business_category': request.segment.business_category,
            'market': request.segment.market}
        assert decoded['processing'] == {
            'affiliate_id': request.processing.affiliate_id,
            'affiliate_url': request.processing.affiliate_url,
            'purchase_country': request.processing.purchase_country.value}
