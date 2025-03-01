from __future__ import absolute_import

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
    error_details: list
    error_type: str

    def __init__(self, response):
        self.http_metadata = map_to_http_metadata(response)
        if response.text:
            try:
                payload = response.json()
                self.error_details = payload.get('error_codes')
                self.error_type = payload.get('error_type')
            except ValueError:
                self.error_details = None
                self.error_type = None
        else:
            self.error_details = None
            self.error_type = None
        super().__init__('The API response status code ({}) does not indicate success.'
                         .format(response.status_code))
