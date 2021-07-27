from checkout_sdk.vaults.tokens_client import TokensClient
from checkout_sdk import Config, HTTPClient
from checkout_sdk.payments import PaymentsClient
from checkout_sdk.vaults import TokensClient

class CheckoutApi:
    def __init__(self, **kwargs):
        config = Config(**kwargs)
        http_client = HTTPClient(config)
        if(config.secret_key is not None):
            self.payments = PaymentsClient(http_client)
        if(config.public_key is not None):
            self.tokens = TokensClient(http_client)
