

class CheckoutSdkError(Exception):
    def __init__(self, request_id=None, api_version=None,
                 http_status=None, error_type=None, error_codes=None,
                 elapsed=0):
        super().__init__()
        self.request_id = request_id
        self.api_version = api_version
        self.http_status = http_status
        self.error_type = error_type
        self.error_codes = error_codes
        self.elapsed = elapsed

    def __str__(self):
        return '{} - {}'.format(self.request_id, self.error_type)


class AuthenticationError(CheckoutSdkError):
    pass


class ValidationError(CheckoutSdkError):
    pass


class ResourceNotFoundError(CheckoutSdkError):
    pass


class NotAllowedError(CheckoutSdkError):
    pass


class TooManyRequestsError(CheckoutSdkError):
    pass


class ApiError(CheckoutSdkError):
    pass


class ApiTimeoutError(CheckoutSdkError):
    pass
