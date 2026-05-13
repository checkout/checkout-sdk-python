from enum import Enum

from checkout_sdk.common.common import QueryFilterDateRange


class TransactionStatus(str, Enum):
    AUTHORIZED = 'authorized'
    DECLINED = 'declined'
    CANCELED = 'canceled'
    CLEARED = 'cleared'
    REFUNDED = 'refunded'
    DISPUTED = 'disputed'


class TransactionsQueryFilter(QueryFilterDateRange):
    limit: int
    skip: int
    cardholder_id: str
    card_id: str
    entity_id: str
    status: TransactionStatus
