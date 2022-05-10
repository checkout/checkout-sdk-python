from checkout_sdk.tokens.tokens import CardTokenRequest
from tests.checkout_test_utils import assert_response, address, phone, VisaCard


def test_should_create_card_token(four_api):
    card_token_request = CardTokenRequest()
    card_token_request.name = VisaCard.name
    card_token_request.number = VisaCard.number
    card_token_request.expiry_year = VisaCard.expiry_year
    card_token_request.expiry_month = VisaCard.expiry_month
    card_token_request.cvv = VisaCard.cvv
    card_token_request.billing_address = address()
    card_token_request.phone = phone()

    response = four_api.tokens.request_card_token(card_token_request)

    assert_response(response,
                    'http_metadata',
                    'token',
                    'type',
                    'expires_on',
                    'expiry_month',
                    'expiry_year',
                    'name',
                    'scheme',
                    'last4',
                    'bin',
                    'card_type',
                    'card_category',
                    # 'issuer',
                    'issuer_country',
                    'product_id',
                    'product_type')
