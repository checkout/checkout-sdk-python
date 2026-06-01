from datetime import datetime
from enum import Enum

from checkout_sdk.common.common import BankDetails, UpdateCustomerRequest, AccountHolder, Phone
from checkout_sdk.common.enums import (
    AccountType, AccountHolderType, AchAccountType, Currency, Country, InstrumentType, SepaMandateType,
)
from checkout_sdk.payments.payments import PaymentType


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


class InstrumentData:
    account_number: str
    country: Country
    currency: Currency
    payment_type: PaymentType
    mandate_id: str
    date_of_signature: datetime
    # SEPA mandate type — set when this InstrumentData is the SEPA variant.
    type: SepaMandateType
    # ACH-only fields below — set when this InstrumentData is the ACH variant.
    # Distinct from AccountType (which serves the bank-account instrument endpoint
    # with savings/current/cash) — ACH has its own value set.
    account_type: AchAccountType
    bank_code: str


class CreateSepaInstrumentRequest(CreateInstrumentRequest):
    token: str
    instrument_data: InstrumentData
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(InstrumentType.SEPA)


class CreateBankAccountInstrumentRequest(CreateInstrumentRequest):
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
    bank: BankDetails

    def __init__(self):
        super().__init__(InstrumentType.BANK_ACCOUNT)


class CreateCardInstrumentRequest(CreateInstrumentRequest):
    number: str
    expiry_month: int
    expiry_year: int
    account_holder: AccountHolder
    customer: CreateCustomerInstrumentRequest
    entity_id: str
    processing_channel_id: str
    network_token: str

    def __init__(self):
        super().__init__(InstrumentType.CARD)


class CreateAchInstrumentRequest(CreateInstrumentRequest):
    instrument_data: InstrumentData
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(InstrumentType.ACH)


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
