import json

from checkout_sdk.common.enums import Currency
from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.payments.payments import CardPayoutProcessing, NetworkTokenType, PaymentInstruction, \
    PaymentRequestCardDestination, PaymentRequestIdDestination, PaymentRequestNetworkTokenDestination, \
    PaymentRequestTokenDestination, PaymentSegment, PayoutRequestCurrencyAccountSource, UnreferencedRefundRequest
from tests.payments.card_payout_fixtures import ACCOUNT_HOLDER_FIXTURE, rich_account_holder

# The spec has no request example for UnreferencedRefundRequest; values below come from the
# per-property examples of the schema where it declares one (amount 120, segment, metadata,
# previous_payment_id) and otherwise from its patterns (source, processing channel, ids).
CARD_DESTINATION_FIXTURE = {
    'type': 'card',
    'number': '4242424242424242',
    'expiry_month': 6,
    'expiry_year': 2025,
    'account_holder': ACCOUNT_HOLDER_FIXTURE
}

NETWORK_TOKEN_DESTINATION_FIXTURE = {
    'type': 'network_token',
    'token': '4543474002249996',
    'expiry_month': 6,
    'expiry_year': 2025,
    'token_type': 'vts',
    'cryptogram': 'hv8mUFzPzRZoCAAAAAEQBDMAAAA=',
    'eci': '05',
    'account_holder': ACCOUNT_HOLDER_FIXTURE
}

ID_DESTINATION_FIXTURE = {
    'type': 'id',
    'id': 'src_wmlfc3zyhqzehihu7giusaaawu',
    'account_holder': ACCOUNT_HOLDER_FIXTURE
}

TOKEN_DESTINATION_FIXTURE = {
    'type': 'token',
    'token': 'tok_ubfj2q76miwundwlk72vxt2i7q',
    'account_holder': ACCOUNT_HOLDER_FIXTURE
}

REQUEST_FIXTURE = {
    'source': {'type': 'currency_account', 'id': 'ca_y3oqhf46pyzuxjbcn2giaqnb44'},
    'destination': CARD_DESTINATION_FIXTURE,
    'instruction': {'funds_transfer_type': 'MI', 'purpose': 'family_support'},
    'amount': 120,
    'currency': 'GBP',
    'payment_type': 'UnreferencedRefund',
    'processing_channel_id': 'pc_q4dbxom5jbgudnjzjpz7j2z6uq',
    'reference': 'ORD-5023-4E89',
    'metadata': {'coupon_code': 'NY2018', 'partner_id': 123989},
    'previous_payment_id': 'pay_fun26akvvjjerahhctaq2uzhu4',
    'segment': {'brand': 'Acme Corporation', 'business_category': 'Inward Payments', 'market': 'UK'},
    'processing': {'processing_speed': 'fast'}
}

REQUEST_KEYS = {'source', 'destination', 'instruction', 'amount', 'currency', 'payment_type',
                'processing_channel_id', 'reference', 'metadata', 'previous_payment_id', 'segment',
                'processing'}

REQUIRED_REQUEST_KEYS = {'source', 'destination', 'amount', 'currency', 'payment_type', 'processing_channel_id'}


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


def _card_destination():
    destination = PaymentRequestCardDestination()
    destination.number = '4242424242424242'
    destination.expiry_month = 6
    destination.expiry_year = 2025
    destination.account_holder = rich_account_holder()
    return destination


def _network_token_destination():
    destination = PaymentRequestNetworkTokenDestination()
    destination.token = '4543474002249996'
    destination.expiry_month = 6
    destination.expiry_year = 2025
    destination.token_type = NetworkTokenType.VTS
    destination.cryptogram = 'hv8mUFzPzRZoCAAAAAEQBDMAAAA='
    destination.eci = '05'
    destination.account_holder = rich_account_holder()
    return destination


def _id_destination(with_account_holder=True):
    destination = PaymentRequestIdDestination()
    destination.id = 'src_wmlfc3zyhqzehihu7giusaaawu'
    if with_account_holder:
        destination.account_holder = rich_account_holder()
    return destination


def _token_destination(with_account_holder=True):
    destination = PaymentRequestTokenDestination()
    destination.token = 'tok_ubfj2q76miwundwlk72vxt2i7q'
    if with_account_holder:
        destination.account_holder = rich_account_holder()
    return destination


def _full_request(destination=None):
    source = PayoutRequestCurrencyAccountSource()
    source.id = 'ca_y3oqhf46pyzuxjbcn2giaqnb44'

    instruction = PaymentInstruction()
    instruction.funds_transfer_type = 'MI'
    instruction.purpose = 'family_support'

    segment = PaymentSegment()
    segment.brand = 'Acme Corporation'
    segment.business_category = 'Inward Payments'
    segment.market = 'UK'

    processing = CardPayoutProcessing()
    processing.processing_speed = 'fast'

    request = UnreferencedRefundRequest()
    request.source = source
    request.destination = destination if destination is not None else _card_destination()
    request.instruction = instruction
    request.amount = 120
    request.currency = Currency.GBP
    request.processing_channel_id = 'pc_q4dbxom5jbgudnjzjpz7j2z6uq'
    request.reference = 'ORD-5023-4E89'
    request.metadata = {'coupon_code': 'NY2018', 'partner_id': 123989}
    request.previous_payment_id = 'pay_fun26akvvjjerahhctaq2uzhu4'
    request.segment = segment
    request.processing = processing
    return request


class TestUnreferencedRefundSerialization:

    def test_constructor_sets_payment_type_literal(self):
        request = UnreferencedRefundRequest()

        assert request.payment_type == 'UnreferencedRefund'
        assert _serialize(request) == {'payment_type': 'UnreferencedRefund'}

    def test_request_serializes_literal_wire_keys(self):
        serialized = _serialize(_full_request())

        assert set(serialized.keys()) == REQUEST_KEYS
        assert all(key == key.lower() for key in serialized.keys())

    def test_request_matches_fixture(self):
        serialized = _serialize(_full_request())

        assert serialized == REQUEST_FIXTURE
        assert isinstance(serialized['amount'], int)

    def test_request_with_only_required_properties(self):
        request = UnreferencedRefundRequest()
        source = PayoutRequestCurrencyAccountSource()
        source.id = 'ca_y3oqhf46pyzuxjbcn2giaqnb44'
        request.source = source
        request.destination = _token_destination(with_account_holder=False)
        request.amount = 120
        request.currency = Currency.GBP
        request.processing_channel_id = 'pc_q4dbxom5jbgudnjzjpz7j2z6uq'

        serialized = _serialize(request)

        assert set(serialized.keys()) == REQUIRED_REQUEST_KEYS
        assert serialized['source'] == REQUEST_FIXTURE['source']
        assert serialized['destination'] == {'type': 'token', 'token': 'tok_ubfj2q76miwundwlk72vxt2i7q'}

    def test_network_token_destination_nested_under_destination(self):
        serialized = _serialize(_full_request(_network_token_destination()))

        assert serialized['destination'] == NETWORK_TOKEN_DESTINATION_FIXTURE

    def test_id_destination_nested_under_destination(self):
        serialized = _serialize(_full_request(_id_destination()))

        assert serialized['destination'] == ID_DESTINATION_FIXTURE

    def test_token_destination_nested_under_destination(self):
        serialized = _serialize(_full_request(_token_destination()))

        assert serialized['destination'] == TOKEN_DESTINATION_FIXTURE

    def test_id_destination_omits_account_holder_when_unset(self):
        serialized = _serialize(_full_request(_id_destination(with_account_holder=False)))

        assert serialized['destination'] == {'type': 'id', 'id': 'src_wmlfc3zyhqzehihu7giusaaawu'}

    def test_token_destination_omits_account_holder_when_unset(self):
        serialized = _serialize(_full_request(_token_destination(with_account_holder=False)))

        assert serialized['destination'] == {'type': 'token', 'token': 'tok_ubfj2q76miwundwlk72vxt2i7q'}

    def test_request_round_trip(self):
        request = _full_request()

        decoded = json.loads(json.dumps(request, cls=JsonSerializer))

        assert decoded['source'] == {'type': request.source.type.value, 'id': request.source.id}
        assert decoded['instruction'] == {
            'funds_transfer_type': request.instruction.funds_transfer_type,
            'purpose': request.instruction.purpose}
        assert decoded['amount'] == request.amount
        assert decoded['currency'] == request.currency.value
        assert decoded['payment_type'] == request.payment_type
        assert decoded['processing_channel_id'] == request.processing_channel_id
        assert decoded['reference'] == request.reference
        assert decoded['metadata'] == request.metadata
        assert decoded['previous_payment_id'] == request.previous_payment_id
        assert decoded['segment'] == {
            'brand': request.segment.brand,
            'business_category': request.segment.business_category,
            'market': request.segment.market}
        assert decoded['processing'] == {'processing_speed': request.processing.processing_speed}
        destination = request.destination
        decoded_destination = decoded['destination']
        assert decoded_destination['type'] == destination.type.value
        assert decoded_destination['number'] == destination.number
        assert decoded_destination['expiry_month'] == destination.expiry_month
        assert decoded_destination['expiry_year'] == destination.expiry_year
        holder = destination.account_holder
        decoded_holder = decoded_destination['account_holder']
        assert decoded_holder['type'] == holder.type.value
        assert decoded_holder['first_name'] == holder.first_name
        assert decoded_holder['middle_name'] == holder.middle_name
        assert decoded_holder['last_name'] == holder.last_name
        assert decoded_holder['email'] == holder.email
        assert decoded_holder['date_of_birth'] == holder.date_of_birth
        assert decoded_holder['country_of_birth'] == holder.country_of_birth.value
        assert decoded_holder['billing_address'] == {
            'address_line1': holder.billing_address.address_line1,
            'address_line2': holder.billing_address.address_line2,
            'city': holder.billing_address.city,
            'state': holder.billing_address.state,
            'zip': holder.billing_address.zip,
            'country': holder.billing_address.country.value}
        assert decoded_holder['phone'] == {
            'country_code': holder.phone.country_code,
            'number': holder.phone.number}
        assert decoded_holder['identification'] == {
            'type': holder.identification.type.value,
            'number': holder.identification.number,
            'issuing_country': holder.identification.issuing_country.value,
            'date_of_expiry': holder.identification.date_of_expiry}
