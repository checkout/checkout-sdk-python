from __future__ import absolute_import

from checkout_sdk.authorization_type import AuthorizationType


class CheckoutException(Exception):

    def __init__(self, message=None):
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
    http_status_code: int
    http_response: dict
    request_id: str
    error_details: dict

    def __init__(self, response):
        self.http_status_code = response.status_code
        self.http_response = response
        if response.text:
            payload = response.json()
            self.request_id = payload['request_id'] if 'request_id' in payload else None
            self.error_details = payload['error_codes'] if 'error_codes' in payload else None
        super().__init__('The API response status code ({}) does not indicate success.'
                         .format(response.status_code))
