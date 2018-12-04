import checkout_sdk as sdk

from checkout_sdk import errors
from tests.base import CheckoutSdkTestCase


class ErrorsTests(CheckoutSdkTestCase):

    def test_init_api_error(self):
        api_error = errors.ApiError(
            request_id='request_id',
            api_version='1.0',
            http_status=500,
            error_type='error_type',
            error_codes=['code'],
            elapsed=100)
        self.assertEqual(api_error.request_id, 'request_id')
        self.assertEqual(api_error.api_version, '1.0')
        self.assertEqual(api_error.http_status, 500)
        self.assertEqual(api_error.error_type, 'error_type')
        self.assertEqual(api_error.error_codes, ['code'])
        self.assertEqual(api_error.elapsed, 100)

        self.assertEqual(
            str(api_error), '{0.request_id} - {0.error_type}'.format(api_error))
