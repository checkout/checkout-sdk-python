from checkout_sdk.payments import PaymentActionResponse
from checkout_sdk.common import Charge


class PaymentHistory(PaymentActionResponse):
    def __init__(self, api_response):
        super().__init__(api_response)
        self._charges = [Charge(charge_data) for charge_data in api_response.body['charges']]

    @property
    def charges(self):
        return self._charges
