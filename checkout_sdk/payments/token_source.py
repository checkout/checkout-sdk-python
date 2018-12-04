from checkout_sdk.payments import PaymentSource
from checkout_sdk.common import RequestDTO


class TokenSource(PaymentSource):
    def __init__(self, token, billing_address=None, phone=None):
        super().__init__(type='token')
        self.token = token
        self.billing_address = billing_address
        self.phone = phone

   # Dictionary to produce the JSON output

    def get_dict(self):
        return self._get_dict_extended(['billing_address', 'phone'])
