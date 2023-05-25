from enum import Enum

from checkout_sdk.common.common import Phone, Address
from checkout_sdk.common.common import ResidentialStatusType, AccountHolderIdentification
from checkout_sdk.common.enums import Currency, InstrumentType, Country, AccountType, AccountHolderType, DocumentType


class ScheduleFrequency(str, Enum):
    WEEKLY = 'weekly'
    DAILY = 'daily'
    MONTHLY = 'monthly'


class DaySchedule(str, Enum):
    MONDAY = 'monday'
    TUESDAY = 'tuesday'
    WEDNESDAY = 'wednesday'
    THURSDAY = 'thursday'
    FRIDAY = 'friday'
    SATURDAY = 'saturday'
    SUNDAY = 'sunday'


class BusinessType(str, Enum):
    GENERAL_PARTNERSHIP = 'general_partnership'
    LIMITED_PARTNERSHIP = 'limited_partnership'
    PUBLIC_LIMITED_COMPANY = 'public_limited_company'
    LIMITED_COMPANY = 'limited_company'
    PROFESSIONAL_ASSOCIATION = 'professional_association'
    UNINCORPORATED_ASSOCIATION = 'unincorporated_association'
    AUTO_ENTREPRENEUR = 'auto_entrepreneur'


class EntityRoles(str, Enum):
    UBO = 'ubo'
    LEGAL_REPRESENTATIVE = 'legal_representative'


class EntityEmailAddresses:
    primary: str


class ContactDetails:
    phone: Phone
    email_addresses: EntityEmailAddresses


class Profile:
    urls: list
    mccs: list
    default_holding_currency: Currency


class EntityDocument:
    file_id: str
    type: str


class EntityIdentificationDocument:
    type: DocumentType
    front: str
    back: str


class EntityIdentification:
    national_id_number: str
    document: EntityIdentificationDocument


class DateOfBirth:
    day: int
    month: int
    year: int


class PlaceOfBirth:
    country: Country


class EntityRepresentative:
    first_name: str
    middle_name: str
    last_name: str
    address: Address
    identification: EntityIdentification
    phone: Phone
    date_of_birth: DateOfBirth
    place_of_birth: PlaceOfBirth
    roles: list  # accounts.EntityRoles


class EntityFinancialDocuments:
    bank_statement: EntityDocument
    financial_statement: EntityDocument


class EntityFinancialDetails:
    annual_processing_volume: int
    average_transaction_value: int
    highest_transaction_value: int
    documents: EntityFinancialDocuments


class Company:
    business_registration_number: str
    business_type: BusinessType
    legal_name: str
    trading_name: str
    principal_address: Address
    registered_address: Address
    document: EntityDocument
    representatives: list  # EntityRepresentative
    financial_details: EntityFinancialDetails


class Identification:
    national_id_number: str
    document: EntityIdentificationDocument


class Individual:
    first_name: str
    middle_name: str
    last_name: str
    trading_name: str
    national_tax_id: str
    registered_address: Address
    date_of_birth: DateOfBirth
    place_of_birth: PlaceOfBirth
    identification: Identification


class OnboardEntityRequest:
    reference: str
    contact_details: ContactDetails
    profile: Profile
    company: Company
    individual: Individual


class InstrumentDocument:
    type: str
    file_id: str


class InstrumentDetails:
    pass


class InstrumentDetailsFasterPayments(InstrumentDetails):
    account_number: str
    bank_code: str


class InstrumentDetailsSepa(InstrumentDetails):
    iban: str
    swift_bic: str


class InstrumentDetailsCardToken(InstrumentDetails):
    token: str


class BankDetails:
    name: str
    branch: str
    address: Address


class AccountsAccountHolder:
    type: AccountHolderType
    tax_id: str
    date_of_birth: DateOfBirth
    country_of_birth: Country
    residential_status: ResidentialStatusType
    billing_address: Address
    phone: Phone
    identification: AccountHolderIdentification
    email: str


class AccountsCorporateAccountHolder(AccountsAccountHolder):
    company_name: str


class AccountsIndividualAccountHolder(AccountsAccountHolder):
    first_name: str
    last_name: str


class AccountsPaymentInstrument:
    type = InstrumentType.BANK_ACCOUNT
    label: str
    account_type: AccountType
    account_number: str
    bank_code: str
    branch_code: str
    iban: str
    bban: str
    swift_bic: str
    currency: Currency
    country: Country
    document: InstrumentDocument
    account_holder: AccountsAccountHolder
    bank: BankDetails


class PaymentInstrumentRequest:
    label: str
    type = InstrumentType
    currency: Currency
    country: Country
    default: bool
    document: InstrumentDocument
    instrument_details: InstrumentDetails


class Headers:
    if_match: str


class UpdatePaymentInstrumentRequest:
    label: str
    default: bool
    headers: Headers


class ScheduleRequest:
    frequency: ScheduleFrequency

    def __init__(self, frequency_p: ScheduleFrequency):
        self.frequency = frequency_p


class ScheduleFrequencyDailyRequest(ScheduleRequest):
    def __init__(self):
        super().__init__(ScheduleFrequency.DAILY)


class ScheduleFrequencyMonthlyRequest(ScheduleRequest):
    by_month_day: list  # int

    def __init__(self):
        super().__init__(ScheduleFrequency.MONTHLY)


class ScheduleFrequencyWeeklyRequest(ScheduleRequest):
    by_day: list  # DaySchedule

    def __init__(self):
        super().__init__(ScheduleFrequency.WEEKLY)


class UpdateScheduleRequest:
    enabled: bool
    threshold: int
    recurrence: ScheduleRequest


class PaymentInstrumentsQuery:
    status: str
