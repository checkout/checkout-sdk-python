from checkout_sdk import Config, HTTPClient
from checkout_sdk.payments import PaymentsClient


class CheckoutApi:
    def __init__(self, **kwargs):
        http_client = HTTPClient(Config(**kwargs))
        self.payments = PaymentsClient(http_client)
