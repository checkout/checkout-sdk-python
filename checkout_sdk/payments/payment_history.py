from checkout_sdk.common import ApiResponse
from checkout_sdk.common import Charge


class PaymentHistory(ApiResponse):
    def __init__(self, api_response):
        super().__init__(api_response)
        self._charges = [Charge(charge_data)
                         for charge_data in api_response.body['charges']]

    @property
    def charges(self):
        return self._charges
