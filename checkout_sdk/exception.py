from __future__ import absolute_import

from checkout_sdk.authorization_type import AuthorizationType


class CheckoutException(Exception):

    def __init__(self, message=None):
        super(CheckoutException, self).__init__(message)


class CheckoutArgumentException(CheckoutException):
    pass


class CheckoutAuthorizationException(CheckoutException):

    def __init__(self, message=None):
        super(CheckoutAuthorizationException, self).__init__(message)

    @staticmethod
    def invalid_authorization(authorization_type: AuthorizationType):
        raise CheckoutAuthorizationException(
            'Operation requires ' + authorization_type.value[0] + ' authorization type')

    @staticmethod
    def invalid_key(key_type: AuthorizationType):
        raise CheckoutAuthorizationException('%s is required for this operation' % key_type.value[0])


class CheckoutApiException(CheckoutException):
    request_id: str
    http_status_code: int
    error_details: dict

    def __init__(self, request_id: str = None, http_status_code: int = None, error_details: dict = None):
        self.request_id = request_id
        self.http_status_code = http_status_code
        self.error_details = error_details
        super().__init__('The API response status code ({}) does not indicate success.'.format(http_status_code))
