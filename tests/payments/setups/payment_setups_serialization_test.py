import json
from datetime import datetime

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
    CashAppCustomerProfile, PaymentSetupRisk, CardDetails, CardToken, WalletToken, PaymentSetupCardScheme,
    GooglePayPreferredScheme,
)
from checkout_sdk.payments.payments import PreferredSchema


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
        token = WalletToken()
        token.id = 'tok_x'
        googlepay.token = token
        token_data = GooglePayTokenData()
        token_data.protocol_version = 'ECv2'
        token_data.signature = 'sig'
        token_data.signed_message = 'msg'
        token_data.tokenization_key = 'pk_x'
        googlepay.token_data = token_data

        assert _serialize(googlepay) == {
            'token': {'id': 'tok_x'},
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
        details = CardDetails()
        details.number = '4242424242424242'
        details.expiry_month = 12
        details.expiry_year = 2030
        details.name = 'John Smith'
        details.cvv = '100'
        card = Card()
        card.details = details

        holder = PaymentSetupAccountHolder()
        holder.type = PaymentSetupAccountHolderType.INDIVIDUAL
        holder.first_name = 'John'
        holder.last_name = 'Smith'
        card.account_holder = holder

        assert _serialize(card) == {
            'details': {
                'number': '4242424242424242',
                'expiry_month': 12,
                'expiry_year': 2030,
                'name': 'John Smith',
                'cvv': '100',
            },
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
            'merchant_account': {
                'id': '1234',
                'registration_date': '2023-05-01T00:00:00.0000000',
                'last_modified': '2023-05-01T00:00:00.0000000',
                'returning_customer': True,
                'first_transaction_date': '2023-09-15T00:00:00.0000000',
                'last_transaction_date': '2025-03-28T00:00:00.0000000',
                'total_order_count': 6,
                'last_payment_amount': 55.99,
            },
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
        assert read.merchant_account.id == '1234'
        assert read.merchant_account.registration_date == '2023-05-01T00:00:00.0000000'
        assert read.merchant_account.last_modified == '2023-05-01T00:00:00.0000000'
        assert read.merchant_account.returning_customer is True
        assert read.merchant_account.first_transaction_date == '2023-09-15T00:00:00.0000000'
        assert read.merchant_account.last_transaction_date == '2025-03-28T00:00:00.0000000'
        assert read.merchant_account.total_order_count == 6
        assert read.merchant_account.last_payment_amount == 55.99


class TestPayByBankKeyAndRiskSerialization:

    def _request(self):
        request = PaymentSetupsRequest()
        request.processing_channel_id = 'pc_aaaaaaaaaaaaaaaaaaaaaaaaaa'
        request.amount = 1000
        request.currency = Currency.GBP
        pay_by_bank = PayByBank()
        pay_by_bank.bank_id = 'ob-natwest'
        methods = PaymentMethods()
        methods.paybybank = pay_by_bank
        request.payment_methods = methods
        risk = PaymentSetupRisk()
        risk.enabled = False
        request.risk = risk
        return request

    def test_request_sends_the_literal_paybybank_key(self):
        body = json.dumps(self._request(), cls=JsonSerializer)

        assert '"paybybank"' in body
        assert 'pay_by_bank' not in body
        assert json.loads(body)['payment_methods'] == {'paybybank': {'bank_id': 'ob-natwest'}}

    def test_request_sends_risk_enabled_false(self):
        assert _serialize(self._request())['risk'] == {'enabled': False}

    def test_risk_enabled_true_serializes(self):
        risk = PaymentSetupRisk()
        risk.enabled = True

        assert _serialize(risk) == {'enabled': True}

    def test_request_round_trip_keeps_paybybank_and_risk(self):
        read = ResponseWrapper(None, _serialize(self._request()))

        assert read.payment_methods.paybybank.bank_id == 'ob-natwest'
        assert read.risk.enabled is False
        assert not hasattr(read.payment_methods, 'pay_by_bank')

    def test_response_reads_paybybank_action(self):
        response = ResponseWrapper(None, {
            'id': 'pset_123',
            'risk': {'enabled': True},
            'payment_methods': {
                'paybybank': {
                    'status': 'action_required',
                    'flags': [],
                    'action': {
                        'type': 'select_bank',
                        'banks': [{
                            'bank_id': 'ob-natwest',
                            'display_name': 'NatWest',
                            'logo_url': 'https://example.com/natwest.png',
                            'available': True,
                        }],
                    },
                },
            },
        })

        method = response.payment_methods.paybybank
        assert method.status == 'action_required'
        assert method.flags == []
        assert method.action.type == 'select_bank'
        bank = method.action.banks[0]
        assert bank.bank_id == 'ob-natwest'
        assert bank.display_name == 'NatWest'
        assert bank.logo_url == 'https://example.com/natwest.png'
        assert bank.available is True
        assert response.risk.enabled is True


_CARD_DETAIL_FIELDS = ('number', 'last4', 'bin', 'scheme', 'expiry_month', 'expiry_year', 'name',
                       'cvv', 'stored', 'expires_on', 'allow_update')

_CARD_DETAIL_VALUES = {
    'number': '4242424242424242',
    'last4': '4242',
    'bin': '424242',
    'scheme': 'Visa',
    'expiry_month': 12,
    'expiry_year': 2030,
    'name': 'John Smith',
    'cvv': '100',
    'stored': True,
    'expires_on': datetime(2026, 6, 1, 10, 0, 0),
    'allow_update': True,
}

_CARD_DETAIL_WIRE = dict(_CARD_DETAIL_VALUES, expires_on='2026-06-01T10:00:00')

_WALLET_TOKEN_ID = 'tok_ubfj2q76miwundwlk72vxt2i7q'


def _phone():
    phone = Phone()
    phone.country_code = '+44'
    phone.number = '207 946 0000'
    return phone


def _account_holder():
    holder = PaymentSetupAccountHolder()
    holder.type = PaymentSetupAccountHolderType.INDIVIDUAL
    holder.first_name = 'John'
    holder.last_name = 'Smith'
    holder.middle_name = 'Paul'
    holder.company_name = 'ACME Ltd'
    holder.account_name_inquiry = True
    return holder


_ACCOUNT_HOLDER_WIRE = {
    'type': 'individual', 'first_name': 'John', 'last_name': 'Smith', 'middle_name': 'Paul',
    'company_name': 'ACME Ltd', 'account_name_inquiry': True,
}


class TestPaymentSetupCardSerialization:
    """payment_methods.card: token, details and the card-level properties, all of them."""

    def _card(self):
        details = CardDetails()
        for field, value in _CARD_DETAIL_VALUES.items():
            setattr(details, field, value)
        token = CardToken()
        token.id = 'tok_4gzeau5o2uqubbk6fufs3m7p54'
        card = Card()
        card.status = 'ready'
        card.flags = ['flag_a']
        card.token = token
        card.details = details
        card.store_for_future_use = True
        card.phone = _phone()
        card.account_holder = _account_holder()
        card.schemes = [PaymentSetupCardScheme.VISA, PaymentSetupCardScheme.CARTES_BANCAIRES]
        card.preferred_scheme = PreferredSchema.CARTES_BANCAIRES
        return card

    def test_card_serializes_every_property_under_the_spec_keys(self):
        body = json.dumps(self._card(), cls=JsonSerializer)

        for key in ('"token"', '"details"', '"store_for_future_use"', '"schemes"',
                    '"preferred_scheme"', '"expiry_month"', '"allow_update"'):
            assert key in body, key
        assert json.loads(body) == {
            'status': 'ready',
            'flags': ['flag_a'],
            'token': {'id': 'tok_4gzeau5o2uqubbk6fufs3m7p54'},
            'details': _CARD_DETAIL_WIRE,
            'store_for_future_use': True,
            'phone': {'country_code': '+44', 'number': '207 946 0000'},
            'account_holder': _ACCOUNT_HOLDER_WIRE,
            'schemes': ['visa', 'cartes_bancaires'],
            'preferred_scheme': 'cartes_bancaires',
        }

    def test_card_round_trip_keeps_every_property(self):
        card = self._card()

        read = ResponseWrapper(None, _serialize(card))

        assert read.status == 'ready'
        assert read.flags == ['flag_a']
        assert read.token.id == card.token.id
        for field in _CARD_DETAIL_FIELDS:
            assert getattr(read.details, field) == _CARD_DETAIL_WIRE[field], field
        assert read.store_for_future_use is True
        assert read.phone.country_code == '+44'
        assert read.phone.number == '207 946 0000'
        for field, value in _ACCOUNT_HOLDER_WIRE.items():
            assert getattr(read.account_holder, field) == value, field
        assert read.schemes == [PaymentSetupCardScheme.VISA, PaymentSetupCardScheme.CARTES_BANCAIRES]
        assert read.preferred_scheme == PreferredSchema.CARTES_BANCAIRES

    def test_card_spec_example_reads(self):
        read = ResponseWrapper(None, {
            'status': 'ready',
            'flags': [],
            'token': {'id': 'tok_4gzeau5o2uqubbk6fufs3m7p54'},
            'details': {
                'last4': '4242', 'bin': '424242', 'scheme': 'Visa', 'expiry_month': 12,
                'expiry_year': 2030, 'expires_on': '2026-06-01T10:00:00Z', 'allow_update': True,
            },
            'phone': {'country_code': '+44', 'number': '207 946 0000'},
            'account_holder': {'type': 'individual', 'first_name': 'John', 'last_name': 'Smith'},
            'schemes': ['visa', 'mastercard'],
            'preferred_scheme': 'visa',
        })

        assert read.status == 'ready'
        assert read.token.id == 'tok_4gzeau5o2uqubbk6fufs3m7p54'
        assert read.details.last4 == '4242'
        assert read.details.bin == '424242'
        assert read.details.scheme == 'Visa'
        assert read.details.expiry_month == 12
        assert read.details.expiry_year == 2030
        assert read.details.expires_on == '2026-06-01T10:00:00Z'
        assert read.details.allow_update is True
        assert read.phone.number == '207 946 0000'
        assert read.account_holder.type == PaymentSetupAccountHolderType.INDIVIDUAL
        assert read.schemes == [PaymentSetupCardScheme.VISA, PaymentSetupCardScheme.MASTERCARD]
        assert read.preferred_scheme == PreferredSchema.VISA

    @pytest.mark.parametrize('field', _CARD_DETAIL_FIELDS)
    def test_deprecated_flat_card_attribute_is_sent_under_details(self, field):
        card = Card()

        with pytest.deprecated_call():
            setattr(card, field, _CARD_DETAIL_VALUES[field])
        with pytest.deprecated_call():
            assert getattr(card, field) == _CARD_DETAIL_VALUES[field]

        assert getattr(card.details, field) == _CARD_DETAIL_VALUES[field]
        assert _serialize(card) == {'details': {field: _CARD_DETAIL_WIRE[field]}}

    def test_deprecated_flat_card_attributes_write_into_existing_details(self):
        details = CardDetails()
        details.number = '4242424242424242'
        card = Card()
        card.details = details

        with pytest.deprecated_call():
            card.cvv = '100'

        assert card.details is details
        assert _serialize(card) == {'details': {'number': '4242424242424242', 'cvv': '100'}}

    def test_unset_deprecated_flat_card_attribute_reads_as_missing(self):
        card = Card()

        with pytest.deprecated_call(), pytest.raises(AttributeError):
            _ = card.number
        assert _serialize(card) == {}


class TestPaymentSetupWalletSerialization:
    """payment_methods.applepay and payment_methods.googlepay: token object, schemes and
    preferred_scheme. Neither wallet has a details object."""

    @staticmethod
    def _token():
        token = WalletToken()
        token.id = _WALLET_TOKEN_ID
        token.expires_on = datetime(2026, 6, 1, 10, 0, 0)
        return token

    def _applepay(self):
        header = ApplePayTokenDataHeader()
        header.ephemeral_public_key = 'key'
        header.public_key_hash = 'hash'
        header.transaction_id = 'txn'
        token_data = ApplePayTokenData()
        token_data.version = 'EC_v1'
        token_data.data = 'encrypted'
        token_data.signature = 'sig'
        token_data.header = header
        applepay = ApplePay()
        applepay.status = 'ready'
        applepay.flags = ['flag_a']
        applepay.token_data = token_data
        applepay.token = self._token()
        applepay.store_for_future_use = True
        applepay.phone = _phone()
        applepay.account_holder = _account_holder()
        applepay.schemes = [PaymentSetupCardScheme.VISA, PaymentSetupCardScheme.CARTES_BANCAIRES]
        applepay.preferred_scheme = PreferredSchema.CARTES_BANCAIRES
        return applepay

    def _googlepay(self):
        token_data = GooglePayTokenData()
        token_data.protocol_version = 'ECv2'
        token_data.signature = 'sig'
        token_data.signed_message = 'msg'
        token_data.tokenization_key = 'pk_x'
        googlepay = GooglePay()
        googlepay.status = 'ready'
        googlepay.flags = ['flag_a']
        googlepay.token_data = token_data
        googlepay.token = self._token()
        googlepay.store_for_future_use = True
        googlepay.phone = _phone()
        googlepay.account_holder = _account_holder()
        googlepay.schemes = [PaymentSetupCardScheme.VISA, PaymentSetupCardScheme.MASTERCARD]
        googlepay.preferred_scheme = GooglePayPreferredScheme.MASTERCARD
        return googlepay

    def test_applepay_serializes_every_property_with_the_token_as_an_object(self):
        body = json.dumps(self._applepay(), cls=JsonSerializer)

        assert '"token": {' in body
        assert '"id": "%s"' % _WALLET_TOKEN_ID in body
        assert '"details"' not in body
        assert json.loads(body) == {
            'status': 'ready',
            'flags': ['flag_a'],
            'token_data': {
                'version': 'EC_v1', 'data': 'encrypted', 'signature': 'sig',
                'header': {'ephemeral_public_key': 'key', 'public_key_hash': 'hash',
                           'transaction_id': 'txn'},
            },
            'token': {'id': _WALLET_TOKEN_ID, 'expires_on': '2026-06-01T10:00:00'},
            'store_for_future_use': True,
            'phone': {'country_code': '+44', 'number': '207 946 0000'},
            'account_holder': _ACCOUNT_HOLDER_WIRE,
            'schemes': ['visa', 'cartes_bancaires'],
            'preferred_scheme': 'cartes_bancaires',
        }

    def test_googlepay_serializes_every_property_with_the_token_as_an_object(self):
        body = json.dumps(self._googlepay(), cls=JsonSerializer)

        assert '"token": {' in body
        assert '"id": "%s"' % _WALLET_TOKEN_ID in body
        assert '"details"' not in body
        assert json.loads(body) == {
            'status': 'ready',
            'flags': ['flag_a'],
            'token_data': {
                'protocol_version': 'ECv2', 'signature': 'sig', 'signed_message': 'msg',
                'tokenization_key': 'pk_x',
            },
            'token': {'id': _WALLET_TOKEN_ID, 'expires_on': '2026-06-01T10:00:00'},
            'store_for_future_use': True,
            'phone': {'country_code': '+44', 'number': '207 946 0000'},
            'account_holder': _ACCOUNT_HOLDER_WIRE,
            'schemes': ['visa', 'mastercard'],
            'preferred_scheme': 'mastercard',
        }

    @pytest.mark.parametrize('wallet', ['_applepay', '_googlepay'])
    def test_wallet_round_trip_keeps_every_property(self, wallet):
        method = getattr(self, wallet)()

        read = ResponseWrapper(None, _serialize(method))

        assert read.status == 'ready'
        assert read.flags == ['flag_a']
        assert read.token.id == _WALLET_TOKEN_ID
        assert read.token.expires_on == '2026-06-01T10:00:00'
        for field in vars(method.token_data):
            if field != 'header':
                assert getattr(read.token_data, field) == getattr(method.token_data, field), field
        assert read.store_for_future_use is True
        assert read.phone.number == '207 946 0000'
        for field, value in _ACCOUNT_HOLDER_WIRE.items():
            assert getattr(read.account_holder, field) == value, field
        assert read.schemes == method.schemes
        assert read.preferred_scheme == method.preferred_scheme

    def test_wallet_spec_example_reads(self):
        read = ResponseWrapper(None, {
            'status': 'ready',
            'flags': [],
            'token': {'id': _WALLET_TOKEN_ID, 'expires_on': '2026-06-01T10:00:00Z'},
            'schemes': ['visa', 'mastercard'],
            'preferred_scheme': 'visa',
        })

        assert read.status == 'ready'
        assert read.token.id == _WALLET_TOKEN_ID
        assert read.token.expires_on == '2026-06-01T10:00:00Z'
        assert read.schemes == [PaymentSetupCardScheme.VISA, PaymentSetupCardScheme.MASTERCARD]
        assert read.preferred_scheme == GooglePayPreferredScheme.VISA

    @pytest.mark.parametrize('wallet_type', [ApplePay, GooglePay])
    def test_deprecated_wallet_expires_on_is_sent_under_token(self, wallet_type):
        wallet = wallet_type()
        expires_on = datetime(2026, 6, 1, 10, 0, 0)

        with pytest.deprecated_call():
            wallet.expires_on = expires_on
        with pytest.deprecated_call():
            assert wallet.expires_on == expires_on

        assert wallet.token.expires_on == expires_on
        assert _serialize(wallet) == {'token': {'expires_on': '2026-06-01T10:00:00'}}

    def test_deprecated_wallet_expires_on_writes_into_existing_token(self):
        token = WalletToken()
        token.id = _WALLET_TOKEN_ID
        applepay = ApplePay()
        applepay.token = token

        with pytest.deprecated_call():
            applepay.expires_on = datetime(2026, 6, 1, 10, 0, 0)

        assert applepay.token is token
        assert _serialize(applepay) == {
            'token': {'id': _WALLET_TOKEN_ID, 'expires_on': '2026-06-01T10:00:00'}
        }


class TestPaymentSetupSchemeEnums:

    def test_card_scheme_has_every_spec_value(self):
        assert [s.value for s in PaymentSetupCardScheme] == [
            'accel', 'amex', 'cartes_bancaires', 'china_union_pay', 'diners', 'discover', 'jcb',
            'mada', 'maestro', 'mastercard', 'nyce', 'omannet', 'pulse', 'shazam', 'star', 'upi',
            'visa',
        ]

    def test_preferred_scheme_enums_have_every_spec_value(self):
        assert [s.value for s in PreferredSchema] == ['visa', 'mastercard', 'cartes_bancaires']
        assert [s.value for s in GooglePayPreferredScheme] == ['visa', 'mastercard']


class TestPaymentSetupRequestTopLevelSerialization:
    """payment_methods.auto_confirm, payment_methods.instrument and the request metadata."""

    def test_instrument_round_trip_keeps_every_spec_property(self):
        instrument = PaymentSetupInstrument()
        instrument.status = 'ready'
        instrument.flags = []
        instrument.id = 'src_wmlfc3zttb4uzmk6snpwb43jbi'
        instrument.type = 'bacs'

        body = json.dumps(instrument, cls=JsonSerializer)

        assert '"type": "bacs"' in body
        read = ResponseWrapper(None, json.loads(body))
        assert read.status == 'ready'
        assert read.flags == []
        assert read.id == 'src_wmlfc3zttb4uzmk6snpwb43jbi'
        assert read.type == 'bacs'

    def test_instrument_spec_example_reads(self):
        read = ResponseWrapper(None, {
            'status': 'ready',
            'id': 'src_wmlfc3zttb4uzmk6snpwb43jbi',
            'type': 'bacs',
            'action': {'type': 'set_instrument'},
        })

        assert read.id == 'src_wmlfc3zttb4uzmk6snpwb43jbi'
        assert read.type == 'bacs'
        assert read.action.type == 'set_instrument'

    def test_auto_confirm_and_metadata_serialize_under_the_spec_keys(self):
        payment_methods = PaymentMethods()
        payment_methods.auto_confirm = 'card'
        request = PaymentSetupsRequest()
        request.processing_channel_id = 'pc_aaaaaaaaaaaaaaaaaaaaaaaaaa'
        request.amount = 1000
        request.currency = Currency.GBP
        request.payment_methods = payment_methods
        request.metadata = {'coupon_code': 'NY2018', 'partner_id': 123989, 'vip': True}

        body = json.dumps(request, cls=JsonSerializer)

        assert '"auto_confirm": "card"' in body
        assert 'autoConfirm' not in body
        assert '"metadata"' in body
        assert json.loads(body) == {
            'processing_channel_id': 'pc_aaaaaaaaaaaaaaaaaaaaaaaaaa',
            'amount': 1000,
            'currency': 'GBP',
            'payment_methods': {'auto_confirm': 'card'},
            'metadata': {'coupon_code': 'NY2018', 'partner_id': 123989, 'vip': True},
        }

        read = ResponseWrapper(None, json.loads(body))
        assert read.payment_methods.auto_confirm == 'card'
        assert read.metadata.coupon_code == 'NY2018'
        assert read.metadata.partner_id == 123989
        assert read.metadata.vip is True
