from enum import Enum

from checkout_sdk.common.enums import Currency


class TransactionType(str, Enum):
    PURCHASE = 'purchase'


class AuthorizationType(str, Enum):
    AUTHORIZATION = 'authorization'
    PRE_AUTHORIZATION = 'pre_authorization'


class CardSimulation:
    id: str
    expiry_month: int
    expiry_year: int


class Merchant:
    category_code: str


class TransactionSimulation:
    type: TransactionType
    amount: int
    currency: Currency
    merchant: Merchant
    authorization_type: AuthorizationType


class CardAuthorizationRequest:
    card: CardSimulation
    transaction: TransactionSimulation


class SimulationRequest:
    amount: int
