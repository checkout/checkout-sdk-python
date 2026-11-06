from enum import Enum

import pytest
import requests
from requests.adapters import BaseAdapter

from checkout_sdk.api_client import ApiClient
from checkout_sdk.accounts.accounts_client import AccountsClient
from checkout_sdk.apm.klarna_client import KlarnaClient
from checkout_sdk.apm.sepa_client import SepaClient
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.common.enums import Country, Currency
from checkout_sdk.customers.customers_client import CustomersClient
from checkout_sdk.disputes.disputes_client import DisputesClient
from checkout_sdk.environment import Environment
from checkout_sdk.events.events_client import EventsClient
from checkout_sdk.exception import CheckoutArgumentException
from checkout_sdk.instruments.instruments_client import InstrumentsClient
from checkout_sdk.issuing.issuing_client import IssuingClient
from checkout_sdk.payments.payments_client import PaymentsClient
from checkout_sdk.payments.sessions.sessions_client import PaymentSessionsClient
from checkout_sdk.payments.setups.setups_client import PaymentSetupsClient
from checkout_sdk.workflows.workflows_client import WorkflowsClient

BASE_URI = 'https://api.example.test/'


class _Authorization:

    @staticmethod
    def get_authorization_header():
        return 'Bearer test'


class _Credentials:

    @staticmethod
    def get_authorization(_authorization_type):
        return _Authorization()


class _RecordingAdapter(BaseAdapter):
    """Transport adapter that records the prepared request instead of sending it."""

    def __init__(self):
        super().__init__()
        self.requests = []

    def send(self, request, **kwargs):
        self.requests.append(request)
        response = requests.Response()
        response.status_code = 200
        response.headers['Content-Type'] = 'application/json'
        response._content = b''
        response.request = request
        return response

    def close(self):
        pass


@pytest.fixture
def wire():
    """Real ApiClient over a real requests.Session; returns (configuration, api_client, adapter)."""
    adapter = _RecordingAdapter()
    session = requests.Session()
    session.mount('https://', adapter)
    configuration = CheckoutConfiguration(_Credentials(), Environment.sandbox(), session)
    return configuration, ApiClient(configuration, BASE_URI), adapter


def _sent_path(adapter):
    assert len(adapter.requests) == 1, f'expected one request, got {len(adapter.requests)}'
    return adapter.requests[0].path_url


class _Plain(str, Enum):
    VALUE = 'GB'


class _ZeroLength(str):
    """str subclass that reports itself as empty and never equal to anything."""

    def __len__(self):
        return 0

    def __bool__(self):
        return False

    def __eq__(self, other):
        return False

    def __hash__(self):
        return 0

    def __str__(self):
        return 'ok'


class TestBuildPath:

    @pytest.mark.parametrize('segments, expected', [
        (('payments', 'pay_abc123'), 'payments/pay_abc123'),
        (('payments', 'pay_abc123', 'voids'), 'payments/pay_abc123/voids'),
        (('payments', 'pay-by.bank_~1'), 'payments/pay-by.bank_~1'),
        (('payments',), 'payments'),
        (('validation', 'bank-accounts', Country.GB, Currency.GBP), 'validation/bank-accounts/GB/GBP'),
        (('x', _Plain.VALUE), 'x/GB'),
    ])
    def test_should_keep_valid_segments_unchanged(self, segments, expected):
        assert Client.build_path(*segments) == expected

    @pytest.mark.parametrize('value, expected', [
        ('a?b', 'a%3Fb'),
        ('a#b', 'a%23b'),
        ('a?limit=1&b=2', 'a%3Flimit%3D1%26b%3D2'),
        ('a b', 'a%20b'),
        ('a%2Fb', 'a%252Fb'),
        ('%2e%2e', '%252e%252e'),
        ('a;b', 'a%3Bb'),
        ('a:b@c', 'a%3Ab%40c'),
        ('...', '...'),
        ('café', 'caf%C3%A9'),
        ('a\u0085b', 'a%C2%85b'),
        ('a．．', 'a%EF%BC%8E%EF%BC%8E'),
    ])
    def test_should_encode_each_value_as_one_segment(self, value, expected):
        assert Client.build_path('payments', value) == 'payments/' + expected

    @pytest.mark.parametrize('value', [
        None, '', '.', '..',
        '../x', '..\\x', 'a/b', 'a\\b', '/', 'x/..',
        'a\x00b', 'a\rb', 'a\nb', 'a\tb', 'a\x7fb',
        'a\ud800b',
        123, 1.5, True, b'pay_x', object(),
    ])
    def test_should_reject_invalid_segments(self, value):
        with pytest.raises(CheckoutArgumentException):
            Client.build_path('payments', value)

    @pytest.mark.parametrize('content, expected', [
        ('pay?x=1#frag', 'payments/pay%3Fx%3D1%23frag'),
        ('ok', 'payments/ok'),
    ])
    def test_should_encode_str_subclass_by_its_content(self, content, expected):
        assert Client.build_path('payments', _ZeroLength(content)) == expected
        assert type(Client.build_path('payments', _ZeroLength(content))) is str

    @pytest.mark.parametrize('content', ['..', '.', ''])
    def test_should_reject_str_subclass_dot_segments(self, content):
        with pytest.raises(CheckoutArgumentException):
            Client.build_path('payments', _ZeroLength(content))

    def test_should_encode_enum_with_str_subclass_value_by_its_content(self):
        member = Enum('Member', {'VALUE': _ZeroLength('a?b')}).VALUE
        assert Client.build_path('x', member) == 'x/a%3Fb'

    def test_should_reject_object_reporting_str_class(self):
        class _Disguised:
            @property
            def __class__(self):
                return str

        with pytest.raises(CheckoutArgumentException):
            Client.build_path('payments', _Disguised())

    def test_should_not_echo_rejected_value_in_message(self):
        with pytest.raises(CheckoutArgumentException) as error:
            Client.build_path('payments', 'sample_value/x')
        assert 'sample_value' not in str(error.value)


class TestRequestPathOnTheWire:

    def test_should_reject_separator_in_void_id_before_sending(self, wire):
        configuration, api_client, adapter = wire
        client = PaymentsClient(api_client, configuration)
        with pytest.raises(CheckoutArgumentException):
            client.void_payment('pay_x/y#')
        assert adapter.requests == []

    def test_should_reject_dot_segments_in_id_before_sending(self, wire):
        configuration, api_client, adapter = wire
        client = PaymentsClient(api_client, configuration)
        with pytest.raises(CheckoutArgumentException):
            client.get_payment_details('../x/y')
        assert adapter.requests == []

    def test_should_keep_query_characters_inside_the_id_segment(self, wire):
        configuration, api_client, adapter = wire
        client = PaymentsClient(api_client, configuration)
        client.get_payment_details('pay_x?limit=1')
        assert _sent_path(adapter) == '/payments/pay_x%3Flimit%3D1'

    def test_should_keep_fragment_characters_inside_the_id_segment(self, wire):
        configuration, api_client, adapter = wire
        client = PaymentsClient(api_client, configuration)
        client.void_payment('pay_x#')
        assert _sent_path(adapter) == '/payments/pay_x%23/voids'

    def test_should_not_decode_percent_encoded_input(self, wire):
        configuration, api_client, adapter = wire
        client = PaymentsClient(api_client, configuration)
        client.get_payment_details('%2E%2E%2Fx')
        assert _sent_path(adapter) == '/payments/%252E%252E%252Fx'

    def test_should_send_valid_id_unchanged(self, wire):
        configuration, api_client, adapter = wire
        client = PaymentsClient(api_client, configuration)
        client.void_payment('pay_abc123')
        assert _sent_path(adapter) == '/payments/pay_abc123/voids'

    def test_should_encode_payment_session_id(self, wire):
        configuration, api_client, adapter = wire
        client = PaymentSessionsClient(api_client, configuration)
        client.submit_payment_session('ps_x?a#b', None)
        assert _sent_path(adapter) == '/payment-sessions/ps_x%3Fa%23b/submit'

    def test_should_reject_payment_session_id_with_separator(self, wire):
        configuration, api_client, adapter = wire
        client = PaymentSessionsClient(api_client, configuration)
        with pytest.raises(CheckoutArgumentException):
            client.submit_payment_session('../x', None)
        assert adapter.requests == []

    def test_should_send_event_types_version_as_query_parameter(self, wire):
        configuration, api_client, adapter = wire
        client = EventsClient(api_client, configuration)
        client.retrieve_all_event_types('1.0&x=y#z')
        assert _sent_path(adapter) == '/event-types?version=1.0%26x%3Dy%23z'

    def test_should_send_event_types_without_version(self, wire):
        configuration, api_client, adapter = wire
        client = EventsClient(api_client, configuration)
        client.retrieve_all_event_types()
        assert _sent_path(adapter) == '/event-types'


def _accounts(api_client, configuration):
    return AccountsClient(api_client=api_client, files_client=api_client, configuration=configuration)


# (client factory, method name, extra positional args, expected path with '{}' for the encoded id)
_SAMPLE = [
    (PaymentsClient, 'get_payment_details', (), '/payments/{}'),
    (PaymentsClient, 'void_payment', (), '/payments/{}/voids'),
    (CustomersClient, 'get', (), '/customers/{}'),
    (DisputesClient, 'get_dispute_details', (), '/disputes/{}'),
    (InstrumentsClient, 'get', (), '/instruments/{}'),
    (WorkflowsClient, 'get_workflow', (), '/workflows/{}'),
    (IssuingClient, 'get_card_details', (), '/issuing/cards/{}'),
    (EventsClient, 'retrieve_event', (), '/events/{}'),
    (SepaClient, 'get_mandate', (), '/sepa/mandates/{}'),
    (PaymentSetupsClient, 'get_payment_setup', (), '/payments/setups/{}'),
    (PaymentSetupsClient, 'confirm_payment_setup', ('klarna',), '/payments/setups/{}/confirm/klarna'),
    (KlarnaClient, 'get_credit_session', (), '/klarna-external/credit-sessions/{}'),
    (_accounts, 'retrieve_entity_file', ('file_x',), '/entities/{}/files/file_x'),
]


class TestSampleOfClients:

    @pytest.mark.parametrize('factory, method, extra, expected', _SAMPLE)
    def test_should_send_valid_id_unchanged(self, wire, factory, method, extra, expected):
        configuration, api_client, adapter = wire
        getattr(factory(api_client, configuration), method)('id_abc-123', *extra)
        assert _sent_path(adapter) == expected.format('id_abc-123')

    @pytest.mark.parametrize('factory, method, extra, expected', _SAMPLE)
    def test_should_encode_id_as_one_segment(self, wire, factory, method, extra, expected):
        configuration, api_client, adapter = wire
        getattr(factory(api_client, configuration), method)('a?b#c d', *extra)
        assert _sent_path(adapter) == expected.format('a%3Fb%23c%20d')

    @pytest.mark.parametrize('value', ['../x', 'a/b', '..', '', None])
    @pytest.mark.parametrize('factory, method, extra, expected', _SAMPLE)
    def test_should_reject_invalid_id_before_sending(self, wire, factory, method, extra, expected, value):
        configuration, api_client, adapter = wire
        with pytest.raises(CheckoutArgumentException):
            getattr(factory(api_client, configuration), method)(value, *extra)
        assert adapter.requests == []

    def test_should_encode_second_caller_value(self, wire):
        configuration, api_client, adapter = wire
        PaymentSetupsClient(api_client, configuration).confirm_payment_setup('ps_x', 'a?b')
        assert _sent_path(adapter) == '/payments/setups/ps_x/confirm/a%3Fb'

    def test_should_reject_second_caller_value_with_separator(self, wire):
        configuration, api_client, adapter = wire
        with pytest.raises(CheckoutArgumentException):
            PaymentSetupsClient(api_client, configuration).confirm_payment_setup('ps_x', '../../x/y')
        assert adapter.requests == []
