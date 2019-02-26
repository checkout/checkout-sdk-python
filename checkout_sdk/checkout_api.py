from checkout_sdk import Config, HttpClient
from checkout_sdk.payments import PaymentsClient
from checkout_sdk.tokens import TokensClient
from checkout_sdk.cards import CardsClient


class CheckoutApi:
    def __init__(self, **kwargs):
        http_client = HttpClient(Config(**kwargs))
        self.payments = PaymentsClient(http_client)
        self.tokens = TokensClient(http_client)
        self.cards = CardsClient(http_client)
