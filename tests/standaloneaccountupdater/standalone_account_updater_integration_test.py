import pytest

from checkout_sdk.exception import CheckoutApiException
from checkout_sdk.standaloneaccountupdater.standalone_account_updater import (
    GetUpdatedCardCredentialsRequest, SourceOptions, CardDetailsRequest, InstrumentReference
)
from tests.checkout_test_utils import assert_response


# tests

@pytest.mark.skip(reason='Requires valid account updater credentials and live card data')
def test_should_get_updated_card_credentials_with_card(oauth_api):
    response = oauth_api.standalone_account_updater.get_updated_card_credentials(
        card_credentials_request(2030)
    )
    assert_updated_card_credentials_response(response)


@pytest.mark.skip(reason='Requires valid account updater credentials and live instrument data')
def test_should_get_updated_card_credentials_with_instrument(oauth_api):
    response = oauth_api.standalone_account_updater.get_updated_card_credentials(
        instrument_credentials_request('ins_v5rgkf3gdtpuzjqesyxmyodnya')
    )
    assert_updated_card_credentials_response(response)


def test_should_throw_on_invalid_card_request(oauth_api):
    with pytest.raises(CheckoutApiException):
        oauth_api.standalone_account_updater.get_updated_card_credentials(invalid_card_credentials_request())


def test_should_throw_422_on_standard_test_card(oauth_api):
    try:
        oauth_api.standalone_account_updater.get_updated_card_credentials(card_credentials_request(2026))
        pytest.fail()
    except CheckoutApiException as err:
        assert err.args[0] == 'The API response status code (422) does not indicate success.'

# common functions

def card_credentials_request(expiry_year: int) -> GetUpdatedCardCredentialsRequest:
    card = CardDetailsRequest()
    card.number = '4242424242424242'
    card.expiry_month = 12
    card.expiry_year = expiry_year

    source = SourceOptions()
    source.card = card

    request = GetUpdatedCardCredentialsRequest()
    request.source_options = source
    return request


def instrument_credentials_request(instrument_id: str) -> GetUpdatedCardCredentialsRequest:
    instrument = InstrumentReference()
    instrument.id = instrument_id

    source = SourceOptions()
    source.instrument = instrument

    request = GetUpdatedCardCredentialsRequest()
    request.source_options = source
    return request


def invalid_card_credentials_request() -> GetUpdatedCardCredentialsRequest:
    card = CardDetailsRequest()
    card.number = 'invalid_card_number'
    card.expiry_month = 13
    card.expiry_year = 2020

    source = SourceOptions()
    source.card = card

    request = GetUpdatedCardCredentialsRequest()
    request.source_options = source
    return request


def assert_updated_card_credentials_response(response):
    assert_response(response, 'http_metadata', 'account_update_status')