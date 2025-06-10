from enum import Enum

from checkout_sdk.common.enums import Currency


class TransferType(str, Enum):
    COMMISSION = 'commission'
    PROMOTION = 'promotion'
    REFUND = 'refund'


class TransferSource:
    id: str
    amount: int
    currency: Currency


class TransferDestination:
    id: str


class CreateTransferRequest:
    reference: str
    transfer_type: TransferType
    source: TransferSource
    destination: TransferDestination
