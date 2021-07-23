import checkout_sdk as sdk
from checkout_sdk import HTTPClient, Config
from checkout_sdk.vaults import TokensClient
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

    def test_tokens_googlepay_request_token(self):
        response = self._token_googlepay()
        self.assertIsNotNone(response)
        self._assert_token_is_valid(response)
        self._assert_googlepay_card_detail_is_valid(response)

    def _token_googlepay(self):
        return self.client.request({
            'type': 'googlepay',
            'token_data': {"signature":"MEYCIQD3eo6sNYma/3AlHJAMKAWL5fuFLDneNS/NYA76G1llogIhAITiWjCUVKqdLu9DbcMT07UCkJu0jQVeeYaQyIEvTt34","protocolVersion":"ECv1","signedMessage":"{\"encryptedMessage\":\"62QcuerFKu5UpezCr6DkeG+Y1+P73QSM3PT+3zywy3I0H9/UwOAm1WQ96XMUXBS1875ZjXHmq2hFo7BBlETo4+p2dcMcRpEdvQpyDsP4Q9P12fOKwKSmDLRdJ1BHfiySRpxgK6xoccqamjQfQAJ74UrRL8aWOL988dDeD8Kg45cVxgTLy2YW2e1l2St6CvFtmvo2DjRumHJomjpB7zPI71QUJI1MvSD334ueJbbaVJNtYSu7yRg9n0oHxu9HWqt7zY2GagPaKTHzN71mt+ljwJJH6uLHdhtBKnnUhshnkOkWT7xEgyNj9ss11wuhWKHxWJx6jUvHeDzZJtE8ZMU5z0IbWVnhSlE7lpfLNT0usIK2zC+6MgwcJL5ifAC6+yxmlnlFTW8hiPKfFkJXF5VaWf2NU571VvbaDZ541w6pPgcR+AsqOISh1xSeF6KDc9W0b5N14sUfnj697PEa/JvFGEzFqTpd7qSyNvflllHKoE5xlJ1obp6f\",\"ephemeralPublicKey\":\"BErw3xVh6CVmnI3E3qp27oSR9dlAGXqAqerWoSoOfuTs7Wkzf4MPEYJxc8+ygEeiq1bpDEeemVkSt8+hlrjo/oM\\u003d\",\"tag\":\"trpgr9jJvoEEMJ6mSfTbbS9qHoiDMjm1IAn2kFMo8Q8\\u003d\"}"}
        })

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
        expires_on = datetime.strptime(response.expires_on, '%Y-%m-%dT%H:%M:%SZ')
        self.assertGreater(datetime.now(), expires_on)
    
    def _assert_card_detail_is_valid(self, response):
        self.assertEqual(response.type, self.TYPE)
        self.assertEqual(response.expiry_month, self.CARD_EXPIRY_MONTH)
        self.assertEqual(response.expiry_year, self.CARD_EXPIRY_YEAR)
    
    def _assert_googlepay_card_detail_is_valid(self, response):
        self.assertEqual(response.type, 'googlepay')
        self.assertEqual(response.last4, '1111')
        self.assertEqual(response.expiry_month, 12)
        self.assertEqual(response.expiry_year, 2026)