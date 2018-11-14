from dateutil import parser
from checkout_sdk.payments.responses import Payment


class PaymentProcessed(Payment):
    def __init__(self, api_response):
        super().__init__(api_response)

        self._processed_on = parser.parse(
            self._response.body.get('processed_on'))

    @property
    def action_id(self):
        return self._response.body.get('action_id')

    @property
    def processed_on(self):
        return self._processed_on

    @property
    def amount(self):
        return self._response.body.get('amount')

    @property
    def currency(self):
        return self._response.body.get('currency')

    @property
    def approved(self):
        return self._response.body.get('approved')

    @property
    def auth_code(self):
        return self._response.body.get('auth_code')

    @property
    def response_code(self):
        return self._response.body.get('response_code')

    @property
    def response_summary(self):
        return self._response.body.get('response_summary')
