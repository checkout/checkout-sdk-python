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


class Invitee:
    email: str


class ContactDetails:
    phone: Phone
    email_addresses: EntityEmailAddresses
    invitee: Invitee


class Profile:
    urls: list
    mccs: list
    default_holding_currency: Currency
    holding_currencies: list


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


class CompanyVerificationType(str, Enum):
    INCORPORATION_DOCUMENT = 'incorporation_document'
    ARTICLES_OF_ASSOCIATION = 'articles_of_association'


class CompanyVerification:
    type: CompanyVerificationType
    front: str


class TaxVerificationType(str, Enum):
    EIN_LETTER = 'ein_letter'


class TaxVerification:
    type: TaxVerificationType
    front: str


class ArticlesOfAssociationType(str, Enum):
    MEMORANDUM_OF_ASSOCIATION = "memorandum_of_association"
    ARTICLES_OF_ASSOCIATION = "articles_of_association"


class BankVerificationType(str, Enum):
    BANK_STATEMENT = 'bank_statement'


class BankVerification:
    type: BankVerificationType
    front: str


class ShareholderStructureType(str, Enum):
    CERTIFIED_SHAREHOLDER_STRUCTURE = 'certified_shareholder_structure'


class ShareholderStructure:
    type: ShareholderStructureType
    front: str


class ProofOfLegalityType(str, Enum):
    PROOF_OF_LEGALITY = 'proof_of_legality'


class ProofOfLegality:
    type: ProofOfLegalityType
    front: str


class ProofOfPrincipalAddressType(str, Enum):
    PROOF_OF_ADDRESS = 'proof_of_address'


class ProofOfPrincipalAddress:
    type: ProofOfPrincipalAddressType
    front: str


class AdditionalDocument:
    front: str


class FinancialVerificationType(str, Enum):
    FINANCIAL_STATEMENT = 'financial_statement'


class FinancialVerification:
    type: FinancialVerificationType
    front: str


class OnboardSubEntityDocuments:
    identity_verification: EntityIdentificationDocument
    company_verification: CompanyVerification
    articles_of_association: ArticlesOfAssociationType
    bank_verification: BankVerification
    shareholder_structure: ShareholderStructure
    proof_of_legality: ProofOfLegality
    proof_of_principal_address: ProofOfPrincipalAddress
    additional_document1: AdditionalDocument
    additional_document2: AdditionalDocument
    additional_document3: AdditionalDocument
    tax_verification: TaxVerification
    financial_verification: FinancialVerification


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
    documents: OnboardSubEntityDocuments


class EntityFinancialDocuments:
    bank_statement: EntityDocument
    financial_statement: EntityDocument


class EntityFinancialDetails:
    annual_processing_volume: int
    average_transaction_value: int
    highest_transaction_value: int
    documents: EntityFinancialDocuments
    currency: Currency


class DateOfIncorporation:
    month: int
    year: int


class Company:
    business_registration_number: str
    business_type: BusinessType
    legal_name: str
    trading_name: str
    date_of_incorporation: DateOfIncorporation
    regulatory_licence_number: str
    principal_address: Address
    registered_address: Address
    representatives: list  # EntityRepresentative
    document: EntityDocument
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
    financial_details: EntityFinancialDetails


class ProcessingDetails:
    settlement_country: str
    target_countries: list  # str
    annual_processing_volume: int
    average_transaction_value: int
    highest_transaction_value: int
    currency: Currency


class AdditionalInfo:
    field1: str
    field2: str
    field3: str


class OnboardEntityRequest:
    reference: str
    is_draft: bool
    profile: Profile
    contact_details: ContactDetails
    company: Company
    processing_details: ProcessingDetails
    individual: Individual
    documents: OnboardSubEntityDocuments
    additional_info: AdditionalInfo


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
