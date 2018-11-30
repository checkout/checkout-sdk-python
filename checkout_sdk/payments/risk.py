from checkout_sdk.common import RequestDTO


class Risk(RequestDTO):
    def __init__(self, enabled=False):
        self.enabled = enabled
