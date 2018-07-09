import unittest
import os
import tests

from checkout_sdk import logger


class CheckoutSdkTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        print('.....{}.....'.format(self._testMethodName))

    def tearDown(self):
        super().tearDown()
        print('\n')
