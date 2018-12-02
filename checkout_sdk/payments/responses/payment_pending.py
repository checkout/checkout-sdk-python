from checkout_sdk.payments.responses import Payment, Customer, ThreeDSEnrollment


class PaymentPending(Payment):
    def __init__(self, api_response):
        super().__init__(api_response, is_pending=True)

        customer = api_response.body.get('customer')
        self._customer = Customer(
            customer) if customer is not None else None

        threeds = api_response.body.get('3ds')
        self._threeds = ThreeDSEnrollment(
            threeds) if threeds is not None else None

    @property
    def customer(self):
        return self._customer

    @property
    def threeds(self):
        return self._threeds

    @property
    def requires_redirect(self):
        return self.has_link('redirect')

    @property
    def redirect_link(self):
        return self.get_link('redirect')
