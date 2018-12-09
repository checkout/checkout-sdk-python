from checkout_sdk.payments.responses import Payment


class PaymentPending(Payment):
    def __init__(self, api_response):
        super().__init__(api_response, is_pending=True)

    @property
    def requires_redirect(self):
        return self.has_link('redirect')

    @property
    def redirect_link(self):
        return self.get_link('redirect')
