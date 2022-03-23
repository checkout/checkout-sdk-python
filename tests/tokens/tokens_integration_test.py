from checkout_sdk.tokens.tokens import CardTokenRequest
from tests.checkout_test_utils import assert_response, address, phone


def test_should_create_card_token(default_api):
    request = CardTokenRequest()
    request.number = '4242424242424242'
    request.expiry_month = 6
    request.expiry_year = 2025
    request.cvv = '100'
    request.name = 'Mr. Test'
    request.billing_address = address()
    request.phone = phone()

    response = default_api.tokens.request_card_token(request)

    assert_response(response,
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
