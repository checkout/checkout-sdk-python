from __future__ import absolute_import

import logging

from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.utils import map_to_http_metadata


class CheckoutException(Exception):

    def __init__(self, message=None):
        if message is None:
            message = ""
        super().__init__(message)


class CheckoutArgumentException(CheckoutException):
    pass


class CheckoutAuthorizationException(CheckoutException):

    def __init__(self, message=None):
        super().__init__(message)

    @staticmethod
    def invalid_authorization(authorization_type: AuthorizationType):
        raise CheckoutAuthorizationException(
            'Operation requires ' + authorization_type.name + ' authorization type')

    @staticmethod
    def invalid_key(key_type: AuthorizationType):
        raise CheckoutAuthorizationException('%s is required for this operation' % key_type.name)


class CheckoutApiException(CheckoutException):
    http_metadata: dict
    request_id: str
    error_details: list
    error_type: str

    def __init__(self, response):
        self.http_metadata = map_to_http_metadata(response)
        self.request_id = None
        self.error_details = None
        self.error_type = None

        if response.text:
            try:
                payload = response.json()
                self.request_id = payload.get('request_id')
                self.error_details = payload.get('error_codes')
                self.error_type = payload.get('error_type')
            except (ValueError, KeyError, TypeError) as e:
                logging.error("Failed to parse response JSON payload: %s", e)

        if not self.request_id:
            self.request_id = response.headers.get('Cko-Request-Id')

        super().__init__('The API response status code ({}) does not indicate success.'
                         .format(response.status_code))
