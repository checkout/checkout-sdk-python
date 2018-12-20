import checkout_sdk as sdk

from checkout_sdk.payments import PaymentResponse


class AlternativePaymentResponse(PaymentResponse):
    def __init__(self, api_response):
        super().__init__(api_response)

    @property
    def charge_mode(self):
        return self._response.body['chargeMode']

    @property
    def response_code(self):
        return self._response.body['responseCode']

    @property
    def redirect_url(self):
        return self._response.body['localPayment'].get('paymentUrl')
