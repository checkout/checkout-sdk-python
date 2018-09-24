from checkout_sdk import HttpResponse

from checkout_sdk import Utils


class PaymentResponse:
    def __init__(self, api_response):
        if not isinstance(api_response, HttpResponse):
            raise TypeError(
                'api_response must be a valid instance of HttpResponse')
        self._response = api_response

    @property
    def http_response(self):
        """Http response with status, headers, JSON body and elapsed time (ms)."""
        return self._response

    @property
    def id(self):
        return self._response.body['id']

    @property
    def requires_redirect(self):
        return Utils.verify_redirect_flow(self._response)
