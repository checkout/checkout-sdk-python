import os
import checkout_sdk as sdk
from checkout_sdk import HTTPClient, Config
from checkout_sdk.vaults import (
    ExchangeClient,
    TokensClient,
    InstrumentsClient
)
from datetime import datetime

from tests.base import CheckoutSdkTestCase

class ExchangeClientTests(CheckoutSdkTestCase):
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
    CURRENCY='usd'
    AMOUNT=100
    PROVIDER='checkout'

    def setUp(self):
        super().setUp()
        self.http_client = HTTPClient(Config())
        self.client = ExchangeClient(self.http_client)
        self.token_client = TokensClient(self.http_client)
        self.instrument_client = InstrumentsClient(self.http_client)
    
    def tearDown(self):
        super().tearDown()
        self.http_client.close_session()

    def test_payments_vault_exchange_client_source(self):
        tokenDTO = self._token_card()
        instrument = self._get_card_source(tokenDTO.token)
        source = {
            'type': 'card',
            'number': '{{source.number}}',
            'expiry_month': '{{source.expiry_month}}',
            'expiry_year': '{{source.expiry_year}}',
            'name': '{{source.name}}',
            'cvv': self.CARD_CVV
        }

        headers = {
            'cko-provider': self.PROVIDER,
            'cko-source-id': instrument.id,
            'cko-authorization': os.environ['CKO_SECRET_KEY'],
            'authorization': os.environ['CKO_SECRET_KEY']
        }

        requestDTO = {
            'headers': headers,
            'source': source,
            'amount': self.AMOUNT,
            'currency': self.CURRENCY,
        }
        payment = self.client.request('payments',requestDTO)
        self.assertTrue(payment.approved)
        self.assertEqual(payment.amount, self.AMOUNT)
    
    def _token_card(self, dict_format=False):
        if dict_format:
            return self.token_client.request({
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
            return self.token_client.request(
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
    
    def _get_card_source(self, token):
        return self.instrument_client.create({
            'type': 'token',
            'token': token
        })
