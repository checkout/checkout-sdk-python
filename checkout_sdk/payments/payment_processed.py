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
    def card(self):
        return self._card

    @property
    def customer(self):
        return self._customer
