import json

from checkout_sdk.common.enums import (
    AccountHolderType, AchInstrumentAccountType, BacsPaymentType, Country, Currency, InstrumentAccountHolderType,
    InstrumentType, PaymentSourceType, SepaMandateType, SepaPaymentType,
)
from checkout_sdk.instruments.instruments import (
    AchAccountHolder, AchInstrumentData, BacsBillingAddress, BacsInstrumentAccount, BacsInstrumentData,
    CreateAchInstrumentRequest, CreateBacsAccountHolder, CreateBacsInstrumentRequest,
    CreateSepaInstrumentRequest, PaymentNetwork, SepaAccountHolder, SepaBillingAddress,
    SepaInstrumentData, UpdateAchInstrumentRequest, UpdateBacsAccountHolder,
    UpdateBacsInstrumentRequest, UpdateSepaInstrumentRequest,
)
from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.payments.payment_apm import RequestBacsSource
from checkout_sdk.payments.payments import PaymentType


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class TestBacsInstrumentSerialization:
    """Schema validation tests against StoreBacsInstrumentRequest and UpdateBacsInstrumentRequest."""

    def test_store_request_serializes_every_property(self):
        address = BacsBillingAddress()
        address.address_line1 = 'Cloverfield St.'
        address.address_line2 = '23A'
        address.city = 'London'
        address.zip = 'SW1A 1AA'
        address.country = Country.GB

        holder = CreateBacsAccountHolder()
        holder.first_name = 'John'
        holder.last_name = 'Smith'
        holder.billing_address = address

        account = BacsInstrumentAccount()
        account.processing_channel_id = 'pc_q4dbxom5jbgudnjzjpz7j2z6uq'

        data = BacsInstrumentData()
        data.account_number = '86753246'
        data.bank_code = '040004'
        data.country = Country.GB
        data.currency = Currency.GBP
        data.payment_type = BacsPaymentType.RECURRING
        data.allow_partial_match = False

        request = CreateBacsInstrumentRequest()
        request.account = account
        request.instrument_data = data
        request.account_holder = holder

        assert _serialize(request) == {
            'type': 'bacs',
            'account': {'processing_channel_id': 'pc_q4dbxom5jbgudnjzjpz7j2z6uq'},
            'instrument_data': {
                'account_number': '86753246',
                'bank_code': '040004',
                'country': 'GB',
                'currency': 'GBP',
                'payment_type': 'Recurring',
                'allow_partial_match': False,
            },
            'account_holder': {
                'first_name': 'John',
                'last_name': 'Smith',
                'billing_address': {
                    'address_line1': 'Cloverfield St.',
                    'address_line2': '23A',
                    'city': 'London',
                    'zip': 'SW1A 1AA',
                    'country': 'GB',
                },
            },
        }

    def test_update_request_serializes_the_five_property_account_holder(self):
        holder = UpdateBacsAccountHolder()
        holder.first_name = 'John'
        holder.last_name = 'Smith'
        holder.company_name = 'Wayne Enterprises'
        holder.type = InstrumentAccountHolderType.CORPORATE

        data = BacsInstrumentData()
        data.payment_type = BacsPaymentType.REGULAR
        data.allow_partial_match = True

        request = UpdateBacsInstrumentRequest()
        request.instrument_data = data
        request.account_holder = holder

        serialized = _serialize(request)

        assert serialized['type'] == 'bacs'
        assert serialized['instrument_data']['payment_type'] == 'Regular'
        assert serialized['instrument_data']['allow_partial_match'] is True
        assert serialized['account_holder']['company_name'] == 'Wayne Enterprises'
        assert serialized['account_holder']['type'] == 'corporate'

    def test_store_account_holder_declares_no_company_name_or_type(self):
        # StoreBacsInstrumentRequest.account_holder declares first_name, last_name and
        # billing_address only; company_name and type appear on update.
        assert set(CreateBacsAccountHolder.__annotations__) == {
            'first_name', 'last_name', 'billing_address'}
        assert set(UpdateBacsAccountHolder.__annotations__) == {
            'first_name', 'last_name', 'company_name', 'billing_address', 'type'}


class TestSepaInstrumentSerialization:
    """Schema validation tests against StoreSepaInstrumentRequest and UpdateSepaInstrumentRequest."""

    def test_store_request_serializes_every_property(self):
        address = SepaBillingAddress()
        address.address_line1 = 'Evergreen Terrace'
        address.address_line2 = '742'
        address.city = 'Paris'
        address.zip = '75000'
        address.country = Country.FR

        holder = SepaAccountHolder()
        holder.first_name = 'John'
        holder.last_name = 'Wick'
        holder.company_name = 'Checkout.com'
        holder.billing_address = address
        holder.type = InstrumentAccountHolderType.INDIVIDUAL

        data = SepaInstrumentData()
        data.type = SepaMandateType.B2B
        data.account_number = 'FR2810096000509685512959O86'
        data.country = Country.FR
        data.currency = Currency.EUR
        data.payment_type = SepaPaymentType.RECURRING
        data.mandate_id = '1234567890'

        request = CreateSepaInstrumentRequest()
        request.instrument_data = data
        request.account_holder = holder

        serialized = _serialize(request)

        assert serialized['type'] == 'sepa'
        assert serialized['instrument_data']['type'] == 'B2B'
        assert serialized['instrument_data']['account_number'] == 'FR2810096000509685512959O86'
        assert serialized['instrument_data']['payment_type'] == 'recurring'
        assert serialized['instrument_data']['mandate_id'] == '1234567890'
        assert serialized['account_holder']['company_name'] == 'Checkout.com'
        assert serialized['account_holder']['type'] == 'individual'
        assert serialized['account_holder']['billing_address']['city'] == 'Paris'

    def test_update_request_carries_the_sepa_type(self):
        request = UpdateSepaInstrumentRequest()
        request.instrument_data = SepaInstrumentData()
        request.instrument_data.payment_type = SepaPaymentType.REGULAR

        serialized = _serialize(request)

        assert serialized['type'] == 'sepa'
        assert serialized['instrument_data']['payment_type'] == 'regular'

    def test_sepa_stays_lowercase_and_bacs_stays_capitalised(self):
        # The specification declares the SEPA payment_type lowercase and the Bacs Direct Debit
        # payment_type capitalised. This is the regression test that stops the two being unified.
        assert [e.value for e in SepaPaymentType] == ['recurring', 'regular']
        assert [e.value for e in BacsPaymentType] == ['Recurring', 'Regular']
        # payments.PaymentType serializes capitalised values and carries values neither instrument
        # schema allows, so it must not be used for either field.
        assert PaymentType.RECURRING.value != SepaPaymentType.RECURRING.value

    def test_sepa_account_holder_is_not_the_shared_superset(self):
        assert set(SepaAccountHolder.__annotations__) == {
            'first_name', 'last_name', 'company_name', 'billing_address', 'type'}

    def test_the_merged_instrument_data_class_is_gone(self):
        import checkout_sdk.instruments.instruments as module
        assert not hasattr(module, 'InstrumentData')


class TestAchInstrumentSerialization:
    """Schema validation tests against StoreAchInstrumentRequest and UpdateAchInstrumentRequest."""

    def test_store_request_serializes_every_property(self):
        data = AchInstrumentData()
        data.account_type = AchInstrumentAccountType.CHECKING
        data.account_number = '4099999992'
        data.bank_code = '211370545'
        data.currency = Currency.USD
        data.country = Country.US

        holder = AchAccountHolder()
        holder.first_name = 'John'
        holder.last_name = 'Smith'
        holder.company_name = 'Smith Enterprises'
        holder.type = InstrumentAccountHolderType.CORPORATE

        request = CreateAchInstrumentRequest()
        request.instrument_data = data
        request.account_holder = holder

        assert _serialize(request) == {
            'type': 'ach',
            'instrument_data': {
                'account_type': 'checking',
                'account_number': '4099999992',
                'bank_code': '211370545',
                'currency': 'USD',
                'country': 'US',
            },
            'account_holder': {
                'first_name': 'John',
                'last_name': 'Smith',
                'company_name': 'Smith Enterprises',
                'type': 'corporate',
            },
        }

    def test_update_request_carries_the_ach_type(self):
        request = UpdateAchInstrumentRequest()
        request.instrument_data = AchInstrumentData()
        request.instrument_data.account_type = AchInstrumentAccountType.SAVINGS

        serialized = _serialize(request)

        assert serialized['type'] == 'ach'
        assert serialized['instrument_data']['account_type'] == 'savings'

    def test_ach_account_holder_declares_no_billing_address(self):
        assert set(AchAccountHolder.__annotations__) == {
            'first_name', 'last_name', 'company_name', 'type'}

    def test_ach_account_type_is_not_the_bank_account_set(self):
        from checkout_sdk.common.enums import AccountType
        assert [e.value for e in AchInstrumentAccountType] == ['savings', 'checking']
        assert [e.value for e in AccountType] == ['savings', 'current', 'cash']


class TestInstrumentEnums:

    def test_instrument_type_carries_bacs_and_ach(self):
        assert InstrumentType.BACS.value == 'bacs'
        assert InstrumentType.ACH.value == 'ach'

    def test_payment_network_values_are_lowercase(self):
        # The payment-network query parameter declares these values lowercase.
        assert [e.value for e in PaymentNetwork] == [
            'local', 'sepa', 'fps', 'ach', 'fedwire', 'swift']

    def test_account_holder_type_carries_government(self):
        assert AccountHolderType.GOVERNMENT.value == 'government'

    def test_instrument_account_holder_type_excludes_government(self):
        assert [e.value for e in InstrumentAccountHolderType] == ['individual', 'corporate']


class TestBacsPaymentSource:
    """Schema validation tests against PaymentRequestBacsSource, which declares type and id only."""

    def test_serializes_the_type_and_the_instrument_id(self):
        source = RequestBacsSource()
        source.id = 'src_wmlfc3zyhqzehihu7giusaaawu'

        assert _serialize(source) == {
            'type': 'bacs',
            'id': 'src_wmlfc3zyhqzehihu7giusaaawu',
        }

    def test_payment_source_type_carries_bacs(self):
        assert PaymentSourceType.BACS.value == 'bacs'


class TestBankAccountInstrumentSerialization:
    """Schema validation tests for the bank-account instrument requests.

    StoreBankAccountInstrumentRequest and UpdateBankInstrumentRequest declare the bank details as
    `bank`. Both classes previously carried a `bank_details` attribute, which serialized under a key
    the API does not declare.
    """

    def test_store_request_serializes_the_bank_details_as_bank(self):
        from checkout_sdk.common.common import BankDetails
        from checkout_sdk.instruments.instruments import CreateBankAccountInstrumentRequest

        bank = BankDetails()
        bank.name = 'Lloyds TSB'
        bank.branch = 'Bournemouth'

        request = CreateBankAccountInstrumentRequest()
        request.currency = Currency.GBP
        request.country = Country.GB
        request.bank = bank

        serialized = _serialize(request)

        assert serialized['bank'] == {'name': 'Lloyds TSB', 'branch': 'Bournemouth'}
        assert 'bank_details' not in serialized
        assert 'bank_details' not in CreateBankAccountInstrumentRequest.__annotations__

    def test_update_request_serializes_the_bank_details_as_bank(self):
        from checkout_sdk.common.common import BankDetails
        from checkout_sdk.instruments.instruments import UpdateBankAccountInstrumentRequest

        bank = BankDetails()
        bank.name = 'Lloyds TSB'

        request = UpdateBankAccountInstrumentRequest()
        request.bank = bank

        serialized = _serialize(request)

        assert serialized['bank'] == {'name': 'Lloyds TSB'}
        assert 'bank_details' not in serialized
        assert 'bank_details' not in UpdateBankAccountInstrumentRequest.__annotations__


class TestDateFieldTypes:
    """The specification declares these fields `format: date`.

    The serializer renders anything with strftime through isoformat(), so a datetime emits a full ISO
    timestamp and a date raises TypeError. Only a yyyy-MM-dd string produces the declared format, so
    these attributes are annotated `str`.
    """

    def test_date_fields_are_annotated_as_strings(self):
        from checkout_sdk.apm.bacs import BacsNotificationRequest
        assert BacsNotificationRequest.__annotations__['collection_date'] is str
        assert SepaInstrumentData.__annotations__['date_of_signature'] is str

    def test_a_string_date_serializes_in_the_declared_format(self):
        data = SepaInstrumentData()
        data.date_of_signature = '2020-01-01'

        assert _serialize(data)['date_of_signature'] == '2020-01-01'

    def test_a_datetime_would_not_serialize_in_the_declared_format(self):
        # Documents why the annotation is str: this is what a datetime produces.
        from datetime import datetime
        data = SepaInstrumentData()
        data.date_of_signature = datetime(2020, 1, 1)

        assert _serialize(data)['date_of_signature'] == '2020-01-01T00:00:00'


class TestSepaPaymentSources:
    """RequestSepaV4Source matches PaymentRequestSEPAV4Source; RequestSepaSource is the legacy shape."""

    def test_the_v4_source_carries_the_mandate_type(self):
        from checkout_sdk.common.enums import SepaMandateType
        from checkout_sdk.payments.payment_apm import RequestSepaV4Source

        source = RequestSepaV4Source()
        source.mandate_type = SepaMandateType.B2B

        serialized = _serialize(source)

        assert serialized['type'] == 'sepa'
        assert serialized['mandate_type'] == 'B2B'

    def test_the_legacy_source_is_the_one_carrying_the_undeclared_bank_code(self):
        from checkout_sdk.payments.payment_apm import RequestSepaSource, RequestSepaV4Source

        assert 'bank_code' in RequestSepaSource.__annotations__
        assert 'mandate_type' not in RequestSepaSource.__annotations__
        assert 'bank_code' not in RequestSepaV4Source.__annotations__
        assert 'mandate_type' in RequestSepaV4Source.__annotations__


class TestAccountHolderTypeConstraint:
    """AccountHolderType serves three positions, all of which declare individual, corporate and
    government. INSTRUMENT is documented as possibly obsolete: the specification declares it only on
    the sender schemas, which PaymentSenderType models instead.
    """

    def test_the_three_declared_values_are_present(self):
        assert AccountHolderType.INDIVIDUAL.value == 'individual'
        assert AccountHolderType.CORPORATE.value == 'corporate'
        assert AccountHolderType.GOVERNMENT.value == 'government'

    def test_instrument_is_carried_but_not_declared_by_any_position_this_enum_serves(self):
        # Retained for backwards compatibility and documented as possibly obsolete. If this ever
        # becomes a real value for an account-holder field, remove the note on the member too.
        assert AccountHolderType.INSTRUMENT.value == 'instrument'

    def test_the_sender_enum_is_where_instrument_belongs(self):
        from checkout_sdk.payments.payments import PaymentSenderType
        assert PaymentSenderType.INSTRUMENT.value == 'instrument'
        assert {e.value for e in PaymentSenderType} == {
            'individual', 'corporate', 'instrument', 'government'}

    def test_nothing_in_the_sdk_passes_the_instrument_member(self):
        import pathlib
        root = pathlib.Path('checkout_sdk')
        hits = [
            str(f) for f in root.rglob('*.py')
            if 'AccountHolderType.INSTRUMENT' in f.read_text(encoding='utf-8')
            and f.name != 'enums.py'
        ]
        assert hits == []

    def test_the_query_parameter_documents_the_constraint(self):
        from checkout_sdk.instruments.instruments import BankAccountFieldQuery
        doc = BankAccountFieldQuery.__doc__ or ''
        assert 'individual, corporate and government' in doc
        assert 'INSTRUMENT' in doc
