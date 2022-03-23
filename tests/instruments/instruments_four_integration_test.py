from __future__ import absolute_import

import pytest

from checkout_sdk.common.common_four import AccountHolder, UpdateCustomerRequest
from checkout_sdk.common.enums import Country, Currency
from checkout_sdk.common.enums_four import AccountHolderType
from checkout_sdk.exception import CheckoutApiException
from checkout_sdk.instruments.instruments_four import CreateTokenInstrumentRequest, CreateCustomerInstrumentRequest, \
    UpdateCardInstrumentRequest, BankAccountFieldQuery, PaymentNetwork
from checkout_sdk.tokens.tokens import CardTokenRequest
from tests.checkout_test_utils import assert_response, phone, VisaCard, address, random_email, FIRST_NAME, LAST_NAME, \
    NAME


def test_should_create_and_get_instrument(four_api):
    create_instrument_response = create_token_instrument(four_api)
    assert_response(create_instrument_response,
                    'bin',
                    'card_category',
                    'card_type',
                    'customer',
                    'customer.email',
                    'customer.name',
                    'expiry_month',
                    'expiry_year',
                    'fingerprint',
                    'id',
                    # 'issuer',
                    'issuer_country',
                    'last4',
                    'product_id',
                    'product_type',
                    'type')

    get_instrument_response = four_api.instruments.get(create_instrument_response['id'])

    assert_response(get_instrument_response,
                    'bin',
                    'card_category',
                    'card_type',
                    'customer',
                    'customer.email',
                    'customer.name',
                    'expiry_month',
                    'expiry_year',
                    'fingerprint',
                    'id',
                    # 'issuer',
                    'issuer_country',
                    'last4',
                    'product_id',
                    'product_type',
                    'type')


def test_should_create_and_update_instrument(four_api):
    create_instrument_response = create_token_instrument(four_api)

    update_instrument_request = UpdateCardInstrumentRequest()
    update_instrument_request.name = 'new name'
    update_instrument_request.expiry_year = 2026
    update_instrument_request.expiry_month = 12

    update_customer_request = UpdateCustomerRequest()
    update_customer_request.id = create_instrument_response['customer']['id']
    update_customer_request.default = True
    update_instrument_request.customer = update_customer_request

    account_holder = AccountHolder()
    account_holder.first_name = FIRST_NAME
    account_holder.last_name = LAST_NAME
    account_holder.phone = phone()
    account_holder.billing_address = address()
    update_instrument_request.account_holder = account_holder

    four_api.instruments.update(create_instrument_response['id'], update_instrument_request)

    get_instrument_response = four_api.instruments.get(create_instrument_response['id'])

    assert get_instrument_response is not None
    assert get_instrument_response['name'] == 'new name'
    assert get_instrument_response['expiry_year'] == 2026
    assert get_instrument_response['expiry_month'] == 12

    assert_response(create_instrument_response,
                    'scheme',
                    'bin',
                    'card_category',
                    'card_type',
                    'customer',
                    'customer.email',
                    'customer.name',
                    'expiry_month',
                    'expiry_year',
                    'fingerprint',
                    'id',
                    # 'issuer',
                    'issuer_country',
                    'last4',
                    'product_id',
                    'product_type',
                    'customer',
                    'type')


def test_should_create_and_delete_instrument(four_api):
    create_instrument_response = create_token_instrument(four_api)

    four_api.instruments.delete(create_instrument_response['id'])

    with pytest.raises(CheckoutApiException):
        four_api.instruments.get(create_instrument_response['id'])


def test_should_get_bank_account_field_formatting(oauth_api):
    query = BankAccountFieldQuery()
    query.account_holder_type = AccountHolderType.INDIVIDUAL
    query.payment_network = PaymentNetwork.LOCAL

    response = oauth_api.instruments.get_bank_account_field_formatting(Country.GB, Currency.GBP, query)
    assert_response(response, 'sections')
    assert response['sections'].__len__() == 3
    for section in response['sections']:
        assert_response(section, 'name', 'fields')
        for field in section['fields']:
            assert_response(field, 'id', 'display', 'type')


def create_token_instrument(four_api):
    card_token_request = CardTokenRequest()
    card_token_request.number = VisaCard.number
    card_token_request.expiry_month = VisaCard.expiry_month
    card_token_request.expiry_year = VisaCard.expiry_year
    card_token_request.cvv = VisaCard.cvv
    card_token_request.name = VisaCard.name
    card_token_request.billing_address = address()
    card_token_request.phone = phone()

    card_token_response = four_api.tokens.request_card_token(card_token_request)
    assert_response(card_token_response, 'token')

    account_holder = AccountHolder()
    account_holder.first_name = FIRST_NAME
    account_holder.last_name = LAST_NAME
    account_holder.phone = phone()

    customer = CreateCustomerInstrumentRequest()
    customer.email = random_email()
    customer.name = NAME
    customer.default = True
    customer.phone = phone()

    create_instrument_request = CreateTokenInstrumentRequest()
    create_instrument_request.token = card_token_response['token']
    create_instrument_request.account_holder = account_holder
    create_instrument_request.customer = customer

    create_instrument_response = four_api.instruments.create(create_instrument_request)
    assert_response(card_token_response, 'token')

    return create_instrument_response
