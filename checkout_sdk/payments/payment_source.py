from checkout_sdk.common import DTO


class PaymentSource(DTO):
    def __init__(self, type):
        self.type = type
