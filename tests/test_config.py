import unittest
import os
import tests

from unittest import mock
from tests.base import CheckoutSdkTestCase
from checkout_sdk import Config


class ConfigTests(CheckoutSdkTestCase):
    def setUp(self):
        super().setUp()

    def test_os_env_secret_key_with_sandbox_as_default(self):
        config = Config()
        self.assertEqual(config.secret_key, os.environ['CKO_SECRET_KEY'])
        self.assertRegex(config.api_base_url, r'sandbox')

    def test_os_env_in_production(self):
        with mock.patch.dict('os.environ', {'CKO_SANDBOX': 'False'}):
            config = Config()
            self.assertEqual(config.secret_key, os.environ['CKO_SECRET_KEY'])
            self.assertNotRegex(config.api_base_url, r'sandbox')

    def test_secret_key_in_constructor_overrides_os_env(self):
        self.assertRaises(Exception, Config, secret_key='sk_invalid')
