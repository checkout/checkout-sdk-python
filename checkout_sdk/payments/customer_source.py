from checkout_sdk.payments import PaymentSource


class CustomerSource(PaymentSource):
    def __init__(self, id=None, email=None):
        super().__init__(type='customer')
        self.id = id
        self.email = email
