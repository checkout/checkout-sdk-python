import json

from checkout_sdk.common.common import AccountHolder, AccountHolderIdentification, Address, Phone
from checkout_sdk.common.enums import AccountHolderIdentificationType, AccountHolderType, Country
from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.payments.payments import NetworkTokenType, PaymentDestinationType, \
    PaymentRequestCardDestination, PaymentRequestNetworkTokenDestination, PaymentRequestTokenDestination, \
    PayoutRequest

# Spec example for 02_CardPayoutRequest_DestinationTypeNetworkToken; vts is the first token_type enum value.
NETWORK_TOKEN_FIXTURE = {
    'type': 'network_token',
    'token': '4543474002249996',
    'expiry_month': 6,
    'expiry_year': 2025,
    'token_type': 'vts',
    'cryptogram': 'hv8mUFzPzRZoCAAAAAEQBDMAAAA=',
    'eci': '05',
    'account_holder': {
        'type': 'individual',
        'first_name': 'John',
        'middle_name': 'Paul',
        'last_name': 'Smith',
        'billing_address': {
            'address_line1': '123 High St.',
            'address_line2': 'Flat 456',
            'city': 'London',
            'state': 'GB',
            'zip': 'SW1A 1AA',
            'country': 'GB'
        },
        'phone': {'country_code': '+44', 'number': '4155552671'},
        'identification': {
            'type': 'passport',
            'number': 'E12345678',
            'issuing_country': 'GB',
            'date_of_expiry': '2030-01-01'
        },
        'email': 'john.smith@example.com',
        'date_of_birth': '1985-05-15',
        'country_of_birth': 'GB'
    }
}

REQUIRED_NETWORK_TOKEN_KEYS = {'type', 'token', 'expiry_month', 'expiry_year', 'token_type', 'account_holder'}


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


def _rich_account_holder():
    billing_address = Address()
    billing_address.address_line1 = '123 High St.'
    billing_address.address_line2 = 'Flat 456'
    billing_address.city = 'London'
    billing_address.state = 'GB'
    billing_address.zip = 'SW1A 1AA'
    billing_address.country = Country.GB

    phone = Phone()
    phone.country_code = '+44'
    phone.number = '4155552671'

    identification = AccountHolderIdentification()
    identification.type = AccountHolderIdentificationType.PASSPORT
    identification.number = 'E12345678'
    identification.issuing_country = Country.GB
    identification.date_of_expiry = '2030-01-01'

    account_holder = AccountHolder()
    account_holder.type = AccountHolderType.INDIVIDUAL
    account_holder.first_name = 'John'
    account_holder.middle_name = 'Paul'
    account_holder.last_name = 'Smith'
    account_holder.billing_address = billing_address
    account_holder.phone = phone
    account_holder.identification = identification
    account_holder.email = 'john.smith@example.com'
    account_holder.date_of_birth = '1985-05-15'
    account_holder.country_of_birth = Country.GB
    return account_holder


def _network_token_destination(with_optionals=True):
    destination = PaymentRequestNetworkTokenDestination()
    destination.token = '4543474002249996'
    destination.expiry_month = 6
    destination.expiry_year = 2025
    destination.token_type = NetworkTokenType.VTS
    if with_optionals:
        destination.cryptogram = 'hv8mUFzPzRZoCAAAAAEQBDMAAAA='
        destination.eci = '05'
    destination.account_holder = _rich_account_holder()
    return destination


class TestCardPayoutDestinationSerialization:

    def test_network_token_destination_serializes_literal_wire_keys(self):
        serialized = _serialize(_network_token_destination())

        assert set(serialized.keys()) == REQUIRED_NETWORK_TOKEN_KEYS | {'cryptogram', 'eci'}
        assert serialized['type'] == 'network_token'
        assert all(key == key.lower() for key in serialized.keys())

    def test_network_token_destination_matches_spec_fixture(self):
        serialized = _serialize(_network_token_destination())

        assert serialized == NETWORK_TOKEN_FIXTURE
        assert isinstance(serialized['expiry_month'], int)
        assert isinstance(serialized['expiry_year'], int)

    def test_network_token_destination_omits_unset_optional_fields(self):
        serialized = _serialize(_network_token_destination(with_optionals=False))

        assert set(serialized.keys()) == REQUIRED_NETWORK_TOKEN_KEYS

    def test_network_token_type_enum_has_exactly_the_spec_values(self):
        assert {member.value for member in NetworkTokenType} == {'vts', 'mdes', 'applepay', 'googlepay'}
        for member in NetworkTokenType:
            destination = _network_token_destination()
            destination.token_type = member
            assert _serialize(destination)['token_type'] == member.value

    def test_destination_type_enum_has_network_token(self):
        assert PaymentDestinationType.NETWORK_TOKEN.value == 'network_token'
        assert PaymentDestinationType('network_token') is PaymentDestinationType.NETWORK_TOKEN

    def test_payout_request_serializes_network_token_destination(self):
        request = PayoutRequest()
        request.destination = _network_token_destination()

        serialized = _serialize(request)

        assert serialized == {'destination': NETWORK_TOKEN_FIXTURE}
        assert set(serialized['destination']['account_holder'].keys()) == {
            'type', 'first_name', 'middle_name', 'last_name', 'billing_address', 'phone',
            'identification', 'email', 'date_of_birth', 'country_of_birth'}

    def test_network_token_destination_round_trip(self):
        destination = _network_token_destination()

        decoded = json.loads(json.dumps(destination, cls=JsonSerializer))

        assert decoded['type'] == destination.type.value
        assert decoded['token'] == destination.token
        assert decoded['expiry_month'] == destination.expiry_month
        assert decoded['expiry_year'] == destination.expiry_year
        assert decoded['token_type'] == destination.token_type.value
        assert decoded['cryptogram'] == destination.cryptogram
        assert decoded['eci'] == destination.eci
        holder = destination.account_holder
        decoded_holder = decoded['account_holder']
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

    def test_card_destination_serializes_every_property(self):
        destination = PaymentRequestCardDestination()
        destination.number = '4242424242424242'
        destination.expiry_month = 6
        destination.expiry_year = 2025
        destination.account_holder = _rich_account_holder()

        assert _serialize(destination) == {
            'type': 'card',
            'number': '4242424242424242',
            'expiry_month': 6,
            'expiry_year': 2025,
            'account_holder': NETWORK_TOKEN_FIXTURE['account_holder'],
        }

    def test_token_destination_serializes_every_property(self):
        account_holder = AccountHolder()
        account_holder.type = AccountHolderType.INDIVIDUAL
        account_holder.first_name = 'John'
        account_holder.middle_name = 'Paul'
        account_holder.last_name = 'Smith'
        destination = PaymentRequestTokenDestination()
        destination.token = 'tok_ubfj2q76miwundwlk72vxt2i7q'
        destination.account_holder = account_holder

        assert _serialize(destination) == {
            'type': 'token',
            'token': 'tok_ubfj2q76miwundwlk72vxt2i7q',
            'account_holder': {'type': 'individual', 'first_name': 'John', 'middle_name': 'Paul',
                               'last_name': 'Smith'},
        }

    def test_raw_string_token_type_serializes_like_the_enum(self):
        with_enum = _network_token_destination()
        with_string = _network_token_destination()
        with_string.token_type = 'vts'

        assert _serialize(with_string) == _serialize(with_enum)
