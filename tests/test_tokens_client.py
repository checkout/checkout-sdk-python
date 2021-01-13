import os
import checkout_sdk as sdk
from checkout_sdk import HTTPClient, Config
from checkout_sdk.tokens import TokensClient
from datetime import datetime

from tests.base import CheckoutSdkTestCase

class TokensClientTests(CheckoutSdkTestCase):
    CUSTOMER_NAME = 'John Doe'
    CARD_NUMBER = '4242424242424242'
    CARD_EXPIRY_MONTH = 9
    CARD_EXPIRY_YEAR = 2025
    CARD_CVV = '100'
    BILLING_LINE_1 = '1 New Street'
    BILLING_CITY = 'London'
    BILLING_ZIP = 'W1'
    BILLING_COUNTRY = 'GB'
    PHONE_COUNTRY_CODE = '+44'
    PHONE_NUMBER = '02999999999'
    TYPE='card'

    def setUp(self):
        super().setUp()
        self.http_client = HTTPClient(Config())
        self.client = TokensClient(self.http_client)
    
    def tearDown(self):
        super().tearDown()
        self.http_client.close_session()

    def test_tokens_request_token_with_kwargs(self):
        response = self._token_card()
        self.assertIsNotNone(response)
        self._assert_token_is_valid(response)
        self._assert_card_detail_is_valid(response)

    def test_tokens_request_token_with_dict(self):
        response = self._token_card(True)
        self.assertIsNotNone(response)
        self._assert_token_is_valid(response)
        self._assert_card_detail_is_valid(response)
    
    def _token_card(self, dict_format=False):
        if dict_format:
            return self.client.request({
            'type': self.TYPE,
            'number': self.CARD_NUMBER,
            'expiry_month': self.CARD_EXPIRY_MONTH,
            'expiry_year': self.CARD_EXPIRY_YEAR,
            'cvv': self.CARD_CVV,
            'billing_address': {
                'address_line1': self.BILLING_LINE_1,
                'city': self.BILLING_CITY,
                'zip': self.BILLING_ZIP,
                'country': self.BILLING_COUNTRY
            },
            'phone': {
                'country_code': self.PHONE_COUNTRY_CODE,
                'number': self.PHONE_NUMBER
            }
        })
        else:
            return self.client.request(
                type=self.TYPE,
                number=self.CARD_NUMBER,
                expiry_month=self.CARD_EXPIRY_MONTH,
                expiry_year=self.CARD_EXPIRY_YEAR,
                cvv=self.CARD_CVV,
                billing_address={
                    'address_line1': self.BILLING_LINE_1,
                    'city': self.BILLING_CITY,
                    'zip': self.BILLING_ZIP,
                    'country': self.BILLING_COUNTRY
                },
                phone={
                    'country_code': self.PHONE_COUNTRY_CODE,
                    'number': self.PHONE_NUMBER
                }
            )

    def _assert_token_is_valid(self, response):
        self.assertIsNotNone(response.token)
        expires_on = datetime.strptime(response.expires_on, '%Y-%m-%dT%H:%M:%SZ')
        self.assertGreater(datetime.now(), expires_on)
    
    def _assert_card_detail_is_valid(self, response):
        self.assertEqual(response.type, self.TYPE)
        self.assertEqual(response.expiry_month, self.CARD_EXPIRY_MONTH)
        self.assertEqual(response.expiry_year, self.CARD_EXPIRY_YEAR)
        