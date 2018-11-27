from checkout_sdk.common import HttpResponse


class ApiResponse:
    def __init__(self, response):
        if not isinstance(response, HttpResponse):
            raise TypeError(
                'response must be a valid instance of HttpResponse')
        self._response = response

    @property
    def http_response(self):
        """Http response with status, headers, JSON body and elapsed time (ms)."""
        return self._response
