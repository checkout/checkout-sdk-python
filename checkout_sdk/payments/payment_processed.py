from checkout_sdk.payments import PaymentActionResponse
from checkout_sdk.common import Card


class PaymentProcessed(PaymentActionResponse):
    def __init__(self, api_response):
        super().__init__(api_response)

    @property
    def charge_mode(self):
        return self._response.body['chargeMode']

    @property
    def auth_code(self):
        return self._response.body['authCode']

    """
    @property
    def customer(self):
        return self._customer
    """
