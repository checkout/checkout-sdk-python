from checkout_sdk import Config, HTTPClient
from checkout_sdk.payments import PaymentsClient

# pylint: disable=too-few-public-methods


class CheckoutApi:
    def __init__(self, **kwargs):
        http_client = HTTPClient(Config(**kwargs))
        self.payments = PaymentsClient(http_client)
