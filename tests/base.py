import unittest
import os
import tests


class CheckoutSdkTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        os.environ['CKO_SECRET_KEY'] = tests.SECRET_KEY

    def tearDown(self):
        super().tearDown()
