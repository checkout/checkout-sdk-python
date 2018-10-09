from checkout_sdk.common import DTO
from checkout_sdk.payments import PaymentSource


class CardSource(PaymentSource):
    def __init__(self, number, expiry_month, expiry_year, cvv=None,
                 name=None, billing_address=None, phone=None):
        super().__init__(type='card')
        self.number = number
        self.expiry_month = expiry_month
        self.expiry_year = expiry_year
        self.cvv = cvv
        self.name = name
        self.billing_address = billing_address
        self.phone = phone

    # Dictionary to produce the JSON output

    def get_dict(self):
        return {
            **self.__dict__,
            'billing_address': self.billing_address.get_dict() if isinstance(self.billing_address, DTO) else self.billing_address,
            'phone': self.phone.get_dict() if isinstance(self.phone, DTO) else self.phone
        }
