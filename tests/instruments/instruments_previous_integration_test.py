from __future__ import absolute_import

import pytest

from checkout_sdk.exception import CheckoutApiException
from checkout_sdk.instruments.instruments_previous import CreateInstrumentRequest, InstrumentCustomerRequest, \
    UpdateInstrumentRequest
from checkout_sdk.tokens.tokens import CardTokenRequest
from tests.checkout_test_utils import assert_response, phone, VisaCard, address, NAME


def test_should_create_and_get_instrument(previous_api):
    create_instrument_response = create_token_instrument(previous_api)
    assert_response(create_instrument_response,
                    'http_metadata',
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

    get_instrument_response = previous_api.instruments.get(create_instrument_response.id)

    assert_response(get_instrument_response,
                    'http_metadata',
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


def test_should_create_and_update_instrument(previous_api):
    create_instrument_response = create_token_instrument(previous_api)

    update_instrument_request = UpdateInstrumentRequest()
    update_instrument_request.name = 'new name'
    update_instrument_request.expiry_year = 2026
    update_instrument_request.expiry_month = 12

    previous_api.instruments.update(create_instrument_response.id, update_instrument_request)

    get_instrument_response = previous_api.instruments.get(create_instrument_response.id)

    assert get_instrument_response is not None
    assert get_instrument_response.name == 'new name'
    assert get_instrument_response.expiry_year == 2026
    assert get_instrument_response.expiry_month == 12


def test_should_create_and_delete_instrument(previous_api):
    create_instrument_response = create_token_instrument(previous_api)

    previous_api.instruments.delete(create_instrument_response.id)

    with pytest.raises(CheckoutApiException):
        previous_api.instruments.get(create_instrument_response.id)


def create_token_instrument(previous_api):
    card_token_request = CardTokenRequest()
    card_token_request.number = VisaCard.number
    card_token_request.expiry_month = VisaCard.expiry_month
    card_token_request.expiry_year = VisaCard.expiry_year
    card_token_request.cvv = VisaCard.cvv
    card_token_request.name = VisaCard.name
    card_token_request.billing_address = address()
    card_token_request.phone = phone()

    card_token_response = previous_api.tokens.request_card_token(card_token_request)
    assert_response(card_token_response, 'token')

    customer = InstrumentCustomerRequest
    customer.email = 'brucewayne@gmail.com'
    customer.name = NAME
    customer.default = True
    customer.phone = phone()

    create_instrument_request = CreateInstrumentRequest()
    create_instrument_request.token = card_token_response.token
    create_instrument_request.customer = customer

    create_instrument_response = previous_api.instruments.create(create_instrument_request)
    assert_response(card_token_response, 'token')

    return create_instrument_response
