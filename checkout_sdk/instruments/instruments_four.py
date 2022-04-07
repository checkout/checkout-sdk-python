from enum import Enum

from checkout_sdk.common.common import Address, Phone
from checkout_sdk.common.common_four import BankDetails, UpdateCustomerRequest, AccountHolder
from checkout_sdk.common.enums import Currency, Country
from checkout_sdk.common.enums_four import AccountType, AccountHolderType
from checkout_sdk.instruments.instruments import InstrumentType


class InstrumentAccountHolder:
    billing_address: Address
    phone: Phone


# Create
class CreateCustomerInstrumentRequest:
    id: str
    email: str
    name: str
    phone: Phone
    default: bool


class CreateInstrumentRequest:
    type: InstrumentType
    customer: CreateCustomerInstrumentRequest

    def __init__(self, type_p: InstrumentType):
        self.type = type_p


class CreateTokenInstrumentRequest(CreateInstrumentRequest):
    token: str
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(InstrumentType.TOKEN)


class CreateBankAccountInstrumentRequest(CreateInstrumentRequest):
    account_type: AccountType
    account_number: str
    bank_code: str
    branch_code: str
    iban: str
    bban: str
    swift_bic: str
    currency: Currency
    processing_channel_id: str
    account_holder: AccountHolder
    bank_details: BankDetails

    def __init__(self):
        super().__init__(InstrumentType.BANK_ACCOUNT)


# Update
class UpdateInstrumentRequest:
    type: InstrumentType

    def __init__(self, type_p: InstrumentType):
        self.type = type_p


class UpdateTokenInstrumentRequest(UpdateInstrumentRequest):
    token: str

    def __init__(self):
        super().__init__(InstrumentType.TOKEN)


class UpdateCardInstrumentRequest(UpdateInstrumentRequest):
    expiry_month: int
    expiry_year: int
    name: str
    customer: UpdateCustomerRequest
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(InstrumentType.CARD)


class UpdateBankAccountInstrumentRequest(UpdateInstrumentRequest):
    account_type: AccountType
    account_number: str
    bank_code: str
    branch_code: str
    iban: str
    bban: str
    swift_bic: str
    currency: Currency
    country: Country
    processing_channel_id: str
    account_holder: AccountHolder
    bank_details: BankDetails
    customer: UpdateCustomerRequest

    def __init__(self):
        super().__init__(InstrumentType.BANK_ACCOUNT)


class PaymentNetwork(str, Enum):
    LOCAL = 'local'
    SEPA = 'sepa'
    FPS = 'Fps'
    ACH = 'Ach'
    FEDWIRE = 'Fedwire'
    SWIFT = 'Swift'


class BankAccountFieldQuery:
    account_holder_type: AccountHolderType
    payment_network: PaymentNetwork
