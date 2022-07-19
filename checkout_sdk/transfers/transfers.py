from enum import Enum


class TransferType(str, Enum):
    COMMISSION = 'commission'
    PROMOTION = 'promotion'
    REFUND = 'refund'


class TransferSource:
    id: str
    amount: int


class TransferDestination:
    id: str


class CreateTransferRequest:
    reference: str
    transfer_type: TransferType
    source: TransferSource
    destination: TransferDestination
