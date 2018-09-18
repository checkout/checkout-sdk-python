from checkout_sdk import constants


class CheckoutSdkError(Exception):
    def __init__(self, event_id=None, http_status=None, error_code=None, message=None, elapsed=0):
        super().__init__(message)
        self.event_id = event_id
        self.http_status = http_status
        self.error_code = error_code
        self.message = message
        self.elapsed = elapsed

    def __str__(self):
        return '{} - {}'.format(self.event_id, self.message)


class AuthenticationError(CheckoutSdkError):
    def __init__(self, **kwargs):
        message = kwargs.pop(
            'message', 'Authentication error. Secret key might be missing or expired.')
        super().__init__(message=message, **kwargs)


class BadRequestError(CheckoutSdkError):
    def __init__(self, **kwargs):
        message = kwargs.pop(
            'message', 'Bad request. Check for possible validation error.')
        super().__init__(message=message, **kwargs)

    @property
    def validation_error(self):
        return self.error_code == constants.VALIDATION_ERROR_CODE


class ResourceNotFoundError(CheckoutSdkError):
    def __init__(self, **kwargs):
        message = kwargs.pop(
            'message', 'Resource not found. Please check the identifier and retry.')
        super().__init__(message=message, **kwargs)


class Timeout(CheckoutSdkError):
    def __init__(self, **kwargs):
        message = kwargs.pop(
            'message', 'The request timed out. Considering adjust the "timeout" setting.')
        super().__init__(message=message, **kwargs)


class TooManyRequestsError(CheckoutSdkError):
    def __init__(self, **kwargs):
        message = kwargs.pop(
            'message', 'Requests blocked due to API request throttling.')
        super().__init__(message=message, **kwargs)


class ApiError(CheckoutSdkError):
    def __init__(self, **kwargs):
        message = kwargs.pop('message', 'General API error.')
        super().__init__(message=message, **kwargs)
