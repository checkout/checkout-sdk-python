from checkout_sdk.common.enums import Currency


class QuoteRequest:
    source_currency: Currency
    source_amount: int
    destination_currency: Currency
    destination_amount: int
    process_channel_id: str
