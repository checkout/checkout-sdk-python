from dateutil import parser
from checkout_sdk.payments.responses import Payment, Customer, RiskAssessment


class PaymentProcessed(Payment):
    def __init__(self, api_response):
        print(api_response.body)
        super().__init__(api_response, is_pending=False)

        self._processed_on = parser.parse(
            self._response.body.get('processed_on'))

        customer = api_response.body.get('customer')
        self._customer = Customer(
            customer) if customer is not None else None

        risk = api_response.body.get('risk')
        self._risk = RiskAssessment(
            risk) if risk is not None else None

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

    @property
    def scheme_id(self):
        return self._response.body.get('scheme_id')

    @property
    def customer(self):
        return self._customer

    @property
    def risk(self):
        return self._risk
