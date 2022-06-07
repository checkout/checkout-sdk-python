from __future__ import absolute_import

from enum import Enum

from checkout_sdk.common.common import Address
from checkout_sdk.common.enums import PaymentSourceType
from checkout_sdk.payments.payments_four import PaymentRequestSource


class TerminalType(str, Enum):
    APP = 'APP'
    WAP = 'WAP'
    WEB = 'WEB'


class OsType(str, Enum):
    ANDROID = 'ANDROID'
    IOS = 'IOS'


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


class RequestPayPalSource(PaymentRequestSource):

    def __init__(self):
        super().__init__(PaymentSourceType.PAYPAL)


class PaymentRequestWeChatPaySource(PaymentRequestSource):
    billing_address: Address

    def __init__(self):
        super().__init__(PaymentSourceType.WECHATPAY)


class RequestAlipayPlusHKSource(PaymentRequestSource):
    terminal_type: TerminalType = TerminalType.WEB
    os_type: OsType

    def __init__(self):
        super().__init__(PaymentSourceType.ALIPAY_HK)


class RequestAlipayPlusCNSource(PaymentRequestSource):
    terminal_type: TerminalType = TerminalType.WEB
    os_type: OsType

    def __init__(self):
        super().__init__(PaymentSourceType.ALIPAY_CN)


class RequestAlipayPlusGCashSource(PaymentRequestSource):
    terminal_type: TerminalType = TerminalType.WEB
    os_type: OsType

    def __init__(self):
        super().__init__(PaymentSourceType.GCASH)
