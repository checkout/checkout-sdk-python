from __future__ import absolute_import

from checkout_sdk.metadata.metadata import CardMetadataRequest, CardMetadataBinSource, CardMetadataCardSource, \
    CardMetadataTokenSource, CardMetadataFormatType
from checkout_sdk.tokens.tokens import CardTokenRequest
from tests.checkout_test_utils import assert_response, VisaCard, address, phone


def test_should_request_card_metadata_for_bin(oauth_api):
    card_metadata_bin_source = CardMetadataBinSource()
    card_metadata_bin_source.bin = '42424242'

    card_metadata_request = CardMetadataRequest()
    card_metadata_request.source = card_metadata_bin_source
    card_metadata_request.format = CardMetadataFormatType.BASIC

    response = oauth_api.card_metadata.request_card_metadata(card_metadata_request)
    assert_response(response,
                    'http_metadata',
                    'bin',
                    'scheme',
                    'card_type',
                    'card_category',
                    'issuer_country',
                    'issuer_country_name',
                    'product_id',
                    'product_type')
    assert response.bin == '42424242'


def test_should_request_card_metadata_for_card(oauth_api):
    card_metadata_card_source = CardMetadataCardSource()
    card_metadata_card_source.number = '4242424242424242'

    card_metadata_request = CardMetadataRequest()
    card_metadata_request.source = card_metadata_card_source
    card_metadata_request.format = CardMetadataFormatType.BASIC

    response = oauth_api.card_metadata.request_card_metadata(card_metadata_request)
    assert_response(response,
                    'http_metadata',
                    'bin',
                    'scheme',
                    'card_type',
                    'card_category',
                    'issuer_country',
                    'issuer_country_name',
                    'product_id',
                    'product_type')
    assert response.bin == '42424242'


def test_should_request_card_metadata_for_token(oauth_api, default_api):
    card_metadata_token_source = CardMetadataTokenSource()
    card_metadata_token_source.token = request_card_token(default_api)

    card_metadata_request = CardMetadataRequest()
    card_metadata_request.source = card_metadata_token_source
    card_metadata_request.format = CardMetadataFormatType.BASIC

    response = oauth_api.card_metadata.request_card_metadata(card_metadata_request)
    assert_response(response,
                    'http_metadata',
                    'bin',
                    'scheme',
                    'card_type',
                    'card_category',
                    'issuer_country',
                    'issuer_country_name',
                    'product_id',
                    'product_type')
    assert response.bin == '42424242'


def request_card_token(default_api):
    card_token_request = CardTokenRequest()
    card_token_request.name = VisaCard.name
    card_token_request.number = VisaCard.number
    card_token_request.expiry_year = VisaCard.expiry_year
    card_token_request.expiry_month = VisaCard.expiry_month
    card_token_request.cvv = VisaCard.cvv
    card_token_request.billing_address = address()
    card_token_request.phone = phone()

    card_token_response = default_api.tokens.request_card_token(card_token_request)
    assert_response(card_token_response, 'token')

    return card_token_response.token
