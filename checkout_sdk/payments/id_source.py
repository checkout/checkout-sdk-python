from checkout_sdk.payments import PaymentSource


class IdSource(PaymentSource):
    def __init__(self, id, **kwargs):
        super().__init__(type='id')
        self.id = id
        # create attributes for kwargs
        for (k, v) in kwargs.items():
            setattr(self, k, v)
