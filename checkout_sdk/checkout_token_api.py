from checkout_sdk.vaults.tokens_client import TokensClient
from checkout_sdk import Config, HTTPClient, http_client


class CheckoutTokenApi:
    def __init__(self, **kwargs):
        http_client = HTTPClient(Config(**kwargs))
        self.tokens = TokensClient(http_client)

