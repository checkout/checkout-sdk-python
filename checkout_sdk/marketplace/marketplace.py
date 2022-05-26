from enum import Enum

from checkout_sdk.common.common import Phone, Address
from checkout_sdk.common.common_four import ResidentialStatusType, AccountHolderIdentification
from checkout_sdk.common.enums import Currency, InstrumentType, Country
from checkout_sdk.common.enums_four import AccountType, AccountHolderType


class ContactDetails:
    phone: Phone


class Profile:
    urls: list
    mccs: list
    default_holding_currency: Currency


class EntityDocument:
    file_id: str
    type: str


class EntityIdentificationType(str, Enum):
    PASSPORT = 'passport'
    NATIONAL_IDENTITY_CARD = 'national_identity_card'
    DRIVING_LICENSE = 'driving_license'
    CITIZEN_CARD = 'citizen_card'
    RESIDENCE_PERMIT = 'residence_permit'
    ELECTORAL_ID = 'electoral_id'


class EntityIdentificationDocument:
    type: EntityIdentificationType
    front: str
    back: str


class EntityIdentification:
    national_id_number: str
    document: EntityIdentificationDocument


class EntityRepresentative:
    first_name: str
    middle_name: str
    last_name: str
    address: Address
    identification: EntityIdentification


class Company:
    business_registration_number: str
    legal_name: str
    trading_name: str
    principal_address: Address
    registered_address: Address
    document: EntityDocument
    representatives: list  # EntityRepresentative


class DateOfBirth:
    day: int
    month: int
    year: int


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


class BankDetails:
    name: str
    branch: str
    address: Address


class MarketplaceAccountHolder:
    type: AccountHolderType
    first_name: str
    last_name: str
    company_name: str
    tax_id: str
    date_of_birth: DateOfBirth
    country_of_birth: Country
    residential_status: ResidentialStatusType
    billing_address: Address
    phone: Phone
    identification: AccountHolderIdentification
    email: str


class MarketplacePaymentInstrument:
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
    account_holder: MarketplaceAccountHolder
    bank: BankDetails


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


class ScheduleRequest:
    frequency: ScheduleFrequency

    def __init__(self, frequency_p: ScheduleFrequency):
        self.frequency = frequency_p


class ScheduleFrequencyDailyRequest(ScheduleRequest):
    def __init__(self):
        super().__init__(ScheduleFrequency.DAILY)


class ScheduleFrequencyMonthlyRequest(ScheduleRequest):
    by_month_day: DaySchedule

    def __init__(self):
        super().__init__(ScheduleFrequency.MONTHLY)


class ScheduleFrequencyWeeklyRequest(ScheduleRequest):
    by_day: DaySchedule

    def __init__(self):
        super().__init__(ScheduleFrequency.WEEKLY)


class UpdateScheduleRequest:
    enabled: bool
    threshold: int
    recurrence: ScheduleRequest


# Transfers

class TransferType(str, Enum):
    COMMISSION = 'commission'
    PROMOTION = 'promotion'
    REFUND = 'refund'


class TransferSource:
    id: str
    amount: int


class TransferDestination:
    id: str


class CreateTransferRequest:
    reference: str
    transfer_type: TransferType
    source: TransferSource
    destination: TransferDestination


# Balances

class BalancesQuery:
    query: str
