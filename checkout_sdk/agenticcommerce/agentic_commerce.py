from __future__ import absolute_import

from enum import Enum
from typing import List, Dict
from datetime import datetime

from checkout_sdk.common.enums import Country, Currency


class DelegatedPaymentMethodType(str, Enum):
    CARD = 'card'


class DelegatedCardNumberType(str, Enum):
    FPAN = 'fpan'
    NETWORK_TOKEN = 'network_token'


class DelegatedPaymentAllowanceReason(str, Enum):
    ONE_TIME = 'one_time'


class DelegatedCardFundingType(str, Enum):
    CREDIT = 'credit'
    DEBIT = 'debit'
    PREPAID = 'prepaid'


class DelegatedPaymentMethodCard:
    type: DelegatedPaymentMethodType
    card_number_type: DelegatedCardNumberType
    number: str
    exp_month: str = None
    exp_year: str = None
    name: str = None
    cvc: str = None
    cryptogram: str = None
    eci_value: str = None
    checks_performed: List[str] = None
    iin: str = None
    display_card_funding_type: DelegatedCardFundingType = None
    display_wallet_type: str = None
    display_brand: str = None
    display_last4: str = None
    metadata: Dict[str, str] = None

    def __init__(self):
        self.type = DelegatedPaymentMethodType.CARD


class DelegatedPaymentAllowance:
    reason: DelegatedPaymentAllowanceReason
    max_amount: int
    currency: Currency
    merchant_id: str
    checkout_session_id: str
    expires_at: datetime


class DelegatedPaymentBillingAddress:
    name: str
    line_one: str
    line_two: str = None
    city: str
    state: str = None
    postal_code: str
    country: Country


class DelegatedPaymentRiskSignal:
    type: str
    score: int
    action: str


class DelegatedPaymentRequest:
    payment_method: DelegatedPaymentMethodCard
    allowance: DelegatedPaymentAllowance
    billing_address: DelegatedPaymentBillingAddress = None
    risk_signals: List[DelegatedPaymentRiskSignal]
    metadata: Dict[str, str]


class DelegatedPaymentHeaders:
    signature: str
    timestamp: str
    api_version: str

    def get_header_mappings(self) -> Dict[str, str]:
        return {
            'api_version': 'API-Version'
        }
