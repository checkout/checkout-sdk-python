from checkout_sdk.common import Resource

from checkout_sdk import Utils


class Payment(Resource):
    @property
    def id(self):
        return self._response.body.get('id')

    @property
    def reference(self):
        return self._response.body.get('reference')

    @property
    def status(self):
        return self._response.body.get('status')

    @property
    def is_pending(self):
        return Utils.is_pending_flow(self._response)
