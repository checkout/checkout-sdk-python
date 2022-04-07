from __future__ import absolute_import

from enum import Enum

from checkout_sdk.common.common import Address, Phone, CustomerRequest


class SourceType(str, Enum):
    SEPA = 'sepa'


class MandateType(str, Enum):
    SINGLE = 'single'
    RECURRING = 'recurring'


class SourceRequest:
    reference: str
    phone: Phone
    customer: CustomerRequest

    def __init__(self, _type: SourceType):
        self.type = _type


class SourceData:
    first_name: str
    last_name: str
    account_iban: str
    bic: str
    billing_descriptor: str
    mandate_type: MandateType


class SepaSourceRequest(SourceRequest):
    billing_address: Address
    source_data: SourceData

    def __init__(self):
        super().__init__(SourceType.SEPA)
