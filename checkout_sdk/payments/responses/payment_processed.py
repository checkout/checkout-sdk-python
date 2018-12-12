from checkout_sdk.payments.responses import Payment


class PaymentProcessed(Payment):
    def __init__(self, api_response):
        super().__init__(api_response, is_pending=False)

    @property
    def actions_link(self):
        return self.get_link('actions')

    @property
    def can_capture(self):
        return self.has_link('capture')

    @property
    def capture_link(self):
        return self.get_link('capture')

    @property
    def can_void(self):
        return self.has_link('void')

    @property
    def void_link(self):
        return self.get_link('void')

    @property
    def can_refund(self):
        return self.has_link('refund')

    @property
    def refund_link(self):
        return self.get_link('refund')
