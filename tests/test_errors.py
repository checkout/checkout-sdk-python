import unittest
import os
import tests
import json

import checkout_sdk as sdk

from checkout_sdk import errors
from tests.base import CheckoutSdkTestCase


class ErrorsTests(CheckoutSdkTestCase):

    def test_init_api_error(self):
        auth_error = errors.AuthenticationError(
            message='api error',
            event_id='event_id',
            http_status=500,
            error_code=500,
            elapsed=100)
        self.assertEqual(auth_error.message, 'api error')
        self.assertEqual(auth_error.event_id, 'event_id')
        self.assertEqual(auth_error.http_status, 500)
        self.assertEqual(auth_error.error_code, 500)
        self.assertEqual(auth_error.elapsed, 100)

        self.assertEqual(str(auth_error), 'event_id' + ' - ' + 'api error')
