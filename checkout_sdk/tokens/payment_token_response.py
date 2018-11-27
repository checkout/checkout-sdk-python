from checkout_sdk.common import ApiResponse


class PaymentTokenResponse(ApiResponse):
    @property
    def id(self):
        return self._response.body['id']
