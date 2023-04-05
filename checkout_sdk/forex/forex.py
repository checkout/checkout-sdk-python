from enum import Enum

from checkout_sdk.common.enums import Currency


class ForexSource(str, Enum):
    VISA = 'visa'
    MASTERCARD = 'mastercard'


class QuoteRequest:
    source_currency: Currency
    source_amount: int
    destination_currency: Currency
    destination_amount: int
    process_channel_id: str


class RatesQueryFilter:
    product: str
    source: ForexSource
    currency_pairs: str
    process_channel_id: str
