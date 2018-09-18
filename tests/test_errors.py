import unittest
import os
import tests
import json

import checkout_sdk as sdk

from checkout_sdk import constants
from checkout_sdk import errors
from tests.base import CheckoutSdkTestCase


class ErrorsTests(CheckoutSdkTestCase):

    def test_init_api_error(self):
        api_error = errors.ApiError(
            message='api error',
            event_id='event_id',
            http_status=500,
            error_code=500,
            elapsed=100)
        self.assertEqual(api_error.message, 'api error')
        self.assertEqual(api_error.event_id, 'event_id')
        self.assertEqual(api_error.http_status, 500)
        self.assertEqual(api_error.error_code, 500)
        self.assertEqual(api_error.elapsed, 100)

        self.assertEqual(
            str(api_error), '{0.event_id} - {0.message}'.format(api_error))

    def test_init_bad_request_error(self):
        bad_request_error = errors.BadRequestError(
            message='bad request',
            error_code=constants.VALIDATION_ERROR_CODE
        )
        self.assertEqual(bad_request_error.message, 'bad request')
        self.assertTrue(bad_request_error.validation_error)

    def test_init_authentication_error(self):
        error = errors.AuthenticationError()
        self.assertIsNotNone(error.message)

    def test_init_resource_not_found_error(self):
        error = errors.ResourceNotFoundError()
        self.assertIsNotNone(error.message)

    def test_timeout_error(self):
        error = errors.Timeout()
        self.assertIsNotNone(error.message)

    def test_too_many_requests_error(self):
        error = errors.TooManyRequestsError()
        self.assertIsNotNone(error.message)
