import unittest
import os
import tests
import json

import checkout_sdk as sdk

from checkout_sdk import HttpClient, Config, Utils
from checkout_sdk.tokens import TokensClient, PaymentTokenResponse
from tests.base import CheckoutSdkTestCase
from enum import Enum


class TokensClientTests(CheckoutSdkTestCase):
    def setUp(self):
        super().setUp()
        self.http_client = HttpClient(Config())
        self.client = TokensClient(self.http_client)

    def tearDown(self):
        super().tearDown()
        self.http_client.close_session()

    def test_bad_payment_token_response_init(self):
        with self.assertRaises(TypeError):
            PaymentTokenResponse(False)

    def test_tokens_client_payment_token_request(self):
        token = self.client.request_payment_token(
            value=100,                  # cents
            currency=sdk.Currency.USD   # or 'usd'
        )

        self.assertEqual(token.http_response.status, 200)

        # test payment
        self.assertIsNotNone(token.id)
