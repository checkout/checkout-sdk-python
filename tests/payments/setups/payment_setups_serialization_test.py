import json

from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.common.common import Phone
from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.setups.setups import (
    PaymentMethods, PaymentSetupInstrument, PayNow, AlipayCn, TerminalType, OsType,
    Qpay, Ideal, Knet, KnetLanguage, Bancontact, Multibanco, P24, P24AccountHolder,
    Swish, SwishAccountHolder, Ach, AchAccountType, AchAccountHolder,
    AchAccountHolderIdentification, Sepa, SepaAccountHolder, SepaMandate, SepaMandateType,
    GooglePay, GooglePayTokenData, ApplePay, ApplePayTokenData, ApplePayTokenDataHeader,
    Card, PaymentSetupAccountHolder, PaymentSetupAccountHolderType,
    KlarnaAccountHolder, Bacs, BacsAccountHolder, BacsAccountHolderType, CardPresent,
    CardPresentPin, PayByBank, PayByBankAction, PayByBankBank, Stablecoin,
    PaymentSetupBillingDescriptor, PaymentSetupPresentmentDetails, PaymentSetupTerminal,
    PaymentSetupAmountAllocation, AmountAllocationCommission, Order,
)


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class TestPaymentSetupsSerialization:

    def test_status_flags_only_method_serializes_without_spurious_fields(self):
        # A method that is not configured must not emit status/flags/initialization.
        assert _serialize(PayNow()) == {}

    def test_terminal_wallet_serializes_terminal_and_os_type(self):
        alipay = AlipayCn()
        alipay.terminal_type = TerminalType.WEB
        alipay.os_type = OsType.ANDROID

        assert _serialize(alipay) == {'terminal_type': 'web', 'os_type': 'android'}

    def test_qpay_serializes_specific_fields(self):
        qpay = Qpay()
        qpay.national_id = '21234567890'
        qpay.description = 'Order 123'

        assert _serialize(qpay) == {'national_id': '21234567890', 'description': 'Order 123'}

    def test_ideal_serializes_description(self):
        ideal = Ideal()
        ideal.description = '2 t-shirts'

        assert _serialize(ideal) == {'description': '2 t-shirts'}

    def test_knet_serializes_language_enum(self):
        knet = Knet()
        knet.language = KnetLanguage.AR

        assert _serialize(knet) == {'language': 'ar'}

    def test_bancontact_and_multibanco_serialize_account_holder_name(self):
        bancontact = Bancontact()
        bancontact.account_holder_name = 'John Smith'
        multibanco = Multibanco()
        multibanco.account_holder_name = 'Jane Doe'

        assert _serialize(bancontact) == {'account_holder_name': 'John Smith'}
        assert _serialize(multibanco) == {'account_holder_name': 'Jane Doe'}

    def test_p24_serializes_nested_account_holder(self):
        p24 = P24()
        holder = P24AccountHolder()
        holder.name = 'John Smith'
        holder.email = 'john@example.com'
        p24.account_holder = holder

        assert _serialize(p24) == {
            'account_holder': {'name': 'John Smith', 'email': 'john@example.com'}
        }

    def test_swish_serializes_billing_descriptor_and_account_holder(self):
        swish = Swish()
        swish.billing_descriptor = 'ACME'
        holder = SwishAccountHolder()
        holder.first_name = 'John'
        holder.last_name = 'Smith'
        swish.account_holder = holder

        assert _serialize(swish) == {
            'billing_descriptor': 'ACME',
            'account_holder': {'first_name': 'John', 'last_name': 'Smith'},
        }

    def test_ach_serializes_nested_structure(self):
        ach = Ach()
        ach.account_type = AchAccountType.CURRENT
        ach.account_number = '12345678'
        ach.bank_code = '01234567'
        ach.country = 'US'

        holder = AchAccountHolder()
        holder.type = PaymentSetupAccountHolderType.INDIVIDUAL
        holder.first_name = 'John'
        holder.last_name = 'Smith'
        identification = AchAccountHolderIdentification()
        identification.type = 'ssn'
        identification.issuing_country = 'US'
        identification.number = '123456789'
        holder.identification = identification
        ach.account_holder = holder

        assert _serialize(ach) == {
            'account_type': 'current',
            'account_number': '12345678',
            'bank_code': '01234567',
            'country': 'US',
            'account_holder': {
                'type': 'individual',
                'first_name': 'John',
                'last_name': 'Smith',
                'identification': {
                    'type': 'ssn',
                    'issuing_country': 'US',
                    'number': '123456789',
                },
            },
        }

    def test_sepa_serializes_account_holder_and_mandate(self):
        sepa = Sepa()
        sepa.account_number = 'DE89370400440532013000'
        sepa.country = 'DE'
        sepa.currency = Currency.EUR

        holder = SepaAccountHolder()
        holder.type = PaymentSetupAccountHolderType.CORPORATE
        holder.company_name = 'ACME Ltd'
        sepa.account_holder = holder

        mandate = SepaMandate()
        mandate.id = 'man_123'
        mandate.type = SepaMandateType.CORE
        sepa.mandate = mandate

        assert _serialize(sepa) == {
            'account_number': 'DE89370400440532013000',
            'country': 'DE',
            'currency': 'EUR',
            'account_holder': {'type': 'corporate', 'company_name': 'ACME Ltd'},
            'mandate': {'id': 'man_123', 'type': 'core'},
        }

    def test_googlepay_serializes_token_data(self):
        googlepay = GooglePay()
        googlepay.token = 'tok_x'
        token_data = GooglePayTokenData()
        token_data.protocol_version = 'ECv2'
        token_data.signature = 'sig'
        token_data.signed_message = 'msg'
        token_data.tokenization_key = 'pk_x'
        googlepay.token_data = token_data

        assert _serialize(googlepay) == {
            'token': 'tok_x',
            'token_data': {
                'protocol_version': 'ECv2',
                'signature': 'sig',
                'signed_message': 'msg',
                'tokenization_key': 'pk_x',
            },
        }

    def test_applepay_serializes_token_data_with_header(self):
        applepay = ApplePay()
        token_data = ApplePayTokenData()
        token_data.version = 'EC_v1'
        token_data.data = 'encrypted'
        token_data.signature = 'sig'
        header = ApplePayTokenDataHeader()
        header.ephemeral_public_key = 'key'
        header.public_key_hash = 'hash'
        header.transaction_id = 'txn'
        token_data.header = header
        applepay.token_data = token_data

        assert _serialize(applepay) == {
            'token_data': {
                'version': 'EC_v1',
                'data': 'encrypted',
                'signature': 'sig',
                'header': {
                    'ephemeral_public_key': 'key',
                    'public_key_hash': 'hash',
                    'transaction_id': 'txn',
                },
            }
        }

    def test_card_serializes_writable_fields_and_account_holder(self):
        card = Card()
        card.number = '4242424242424242'
        card.expiry_month = 12
        card.expiry_year = 2030
        card.name = 'John Smith'
        card.cvv = '100'

        holder = PaymentSetupAccountHolder()
        holder.type = PaymentSetupAccountHolderType.INDIVIDUAL
        holder.first_name = 'John'
        holder.last_name = 'Smith'
        card.account_holder = holder

        assert _serialize(card) == {
            'number': '4242424242424242',
            'expiry_month': 12,
            'expiry_year': 2030,
            'name': 'John Smith',
            'cvv': '100',
            'account_holder': {'type': 'individual', 'first_name': 'John', 'last_name': 'Smith'},
        }

    def test_instrument_serializes_id_and_phone(self):
        instrument = PaymentSetupInstrument()
        instrument.id = 'src_wmlfc3zttb4uzmk6snpwb43jbi'
        instrument.allow_update = True
        phone = Phone()
        phone.country_code = '+44'
        phone.number = '207 946 0000'
        instrument.phone = phone

        assert _serialize(instrument) == {
            'id': 'src_wmlfc3zttb4uzmk6snpwb43jbi',
            'allow_update': True,
            'phone': {'country_code': '+44', 'number': '207 946 0000'},
        }

    def test_payment_methods_container_serializes_only_set_methods(self):
        payment_methods = PaymentMethods()
        ideal = Ideal()
        ideal.description = 'order'
        payment_methods.ideal = ideal

        assert _serialize(payment_methods) == {'ideal': {'description': 'order'}}

    # ── 2026-06-29 additions ─────────────────────────────────────────────────

    def test_klarna_account_holder_serializes_name(self):
        holder = KlarnaAccountHolder()
        holder.name = 'John Smith'

        assert _serialize(holder) == {'name': 'John Smith'}

    def test_bacs_serializes_nested_account_holder(self):
        bacs = Bacs()
        holder = BacsAccountHolder()
        holder.type = BacsAccountHolderType.INDIVIDUAL
        holder.first_name = 'John'
        holder.last_name = 'Smith'
        holder.email = 'john.smith@example.com'
        bacs.account_holder = holder
        bacs.account_number = '12345678'
        bacs.bank_code = '200000'
        bacs.country = 'GB'
        bacs.currency = Currency.GBP
        bacs.allow_partial_match = True

        assert _serialize(bacs) == {
            'initialization': 'disabled',
            'account_holder': {
                'type': 'individual', 'first_name': 'John', 'last_name': 'Smith',
                'email': 'john.smith@example.com',
            },
            'account_number': '12345678',
            'bank_code': '200000',
            'country': 'GB',
            'currency': 'GBP',
            'allow_partial_match': True,
        }

    def test_card_present_serializes_nested_pin(self):
        card_present = CardPresent()
        card_present.track2 = 'track2-data'
        card_present.emv = 'emv-data'
        card_present.entry_mode = 'contactless'
        pin = CardPresentPin()
        pin.key_set_id = 'ks_1'
        pin.block = 'block'
        pin.block_format = 'iso0'
        card_present.pin = pin
        card_present.store_for_future_use = True
        card_present.name = 'John Smith'

        assert _serialize(card_present) == {
            'track2': 'track2-data',
            'emv': 'emv-data',
            'entry_mode': 'contactless',
            'pin': {'key_set_id': 'ks_1', 'block': 'block', 'block_format': 'iso0'},
            'store_for_future_use': True,
            'name': 'John Smith',
        }

    def test_pay_by_bank_serializes_bank_id_and_action(self):
        pay_by_bank = PayByBank()
        pay_by_bank.bank_id = 'ob-natwest'
        action = PayByBankAction()
        action.type = 'select_bank'
        bank = PayByBankBank()
        bank.bank_id = 'ob-natwest'
        bank.display_name = 'NatWest'
        bank.available = True
        action.banks = [bank]
        pay_by_bank.action = action

        assert _serialize(pay_by_bank) == {
            'bank_id': 'ob-natwest',
            'action': {
                'type': 'select_bank',
                'banks': [{'bank_id': 'ob-natwest', 'display_name': 'NatWest', 'available': True}],
            },
        }

    def test_stablecoin_serializes_status_and_flags(self):
        stablecoin = Stablecoin()
        stablecoin.status = 'available'
        stablecoin.flags = ['flag_a']

        assert _serialize(stablecoin) == {'status': 'available', 'flags': ['flag_a']}

    def test_billing_descriptor_presentment_terminal_serialize(self):
        billing_descriptor = PaymentSetupBillingDescriptor()
        billing_descriptor.name = 'ACME'
        billing_descriptor.city = 'London'
        billing_descriptor.reference = 'REF-1'

        presentment = PaymentSetupPresentmentDetails()
        presentment.amount = 1000
        presentment.currency = 'GBP'

        terminal = PaymentSetupTerminal()
        terminal.id = 'term_1'
        terminal.local_date_time = '2026-06-01T10:00:00'

        assert _serialize(billing_descriptor) == {'name': 'ACME', 'city': 'London', 'reference': 'REF-1'}
        assert _serialize(presentment) == {'amount': 1000, 'currency': 'GBP'}
        assert _serialize(terminal) == {'id': 'term_1', 'local_date_time': '2026-06-01T10:00:00'}

    def test_order_serializes_amount_allocations(self):
        allocation = PaymentSetupAmountAllocation()
        allocation.id = 'ent_w4jelhppmfiufdnatam37wrfc4'
        allocation.amount = 1000
        allocation.reference = 'ORD-5023-4E89'
        commission = AmountAllocationCommission()
        commission.amount = 100
        commission.percentage = 2.5
        allocation.commission = commission

        order = Order()
        order.amount_allocations = [allocation]

        assert _serialize(order) == {
            'amount_allocations': [{
                'id': 'ent_w4jelhppmfiufdnatam37wrfc4',
                'amount': 1000,
                'reference': 'ORD-5023-4E89',
                'commission': {'amount': 100, 'percentage': 2.5},
            }]
        }
