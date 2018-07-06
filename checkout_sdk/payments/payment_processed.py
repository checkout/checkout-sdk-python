from checkout_sdk.payments import PaymentResponse
from checkout_sdk.common import Customer, Card


class PaymentProcessed(PaymentResponse):
    def __init__(self, api_response):
        super().__init__(api_response)
        self._card = Card(api_response.body['card'])
        # customer name is not currently returned from an Auth response
        self._customer = Customer(
            id=api_response.body['card']['customerId'], email=api_response.body['email'])

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
    def card(self):
        return self._card

    @property
    def customer(self):
        return self._customer
