from checkout_sdk.payments import PaymentResponse


class PaymentActionResponse(PaymentResponse):
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
    def response_code(self):
        return self._response.body['responseCode']

    @property
    def approved(self):
        return str(self.response_code).startswith('1')
