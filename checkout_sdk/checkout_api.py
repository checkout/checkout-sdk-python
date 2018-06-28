from checkout_sdk import Config, HttpClient
from checkout_sdk.payments import PaymentsClient


class CheckoutApi:
    def __init__(self, **kwargs):
        http_client = HttpClient(Config(**kwargs))
        self.payments = PaymentsClient(http_client)
