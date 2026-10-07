import json

import pytest

from checkout_sdk.checkout_response import ResponseWrapper
from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.common.common import Phone
from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.setups.setups import (
    PaymentMethods, PaymentSetupInstrument, PayNow, AlipayCn, TerminalType, OsType,
    Qpay, Ideal, Knet, KnetLanguage, Bancontact, Multibanco, P24, P24AccountHolder,
    Swish, SwishAccountHolder, Ach, AchAccountType, AchAccountHolder,
    AchAccountHolderIdentification, Sepa, SepaAccountHolder, SepaMandate, SetupsSepaMandateType,
    GooglePay, GooglePayTokenData, ApplePay, ApplePayTokenData, ApplePayTokenDataHeader,
    Card, PaymentSetupAccountHolder, PaymentSetupAccountHolderType,
    KlarnaAccountHolder, Bacs, BacsAccountHolder, BacsAccountHolderType, CardPresent,
    CardPresentPin, PayByBank, PayByBankAction, PayByBankActionType, PayByBankBank, Stablecoin,
    PaymentSetupBillingDescriptor, PaymentSetupPresentmentDetails, PaymentSetupTerminal,
    PaymentSetupAmountAllocation, AmountAllocationCommission, Order,
    Industry, PaymentSetupAccommodation, PaymentSetupAccommodationAddress,
    PaymentSetupAccommodationGuest, PaymentSetupAccommodationRoom, PaymentSetupAccommodationHost,
    PaymentSetupAirline, PaymentSetupAirlineTicket, PaymentSetupAirlinePassenger,
    PaymentSetupAirlinePassengerAddress, PaymentSetupFlightLegDetails,
    PaymentSetupAirlineInsurance, PaymentSetupAirlineInsurancePrice,
    MerchantAccount, OrderSubMerchant,
    PaymentSetupsRequest, Customer, CustomerEmail, CustomerDevice, CustomerDeviceClient,
    PaymentMethodInitialization, CashApp, CashAppAction, CashAppActionType, CashAppAddress,
    CashAppCustomerProfile,
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
        mandate.type = SetupsSepaMandateType.CORE
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
        action.type = PayByBankActionType.SELECT_BANK
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
        order.tipping_amount = 200
        order.surcharge_amount = 50
        order.amount_allocations = [allocation]

        assert _serialize(order) == {
            'tipping_amount': 200,
            'surcharge_amount': 50,
            'amount_allocations': [{
                'id': 'ent_w4jelhppmfiufdnatam37wrfc4',
                'amount': 1000,
                'reference': 'ORD-5023-4E89',
                'commission': {'amount': 100, 'percentage': 2.5},
            }]
        }

    def test_industry_accommodation_serializes_all_fields(self):
        address = PaymentSetupAccommodationAddress()
        address.address_line1 = '123 High Street'
        address.city = 'London'
        address.state = 'Greater London'
        address.country = 'GB'
        address.zip = 'NE1 1CK'

        guest = PaymentSetupAccommodationGuest()
        guest.first_name = 'John'
        guest.last_name = 'Smith'
        guest.date_of_birth = '1970-03-19'

        room = PaymentSetupAccommodationRoom()
        room.rate = 42.3
        room.number_of_nights = 5
        room.type = 'deluxe'

        host = PaymentSetupAccommodationHost()
        host.registration_date = '2020-01-01'
        host.total_reservation_count = 150

        accommodation = PaymentSetupAccommodation()
        accommodation.name = 'Checkout Lodge'
        accommodation.booking_reference = 'REF9083748'
        accommodation.check_in_date = '2025-04-11'
        accommodation.check_out_date = '2025-04-18'
        accommodation.address = address
        accommodation.number_of_rooms = 2
        accommodation.guests = [guest]
        accommodation.room = [room]
        accommodation.total_number_of_guests = 2
        accommodation.refundable = True
        accommodation.delivery_recipient = 'jane.smith@example.com'
        accommodation.host = host

        industry = Industry()
        industry.accommodation = [accommodation]

        assert _serialize(industry) == {
            'accommodation': [{
                'name': 'Checkout Lodge',
                'booking_reference': 'REF9083748',
                'check_in_date': '2025-04-11',
                'check_out_date': '2025-04-18',
                'address': {
                    'address_line1': '123 High Street',
                    'city': 'London',
                    'state': 'Greater London',
                    'country': 'GB',
                    'zip': 'NE1 1CK',
                },
                'number_of_rooms': 2,
                'guests': [{'first_name': 'John', 'last_name': 'Smith', 'date_of_birth': '1970-03-19'}],
                'room': [{'rate': 42.3, 'number_of_nights': 5, 'type': 'deluxe'}],
                'total_number_of_guests': 2,
                'refundable': True,
                'delivery_recipient': 'jane.smith@example.com',
                'host': {'registration_date': '2020-01-01', 'total_reservation_count': 150},
            }]
        }

    def test_industry_airline_serializes_all_fields(self):
        ticket = PaymentSetupAirlineTicket()
        ticket.number = '0742464639523'
        ticket.issue_date = '2025-05-01'
        ticket.issuing_carrier_code = '042'
        ticket.travel_package_indicator = 'A'
        ticket.travel_agency_name = 'Checkout Travel Agents'
        ticket.travel_agency_code = '91114362'

        passenger_address = PaymentSetupAirlinePassengerAddress()
        passenger_address.country = 'GB'
        passenger = PaymentSetupAirlinePassenger()
        passenger.first_name = 'John'
        passenger.last_name = 'Smith'
        passenger.date_of_birth = '1990-10-31'
        passenger.address = passenger_address

        leg = PaymentSetupFlightLegDetails()
        leg.flight_number = 'BA1483'
        leg.carrier_code = 'BA'
        leg.class_of_travelling = 'W'
        leg.departure_airport = 'LHR'
        leg.departure_date = '2025-10-13'
        leg.departure_time = '18:30'
        leg.arrival_airport = 'JFK'
        leg.stop_over_code = 'X'
        leg.fare_basis_code = 'WUP14B'

        price = PaymentSetupAirlineInsurancePrice()
        price.amount = 500
        price.currency = 'SAR'
        insurance = PaymentSetupAirlineInsurance()
        insurance.type = 'travel'
        insurance.company = 'AXA'
        insurance.price = price

        airline = PaymentSetupAirline()
        airline.ticket = ticket
        airline.passengers = [passenger]
        airline.flight_leg_details = [leg]
        airline.total_number_of_passengers = 1
        airline.travel_type = 'international'
        airline.trip_type = 'one_way'
        airline.refundable = True
        airline.delivery_recipient = 'jane.smith@example.com'
        airline.ancillaries = 'extra_baggage'
        airline.insurance = insurance

        industry = Industry()
        industry.airline = [airline]

        assert _serialize(industry) == {
            'airline': [{
                'ticket': {
                    'number': '0742464639523',
                    'issue_date': '2025-05-01',
                    'issuing_carrier_code': '042',
                    'travel_package_indicator': 'A',
                    'travel_agency_name': 'Checkout Travel Agents',
                    'travel_agency_code': '91114362',
                },
                'passengers': [{
                    'first_name': 'John',
                    'last_name': 'Smith',
                    'date_of_birth': '1990-10-31',
                    'address': {'country': 'GB'},
                }],
                'flight_leg_details': [{
                    'flight_number': 'BA1483',
                    'carrier_code': 'BA',
                    'class_of_travelling': 'W',
                    'departure_airport': 'LHR',
                    'departure_date': '2025-10-13',
                    'departure_time': '18:30',
                    'arrival_airport': 'JFK',
                    'stop_over_code': 'X',
                    'fare_basis_code': 'WUP14B',
                }],
                'total_number_of_passengers': 1,
                'travel_type': 'international',
                'trip_type': 'one_way',
                'refundable': True,
                'delivery_recipient': 'jane.smith@example.com',
                'ancillaries': 'extra_baggage',
                'insurance': {
                    'type': 'travel',
                    'company': 'AXA',
                    'price': {'amount': 500, 'currency': 'SAR'},
                },
            }]
        }


class TestDateFieldTypes:
    """The specification declares these fields `format: date`.

    The serializer renders anything with strftime through isoformat(), so a datetime emits a full
    ISO timestamp. Only a yyyy-MM-dd string produces the declared format, so these attributes are
    annotated `str` -- the same convention as BacsNotificationRequest.collection_date and
    SepaInstrumentData.date_of_signature.
    """

    def test_merchant_account_date_fields_are_annotated_as_strings(self):
        for field in (
            'registration_date', 'last_modified',
            'first_transaction_date', 'last_transaction_date',
        ):
            assert MerchantAccount.__annotations__[field] is str, field

    def test_sub_merchant_and_mandate_date_fields_are_annotated_as_strings(self):
        assert OrderSubMerchant.__annotations__['registration_date'] is str
        assert SepaMandate.__annotations__['date_of_signature'] is str

    def test_merchant_account_string_dates_serialize_in_the_declared_format(self):
        account = MerchantAccount()
        account.id = 'acct_1'
        account.registration_date = '2023-05-01'
        account.last_modified = '2023-05-02'
        account.first_transaction_date = '2023-09-15'
        account.last_transaction_date = '2025-03-28'

        serialized = _serialize(account)

        assert serialized['registration_date'] == '2023-05-01'
        assert serialized['last_modified'] == '2023-05-02'
        assert serialized['first_transaction_date'] == '2023-09-15'
        assert serialized['last_transaction_date'] == '2025-03-28'

    def test_sub_merchant_string_date_serializes_in_the_declared_format(self):
        sub_merchant = OrderSubMerchant()
        sub_merchant.id = 'sub_1'
        sub_merchant.registration_date = '2023-01-15'

        assert _serialize(sub_merchant)['registration_date'] == '2023-01-15'

    def test_mandate_string_date_serializes_in_the_declared_format(self):
        mandate = SepaMandate()
        mandate.id = 'mandate_1'
        mandate.date_of_signature = '2020-01-01'

        assert _serialize(mandate)['date_of_signature'] == '2020-01-01'

    def test_unset_date_fields_are_absent(self):
        account = MerchantAccount()
        account.id = 'acct_1'

        serialized = _serialize(account)

        for field in (
            'registration_date', 'last_modified',
            'first_transaction_date', 'last_transaction_date',
        ):
            assert field not in serialized, field

    def test_a_datetime_would_not_serialize_in_the_declared_format(self):
        # Documents why the annotation is str: this is what a datetime produces. These fields were
        # annotated `datetime`, so following the annotation put a timestamp on a date-only field.
        from datetime import datetime
        account = MerchantAccount()
        account.registration_date = datetime(2023, 5, 1)

        assert _serialize(account)['registration_date'] == '2023-05-01T00:00:00'


_CASH_APP_REDIRECT_URL = ('https://sandbox.api.cash.app/customer-request/v1/requests/'
                          'GRR_f5xg6wrxhtv3p4w24g0wrexa/interstitial?validity_token=bap03y')

_CASH_APP_CUSTOMER_ID = 'CST_AYVkuLzfsRqEhf4OyQFxQNv22m7IjNFjO6f2J5CDE2nxAC4-21wJ2H8_2kvsdIsDZMN4'


class TestCashAppSerialization:
    """Cash App Pay on Payment Setups: payment_methods.cashapp and the customer device fields."""

    def test_cash_app_request_serializes_to_the_spec_body(self):
        cashapp = CashApp()
        cashapp.initialization = PaymentMethodInitialization.ENABLED
        cashapp.customer_profile_sharing = True
        payment_methods = PaymentMethods()
        payment_methods.cashapp = cashapp

        device = CustomerDevice()
        device.locale = 'en_US'
        device.fingerprint = 'fp_abc123xyz'
        device.ipv4 = '203.0.113.0'
        device.ipv6 = '2001:db8:85a3::8a2e:370:7334'
        device.client = CustomerDeviceClient.WEB
        device.os = OsType.ANDROID
        customer = Customer()
        customer.device = device

        request = PaymentSetupsRequest()
        request.processing_channel_id = 'pc_aaaaaaaaaaaaaaaaaaaaaaaaaa'
        request.amount = 1000
        request.currency = Currency.USD
        request.payment_methods = payment_methods
        request.customer = customer

        body = json.dumps(request, cls=JsonSerializer)

        # The wire key is one lowercase word. Checked on the raw string, case-sensitively.
        assert '"cashapp"' in body
        assert 'cash_app' not in body
        assert 'cashApp' not in body
        assert '"customer_profile_sharing"' in body
        assert 'customerProfileSharing' not in body
        assert json.loads(body) == {
            'processing_channel_id': 'pc_aaaaaaaaaaaaaaaaaaaaaaaaaa',
            'amount': 1000,
            'currency': 'USD',
            'payment_methods': {
                'cashapp': {'initialization': 'enabled', 'customer_profile_sharing': True},
            },
            'customer': {
                'device': {
                    'locale': 'en_US',
                    'fingerprint': 'fp_abc123xyz',
                    'ipv4': '203.0.113.0',
                    'ipv6': '2001:db8:85a3::8a2e:370:7334',
                    'client': 'web',
                    'os': 'android',
                },
            },
        }

    def test_cash_app_initialization_defaults_to_disabled(self):
        assert _serialize(CashApp()) == {'initialization': 'disabled'}

    @pytest.mark.parametrize('client, expected', [
        (CustomerDeviceClient.WEB, 'web'),
        (CustomerDeviceClient.MOBILE_WEB, 'mobile_web'),
        (CustomerDeviceClient.APP, 'app'),
    ])
    def test_device_client_serializes_each_spec_value(self, client, expected):
        device = CustomerDevice()
        device.client = client

        assert _serialize(device) == {'client': expected}

    @pytest.mark.parametrize('os_type, expected', [
        (OsType.ANDROID, 'android'),
        (OsType.IOS, 'ios'),
    ])
    def test_device_os_serializes_each_spec_value(self, os_type, expected):
        device = CustomerDevice()
        device.os = os_type

        assert _serialize(device) == {'os': expected}

    def test_cash_app_customer_profile_sharing_false_is_sent(self):
        cashapp = CashApp()
        cashapp.customer_profile_sharing = False

        body = json.loads(json.dumps(cashapp, cls=JsonSerializer))

        # Only unset attributes are omitted; an explicit False must still reach the API.
        assert 'customer_profile_sharing' in body
        assert body['customer_profile_sharing'] is False

    def test_device_with_only_locale_serializes_only_locale(self):
        device = CustomerDevice()
        device.locale = 'en_US'

        assert _serialize(device) == {'locale': 'en_US'}

    def test_cash_app_response_reads_every_field(self):
        # The Payment Setup response, as returned by create, update, get and confirm.
        response = ResponseWrapper(None, {
            'id': 'pset_123',
            'processing_channel_id': 'pc_aaaaaaaaaaaaaaaaaaaaaaaaaa',
            'amount': 1000,
            'currency': 'USD',
            'customer': {
                'device': {
                    'locale': 'en_US',
                    'fingerprint': 'fp_abc123xyz',
                    'ipv4': '203.0.113.0',
                    'ipv6': '2001:db8:85a3::8a2e:370:7334',
                    'client': 'web',
                    'os': 'android',
                },
            },
            'payment_methods': {
                'cashapp': {
                    'status': 'action_required',
                    'flags': [],
                    'initialization': 'enabled',
                    'customer_profile_sharing': True,
                    'reference': 'ORDER-99',
                    'action': {'type': 'redirect', 'redirect_url': _CASH_APP_REDIRECT_URL},
                    'customer_profile': {
                        'customer_id': _CASH_APP_CUSTOMER_ID,
                        'cashtag': '$CASHTAG_C_TOKEN',
                        'reference_id': 'value',
                        'full_name': 'John Middle Doe',
                        'given_name': 'John',
                        'middle_name': 'Middle',
                        'family_name': 'Doe',
                        'suffix': 'Jr.',
                        'birth_date': '1990-01-01T00:00:00.0000000',
                        'address': {
                            'address_line_1': '123 Main St',
                            'address_line_2': 'Apt 2',
                            'address_line_3': 'Floor 3',
                            'locality': 'Springfield',
                            'sublocality': 'Downtown',
                            'administrative_district_level_1': 'IL',
                            'postal_code': '62701',
                            'country': 'US',
                        },
                        'phone_number': '5555555555',
                        'email_address': 'cash@cash.com',
                        'customer_since': '1970-01-18T12:46:04.8000000+00:00',
                    },
                },
            },
            'available_payment_methods': ['cashapp'],
        })

        device = response.customer.device
        assert device.locale == 'en_US'
        assert device.fingerprint == 'fp_abc123xyz'
        assert device.ipv4 == '203.0.113.0'
        assert device.ipv6 == '2001:db8:85a3::8a2e:370:7334'
        assert device.client == CustomerDeviceClient.WEB
        assert device.os == OsType.ANDROID

        cashapp = response.payment_methods.cashapp
        assert cashapp.status == 'action_required'
        assert cashapp.flags == []
        assert cashapp.initialization == PaymentMethodInitialization.ENABLED
        assert cashapp.customer_profile_sharing is True
        assert cashapp.reference == 'ORDER-99'
        assert cashapp.action.type == CashAppActionType.REDIRECT
        assert cashapp.action.redirect_url == _CASH_APP_REDIRECT_URL

        profile = cashapp.customer_profile
        assert profile.customer_id == _CASH_APP_CUSTOMER_ID
        assert profile.cashtag == '$CASHTAG_C_TOKEN'
        assert profile.reference_id == 'value'
        assert profile.full_name == 'John Middle Doe'
        assert profile.given_name == 'John'
        assert profile.middle_name == 'Middle'
        assert profile.family_name == 'Doe'
        assert profile.suffix == 'Jr.'
        assert profile.birth_date == '1990-01-01T00:00:00.0000000'
        assert profile.phone_number == '5555555555'
        assert profile.email_address == 'cash@cash.com'
        assert profile.customer_since == '1970-01-18T12:46:04.8000000+00:00'

        address = profile.address
        assert address.address_line_1 == '123 Main St'
        assert address.address_line_2 == 'Apt 2'
        assert address.address_line_3 == 'Floor 3'
        assert address.locality == 'Springfield'
        assert address.sublocality == 'Downtown'
        assert address.administrative_district_level_1 == 'IL'
        assert address.postal_code == '62701'
        assert address.country == 'US'

    def test_cash_app_round_trip_keeps_every_property_and_the_literal_address_keys(self):
        address = CashAppAddress()
        address.address_line_1 = '123 Main St'
        address.address_line_2 = 'Apt 2'
        address.address_line_3 = 'Floor 3'
        address.locality = 'Springfield'
        address.sublocality = 'Downtown'
        address.administrative_district_level_1 = 'IL'
        address.postal_code = '62701'
        address.country = 'US'

        profile = CashAppCustomerProfile()
        profile.customer_id = _CASH_APP_CUSTOMER_ID
        profile.cashtag = '$CASHTAG_C_TOKEN'
        profile.reference_id = 'value'
        profile.full_name = 'John Middle Doe'
        profile.given_name = 'John'
        profile.middle_name = 'Middle'
        profile.family_name = 'Doe'
        profile.suffix = 'Jr.'
        profile.birth_date = '1990-01-01T00:00:00.0000000'
        profile.address = address
        profile.phone_number = '5555555555'
        profile.email_address = 'cash@cash.com'
        profile.customer_since = '1970-01-18T12:46:04.8000000+00:00'

        action = CashAppAction()
        action.type = CashAppActionType.REDIRECT
        action.redirect_url = _CASH_APP_REDIRECT_URL

        cashapp = CashApp()
        cashapp.status = 'action_required'
        cashapp.flags = []
        cashapp.initialization = PaymentMethodInitialization.ENABLED
        cashapp.customer_profile_sharing = True
        cashapp.reference = 'ORDER-99'
        cashapp.action = action
        cashapp.customer_profile = profile

        body = json.dumps(cashapp, cls=JsonSerializer)

        for key in ('"address_line_1"', '"address_line_2"', '"address_line_3"',
                    '"administrative_district_level_1"', '"redirect_url"'):
            assert key in body, key
        assert 'address_line1' not in body
        assert 'administrative_district_level1' not in body

        read = ResponseWrapper(None, json.loads(body))

        assert read.status == cashapp.status
        assert read.flags == cashapp.flags
        assert read.initialization == cashapp.initialization
        assert read.customer_profile_sharing is True
        assert read.reference == cashapp.reference
        assert read.action.type == action.type
        assert read.action.redirect_url == action.redirect_url
        for field in ('customer_id', 'cashtag', 'reference_id', 'full_name', 'given_name',
                      'middle_name', 'family_name', 'suffix', 'birth_date', 'phone_number',
                      'email_address', 'customer_since'):
            assert getattr(read.customer_profile, field) == getattr(profile, field), field
        for field in ('address_line_1', 'address_line_2', 'address_line_3', 'locality',
                      'sublocality', 'administrative_district_level_1', 'postal_code', 'country'):
            assert getattr(read.customer_profile.address, field) == getattr(address, field), field


class TestPaymentSetupCustomerSerialization:
    """PaymentSetup.customer, all eight properties."""

    def test_customer_round_trip_keeps_every_property(self):
        email = CustomerEmail()
        email.address = 'johnsmith@example.com'
        email.verified = True
        phone = Phone()
        phone.country_code = '+44'
        phone.number = '207 946 0000'
        device = CustomerDevice()
        device.locale = 'en_GB'
        device.fingerprint = 'fp_abc123xyz'
        device.ipv4 = '203.0.113.0'
        device.ipv6 = '2001:db8:85a3::8a2e:370:7334'
        device.client = CustomerDeviceClient.MOBILE_WEB
        device.os = OsType.IOS
        merchant_account = MerchantAccount()
        merchant_account.id = 'acct_1'
        merchant_account.registration_date = '2023-05-01'
        merchant_account.last_modified = '2023-05-02'
        merchant_account.returning_customer = True
        merchant_account.first_transaction_date = '2023-09-15'
        merchant_account.last_transaction_date = '2025-03-28'
        merchant_account.total_order_count = 6
        merchant_account.last_payment_amount = 5599

        customer = Customer()
        customer.country = 'GB'
        customer.id = 'cus_123456789'
        customer.email = email
        customer.name = 'John Smith'
        customer.tax_number = 'GB123456789'
        customer.phone = phone
        customer.device = device
        customer.merchant_account = merchant_account

        body = json.dumps(customer, cls=JsonSerializer)

        assert '"id": "cus_123456789"' in body
        assert '"country": "GB"' in body
        assert '"tax_number": "GB123456789"' in body
        assert 'taxNumber' not in body

        read = ResponseWrapper(None, json.loads(body))

        assert read.country == 'GB'
        assert read.id == 'cus_123456789'
        assert read.name == 'John Smith'
        assert read.tax_number == 'GB123456789'
        assert read.email.address == email.address
        assert read.email.verified is True
        assert read.phone.country_code == phone.country_code
        assert read.phone.number == phone.number
        for field in ('locale', 'fingerprint', 'ipv4', 'ipv6', 'client', 'os'):
            assert getattr(read.device, field) == getattr(device, field), field
        for field in ('id', 'registration_date', 'last_modified', 'returning_customer',
                      'first_transaction_date', 'last_transaction_date', 'total_order_count',
                      'last_payment_amount'):
            assert getattr(read.merchant_account, field) == getattr(merchant_account, field), field

    def test_customer_spec_example_reads(self):
        read = ResponseWrapper(None, {
            'country': 'GB',
            'id': 'cus_123456789',
            'email': {'address': 'johnsmith@example.com', 'verified': True},
            'name': 'John Smith',
            'tax_number': 'GB123456789',
            'phone': {'country_code': '+44', 'number': '207 946 0000'},
            'device': {'locale': 'en_GB'},
        })

        assert read.country == 'GB'
        assert read.id == 'cus_123456789'
        assert read.email.address == 'johnsmith@example.com'
        assert read.email.verified is True
        assert read.name == 'John Smith'
        assert read.tax_number == 'GB123456789'
        assert read.phone.country_code == '+44'
        assert read.phone.number == '207 946 0000'
        assert read.device.locale == 'en_GB'
