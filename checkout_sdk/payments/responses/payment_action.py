from checkout_sdk.common import Resource


class PaymentAction(Resource):
    @property
    def action_id(self):
        return self._response.body.get('action_id')

    @property
    def reference(self):
        return self._response.body.get('reference')
