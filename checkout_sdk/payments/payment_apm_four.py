from __future__ import absolute_import

from checkout_sdk.common.common import Address
from checkout_sdk.common.enums import PaymentSourceType
from checkout_sdk.payments.payments_four import PaymentRequestSource


class RequestIdealSource(PaymentRequestSource):
    bic: str
    description: str
    language: str

    def __init__(self):
        super().__init__(PaymentSourceType.IDEAL)


class RequestSofortSource(PaymentRequestSource):

    def __init__(self):
        super().__init__(PaymentSourceType.SOFORT)


class RequestTamaraSource(PaymentRequestSource):
    billing_address: Address

    def __init__(self):
        super().__init__(PaymentSourceType.TAMARA)
