from checkout_sdk.common import ApiResponse

from checkout_sdk import Utils


class PaymentResponse(ApiResponse):
    @property
    def id(self):
        return self._response.body['id']

    @property
    def requires_redirect(self):
        return Utils.verify_redirect_flow(self._response)
