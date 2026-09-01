from datetime import datetime
from enum import Enum

from checkout_sdk.common.common import BankDetails, UpdateCustomerRequest, AccountHolder, Phone
from checkout_sdk.common.enums import (
    AccountType, AccountHolderType, AchAccountType, BacsPaymentType, Currency, Country, InstrumentType,
    InstrumentAccountHolderType, SepaMandateType, SepaPaymentType,
)


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


# SEPA
class SepaBillingAddress:
    """The billing address of the account holder of a SEPA instrument.

    address_line1 max 200, address_line2 max 10 and country min 2 max 2 characters. city and zip are
    max 35 and max 16 when storing, and max 50 both when updating.
    """
    address_line1: str
    address_line2: str
    city: str
    zip: str
    country: Country


class SepaAccountHolder:
    """The account holder details of a SEPA instrument.

    The schema declares these five properties only. Deliberately not AccountHolder, which is a
    superset carrying a phone, identification, a date of birth and a tax ID that this schema does not
    declare.
    """
    first_name: str
    last_name: str
    company_name: str
    billing_address: SepaBillingAddress
    type: InstrumentAccountHolderType


class SepaInstrumentData:
    """The details of a SEPA account.

    account_number is the IBAN, min 15 max 34 characters. mandate_id min 1 max 35 characters.
    date_of_signature is a yyyy-MM-dd string, required when mandate_id is provided and defaulting to
    the current date otherwise. Do not pass a datetime: the serializer emits a full ISO timestamp for
    it, which this field rejects, and a date object raises inside the serializer.
    """
    type: SepaMandateType
    account_number: str
    country: Country
    currency: Currency
    payment_type: SepaPaymentType
    mandate_id: str
    date_of_signature: str


# Bacs Direct Debit
class BacsBillingAddress:
    """The billing address of the account holder of a Bacs Direct Debit instrument.

    address_line1 max 200 and address_line2 max 10 characters. city and zip are max 35 and max 16
    when storing, and max 50 both when updating. country is min 2 max 2 characters and is the only
    required property when storing.
    """
    address_line1: str
    address_line2: str
    city: str
    zip: str
    country: Country


class CreateBacsAccountHolder:
    """The account holder details of a Bacs Direct Debit instrument being stored.

    The store schema declares first_name, last_name and billing_address only. It adds company_name
    and type on update, which UpdateBacsAccountHolder carries.
    """
    first_name: str
    last_name: str
    billing_address: BacsBillingAddress


class UpdateBacsAccountHolder:
    """The account holder details of a Bacs Direct Debit instrument being updated."""
    first_name: str
    last_name: str
    company_name: str
    billing_address: BacsBillingAddress
    type: InstrumentAccountHolderType


class BacsInstrumentAccount:
    r"""The account configuration for a Bacs Direct Debit instrument.

    processing_channel_id matches the pattern ^(pc)_(\w{26})$.
    """
    processing_channel_id: str


class BacsInstrumentData:
    """The details of a Bacs Direct Debit account.

    account_number is min 8 max 8 characters and bank_code is the six-digit sort code.
    payment_type is capitalised, unlike the SEPA equivalent.
    """
    account_number: str
    bank_code: str
    country: Country
    currency: Currency
    payment_type: BacsPaymentType
    allow_partial_match: bool


# ACH
class AchAccountHolder:
    """The account holder details of an ACH instrument.

    The schema marks all four properties required, but the descriptions qualify that: the names apply
    to an individual account holder and the company name to a corporate one. The ACH account holder
    declares no billing address.
    """
    first_name: str
    last_name: str
    company_name: str
    type: InstrumentAccountHolderType


class AchInstrumentData:
    """The details of an ACH bank account.

    account_number min 4 max 17 characters. bank_code is the routing number, min 8 max 9 characters.
    account_type is savings or checking, which AccountType does not declare.
    """
    account_type: AchAccountType
    account_number: str
    bank_code: str
    currency: Currency
    country: Country


class CreateSepaInstrumentRequest(CreateInstrumentRequest):
    instrument_data: SepaInstrumentData
    account_holder: SepaAccountHolder

    def __init__(self):
        super().__init__(InstrumentType.SEPA)


class CreateBacsInstrumentRequest(CreateInstrumentRequest):
    """Stores Bacs Direct Debit account details as a payment instrument."""

    account: BacsInstrumentAccount
    instrument_data: BacsInstrumentData
    account_holder: CreateBacsAccountHolder

    def __init__(self):
        super().__init__(InstrumentType.BACS)


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
    bank: BankDetails

    def __init__(self):
        super().__init__(InstrumentType.BANK_ACCOUNT)


class ProvisionNetworkToken:
    provision: bool


class CreateCardInstrumentRequest(CreateInstrumentRequest):
    number: str
    expiry_month: int
    expiry_year: int
    account_holder: AccountHolder
    customer: CreateCustomerInstrumentRequest
    entity_id: str
    processing_channel_id: str
    network_token: ProvisionNetworkToken

    def __init__(self):
        super().__init__(InstrumentType.CARD)


class CreateAchInstrumentRequest(CreateInstrumentRequest):
    instrument_data: AchInstrumentData
    account_holder: AchAccountHolder

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
    bank: BankDetails
    customer: UpdateCustomerRequest

    def __init__(self):
        super().__init__(InstrumentType.BANK_ACCOUNT)


class UpdateSepaInstrumentRequest(UpdateInstrumentRequest):
    """Updates the details of a stored SEPA instrument.

    Nothing in this request is required by the specification.
    """

    instrument_data: SepaInstrumentData
    account_holder: SepaAccountHolder

    def __init__(self):
        super().__init__(InstrumentType.SEPA)


class UpdateBacsInstrumentRequest(UpdateInstrumentRequest):
    """Updates the details of a stored Bacs Direct Debit instrument.

    Nothing in this request is required by the specification.
    """

    instrument_data: BacsInstrumentData
    account_holder: UpdateBacsAccountHolder

    def __init__(self):
        super().__init__(InstrumentType.BACS)


class UpdateAchInstrumentRequest(UpdateInstrumentRequest):
    """Updates the details of a stored ACH instrument.

    Nothing in this request is required by the specification.
    """

    instrument_data: AchInstrumentData
    account_holder: AchAccountHolder

    def __init__(self):
        super().__init__(InstrumentType.ACH)


# The payment-network query parameter of GET /validation/bank-accounts/{country}/{currency}.
# The specification declares these values lowercase.
class PaymentNetwork(str, Enum):
    LOCAL = 'local'
    SEPA = 'sepa'
    FPS = 'fps'
    ACH = 'ach'
    FEDWIRE = 'fedwire'
    SWIFT = 'swift'


class BankAccountFieldQuery:
    """Query parameters for GET /validation/bank-accounts/{country}/{currency}.

    The account-holder-type parameter declares individual, corporate and government.
    AccountHolderType also carries INSTRUMENT, which this parameter does not accept - see the note on
    that member. Both parameters are optional; the serializer maps them to the hyphenated wire names.
    """
    account_holder_type: AccountHolderType
    payment_network: PaymentNetwork
