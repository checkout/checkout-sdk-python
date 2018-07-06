from checkout_sdk import HttpResponse


class PaymentResponse:
    def __init__(self, api_response):
        if not isinstance(api_response, HttpResponse):
            raise ValueError(
                'api_response must be a valid instance of APIResponse')
        self._response = api_response

    @property
    def http_response(self):
        """Http response with status, headers, JSON body and elapsed time (ms)."""
        return self._response

    @property
    def id(self):
        return self._response.body['id']

    @property
    def created(self):
        return self._response.body['created']

    @property
    def track_id(self):
        return self._response.body['trackId']

    @property
    def currency(self):
        return self._response.body['currency']

    @property
    def value(self):
        return self._response.body['value']

    @property
    def approved(self):
        return str(self._response.body['responseCode']).startswith('1')
