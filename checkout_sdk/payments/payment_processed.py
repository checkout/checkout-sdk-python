from checkout_sdk import ApiResponse
from checkout_sdk.common import Customer, Card


class PaymentProcessed:
    def __init__(self, api_response):
        if not isinstance(api_response, ApiResponse):
            raise ValueError(
                'api_response must be a valid instance of APIResponse')
        self._card = Card(api_response.body['card'])
        # customer name is not currently returned from the API
        self._customer = Customer(
            id=api_response.body['card']['customerId'], email=api_response.body['email'])
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
    def approved(self):
        return str(self._response.body['responseCode']).startswith('1')

    @property
    def currency(self):
        return self._response.body['currency']

    @property
    def value(self):
        return self._response.body['value']

    @property
    def track_id(self):
        return self._response.body['trackId']

    @property
    def card(self):
        return self._card

    @property
    def customer(self):
        return self._customer
