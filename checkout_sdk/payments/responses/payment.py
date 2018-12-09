from checkout_sdk.common import Resource


class Payment(Resource):
    def __init__(self, api_response, is_pending):
        super().__init__(api_response)
        self._is_pending = is_pending

    @property
    def is_pending(self):
        return self._is_pending
