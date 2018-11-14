from checkout_sdk.common import RequestDTO


class PaymentSource(RequestDTO):
    def __init__(self, type):
        self.type = type
