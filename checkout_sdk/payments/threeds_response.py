import checkout_sdk as sdk

from checkout_sdk.payments import PaymentResponse


class ThreeDSResponse(PaymentResponse):
    def __init__(self, api_response):
        super().__init__(api_response)

    @property
    def charge_mode(self):
        return self._response.body['chargeMode']

    @property
    def track_id(self):
        return self._response.body['trackId']

    @property
    def response_code(self):
        return self._response.body['responseCode']

    @property
    def enrolled(self):
        return self._response.body['enrolled'] == 'Y'

    @property
    def redirect_url(self):
        return self._response.body['redirectUrl']

    @property
    def downgraded(self):
        return self.charge_mode == sdk.ChargeMode.NonThreeD.value  # pylint: disable = no-member
