from __future__ import absolute_import

from enum import Enum

from checkout_sdk.common.common import Address, Phone


class TokenType(str, Enum):
    CARD = 'card'
    APPLE_PAY = 'applepay'
    GOOGLE_PAY = 'googlepay'
    CVV = 'cvv'
    PIN = 'pin'


class CardTokenRequest:
    type: TokenType
    number: str
    expiry_month: int
    expiry_year: int
    name: str
    cvv: str
    pin: str
    billing_address: Address
    phone: Phone

    def __init__(self):
        self.type = TokenType.CARD


class WalletTokenRequest:
    type: str

    def __init__(self, token_type: TokenType):
        self.type = token_type


class GooglePayTokenData:
    signature: str
    protocolVersion: str
    signedMessage: str


class GooglePayTokenRequest(WalletTokenRequest):
    token_data: GooglePayTokenData

    def __init__(self):
        super().__init__(TokenType.GOOGLE_PAY)


class ApplePayTokenData:
    version: str
    data: str
    signature: str
    header: dict


class ApplePayTokenRequest(WalletTokenRequest):
    token_data: ApplePayTokenData

    def __init__(self):
        super().__init__(TokenType.APPLE_PAY)


class CvvTokenData:
    cvv: str


class CvvTokenRequest:
    type: TokenType
    token_data: CvvTokenData

    def __init__(self):
        self.type = TokenType.CVV


class PinTokenData:
    pin: str


class PinTokenRequest:
    type: TokenType
    token_data: PinTokenData

    def __init__(self):
        self.type = TokenType.PIN
