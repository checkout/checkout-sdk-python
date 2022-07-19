from checkout_sdk.common.common import Address, CustomerRequest, Phone
from checkout_sdk.common.enums import InstrumentType


class InstrumentAccountHolder:
    billing_address: Address
    phone: Phone


class InstrumentCustomerRequest(CustomerRequest):
    default: bool
    phone: Phone


class CreateInstrumentRequest:
    type: InstrumentType
    token: str
    account_holder: InstrumentAccountHolder
    customer: InstrumentCustomerRequest

    def __init__(self):
        self.type = InstrumentType.TOKEN


class UpdateInstrumentCustomer:
    id: str
    default: bool


class UpdateInstrumentRequest:
    expiry_month: int
    expiry_year: int
    name: str
    account_holder: InstrumentAccountHolder
    customer: UpdateInstrumentCustomer
