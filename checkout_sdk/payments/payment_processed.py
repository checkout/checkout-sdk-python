from checkout_sdk.payments import PaymentActionResponse
from checkout_sdk.common import Customer, Card


class PaymentProcessed(PaymentActionResponse):
    def __init__(self, api_response):
        super().__init__(api_response)
        self._card = Card(api_response.body['card'])
        # customer name is not currently returned from an Auth response
        self._customer = Customer(
            id=api_response.body['card']['customerId'], email=api_response.body['email'])

    @property
    def charge_mode(self):
        return self._response.body['chargeMode']

    @property
    def auth_code(self):
        return self._response.body['authCode']

    @property
    def card(self):
        return self._card

    @property
    def customer(self):
        return self._customer
