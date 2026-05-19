from __future__ import absolute_import

from enum import Enum

from checkout_sdk.common.enums import PaymentSourceType


class NetworkTokenTransactionType(str, Enum):
    ECOM = 'ecom'
    RECURRING = 'recurring'
    POS = 'pos'
    AFT = 'aft'


class NetworkTokenInitiatedBy(str, Enum):
    CARDHOLDER = 'cardholder'
    TOKEN_REQUESTOR = 'token_requestor'


class NetworkTokenDeleteReason(str, Enum):
    FRAUD = 'fraud'
    OTHER = 'other'


# Network Token Request Source
class NetworkTokenRequestSource:
    type: PaymentSourceType

    def __init__(self, type_p: PaymentSourceType):
        self.type = type_p


class NetworkTokenRequestCardSource(NetworkTokenRequestSource):
    number: str
    expiry_month: str
    expiry_year: str
    cvv: str

    def __init__(self):
        super().__init__(PaymentSourceType.CARD)


class NetworkTokenRequestIdSource(NetworkTokenRequestSource):
    id: str

    def __init__(self):
        super().__init__(PaymentSourceType.ID)


# Provision Network Token
class ProvisionNetworkTokenRequest:
    source: NetworkTokenRequestSource


# Provision Cryptogram
class RequestCryptogramRequest:
    transaction_type: NetworkTokenTransactionType


# Delete Network Token
class DeleteNetworkTokenRequest:
    initiated_by: NetworkTokenInitiatedBy
    reason: NetworkTokenDeleteReason
