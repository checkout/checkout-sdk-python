import pytest

from checkout_sdk.tokens.tokens import CardTokenRequest
from tests.checkout_test_utils import assert_response, address, phone


@pytest.mark.skip(reason='not available')
def test_should_create_card_token(previous_api):
    request = CardTokenRequest()
    request.number = '4242424242424242'
    request.expiry_month = 6
    request.expiry_year = 2025
    request.cvv = '100'
    request.name = 'Mr. Test'
    request.billing_address = address()
    request.phone = phone()

    response = previous_api.tokens.request_card_token(request)

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
