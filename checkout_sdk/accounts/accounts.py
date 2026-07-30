from enum import Enum
from typing import Dict

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
    INDIVIDUAL_OR_SOLE_PROPRIETORSHIP = 'individual_or_sole_proprietorship'
    GENERAL_PARTNERSHIP = 'general_partnership'
    LIMITED_PARTNERSHIP = 'limited_partnership'
    SCOTTISH_LIMITED_PARTNERSHIP = 'scottish_limited_partnership'
    PUBLIC_LIMITED_COMPANY = 'public_limited_company'
    LIMITED_COMPANY = 'limited_company'
    LIMITED_LIABILITY_CORPORATION = 'limited_liability_corporation'
    PRIVATE_CORPORATION = 'private_corporation'
    PUBLICLY_TRADED_CORPORATION = 'publicly_traded_corporation'
    PROFESSIONAL_ASSOCIATION = 'professional_association'
    UNINCORPORATED_ASSOCIATION = 'unincorporated_association'
    AUTO_ENTREPRENEUR = 'auto_entrepreneur'
    GOVERNMENT_AGENCY = 'government_agency'
    NON_PROFIT_ENTITY = 'non_profit_entity'
    TRUST = 'trust'
    CLUB_OR_SOCIETY = 'club_or_society'
    REGULATED_FINANCIAL_INSTITUTION = 'regulated_financial_institution'
    CFTC_REGISTERED_ENTITY = 'cftc_registered_entity'
    SEC_REGISTERED_ENTITY = 'sec_registered_entity'


class EntityRoles(str, Enum):
    UBO = 'ubo'
    LEGAL_REPRESENTATIVE = 'legal_representative'
    AUTHORISED_SIGNATORY = 'authorised_signatory'
    DIRECTOR = 'director'
    CONTROL_PERSON = 'control_person'


class CompanyPosition(str, Enum):
    CEO = 'ceo'
    CFO = 'cfo'
    COO = 'coo'
    MANAGING_MEMBER = 'managing_member'
    GENERAL_PARTNER = 'general_partner'
    PRESIDENT = 'president'
    VICE_PRESIDENT = 'vice_president'
    TREASURER = 'treasurer'
    OTHER_SENIOR_MANAGEMENT = 'other_senior_management'
    OTHER_EXECUTIVE_OFFICER = 'other_executive_officer'
    OTHER_NON_EXECUTIVE_NON_SENIOR = 'other_non_executive_non_senior'


class NationalIdType(str, Enum):
    SSN = 'ssn'
    ITIN = 'itin'
    PASSPORT = 'passport'
    DRIVING_LICENSE = 'driving_license'
    NATIONAL_ID_CARD = 'national_id_card'
    RESIDENCE_PERMIT = 'residence_permit'
    OTHER = 'other'


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


class ArticlesOfAssociation:
    type: ArticlesOfAssociationType
    front: str


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


class FinancialStatementsType(str, Enum):
    FINANCIAL_STATEMENTS = 'financial_statements'


class FinancialStatements:
    type: FinancialStatementsType
    front: str


class OnboardSubEntityDocuments:
    identity_verification: EntityIdentificationDocument
    company_verification: CompanyVerification
    articles_of_association: ArticlesOfAssociation
    bank_verification: BankVerification
    shareholder_structure: ShareholderStructure
    proof_of_legality: ProofOfLegality
    proof_of_principal_address: ProofOfPrincipalAddress
    additional_document1: AdditionalDocument
    additional_document2: AdditionalDocument
    additional_document3: AdditionalDocument
    tax_verification: TaxVerification
    financial_verification: FinancialVerification
    financial_statements: FinancialStatements


class CertifiedAuthorisedSignatoryType(str, Enum):
    POWER_OF_ATTORNEY = 'power_of_attorney'


class CertifiedAuthorisedSignatory:
    type: CertifiedAuthorisedSignatoryType
    front: str


class ProofOfResidentialAddressType(str, Enum):
    PROOF_OF_ADDRESS = 'proof_of_address'


class ProofOfResidentialAddress:
    type: ProofOfResidentialAddressType
    front: str


class ProofOfRegistrationType(str, Enum):
    EXTRACT_FROM_TRADE_REGISTER = 'extract_from_trade_register'
    OTHER = 'other'


class ProofOfRegistration:
    type: ProofOfRegistrationType
    front: str


# The representative-level documents union (Accounts API v3.0) is a distinct, smaller shape than the
# entity-level OnboardSubEntityDocuments — per shared/swagger-latest.json it carries only these fields.
class RepresentativeDocuments:
    identity_verification: EntityIdentificationDocument
    certified_authorised_signatory: CertifiedAuthorisedSignatory
    proof_of_residential_address: ProofOfResidentialAddress
    proof_of_registration: ProofOfRegistration


class Citizenship:
    type: str
    country: Country


class RepresentativeIndividual:
    first_name: str
    middle_name: str
    last_name: str
    date_of_birth: DateOfBirth
    place_of_birth: PlaceOfBirth
    citizenships: list  # Citizenship
    national_id_type: NationalIdType
    national_id_number: str
    email_address: str
    phone: Phone
    address: Address


class EntityRepresentative:
    # v3.0 (Accounts API v3.0)
    id: str
    individual: RepresentativeIndividual
    roles: list  # accounts.EntityRoles
    company_position: CompanyPosition
    ownership_percentage: int
    documents: RepresentativeDocuments
    # v2.0 only — deprecated; use `individual` for v3.0
    first_name: str
    middle_name: str
    last_name: str
    address: Address
    identification: EntityIdentification
    phone: Phone
    date_of_birth: DateOfBirth
    place_of_birth: PlaceOfBirth


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
    day: int
    month: int
    year: int


class Company:
    business_registration_number: str
    business_type: BusinessType
    legal_name: str
    trading_name: str
    additional_trading_names: list  # str
    is_registered_company: bool
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


class ProcessingDetailsAch:
    annual_ach_volume: int
    average_ach_transaction_size: int
    estimated_monthly_credit_volume: int
    average_credit_amount: int


class ProcessingDetailsPayments:
    ach: ProcessingDetailsAch


class ProcessingDetails:
    settlement_country: str
    target_countries: list  # str
    annual_processing_volume: int
    average_transaction_value: int
    average_order_fulfillment_time: int
    highest_transaction_value: int
    currency: Currency
    payments: ProcessingDetailsPayments


class AdditionalInfo:
    field1: str
    field2: str
    field3: str


class AgreedTerms:
    date: str
    ip_address: str
    name: str
    email: str
    version: str


class SchemaVersionHeader:
    accept: str

    def get_header_mappings(self) -> Dict[str, str]:
        return {
            'accept': 'Accept'
        }


class OnboardEntityRequest:
    reference: str
    is_draft: bool
    profile: Profile
    contact_details: ContactDetails
    company: Company
    processing_details: ProcessingDetails
    agreed_terms: AgreedTerms
    seller_category: str
    documents: OnboardSubEntityDocuments
    additional_info: AdditionalInfo
    # v2.0 only — deprecated; a v3.0 sole trader is onboarded as a `company` with representatives
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


class InstrumentAccountType(str, Enum):
    SAVINGS = 'savings'
    CHECKING = 'checking'


class InstrumentDetailsAch(InstrumentDetails):
    account_number: str
    routing_number: str
    account_type: InstrumentAccountType


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
    type: InstrumentType
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


class ReserveRuleType(str, Enum):
    ROLLING = 'rolling'


class HoldingDuration:
    weeks: int


class RollingReserveRule:
    percentage: float
    holding_duration: HoldingDuration


class ReserveRuleRequest:
    type: ReserveRuleType
    rolling: RollingReserveRule
    valid_from: str


class FilePurpose(str, Enum):
    ADDITIONAL_DOCUMENT = 'additional_document'
    ARTICLES_OF_ASSOCIATION = 'articles_of_association'
    BANK_VERIFICATION = 'bank_verification'
    CERTIFIED_AUTHORISED_SIGNATORY = 'certified_authorised_signatory'
    COMPANY_OWNERSHIP = 'company_ownership'
    IDENTIFICATION = 'identification'
    IDENTITY_VERIFICATION = 'identity_verification'
    DISPUTE_EVIDENCE = 'dispute_evidence'
    COMPANY_VERIFICATION = 'company_verification'
    FINANCIAL_VERIFICATION = 'financial_verification'
    TAX_VERIFICATION = 'tax_verification'
    PROOF_OF_LEGALITY = 'proof_of_legality'
    PROOF_OF_PRINCIPAL_ADDRESS = 'proof_of_principal_address'
    SHAREHOLDER_STRUCTURE = 'shareholder_structure'
    PROOF_OF_RESIDENTIAL_ADDRESS = 'proof_of_residential_address'
    PROOF_OF_REGISTRATION = 'proof_of_registration'


class EntityFileRequest:
    purpose: FilePurpose


class EntityRequirementUpdateRequest:
    value: object


class EtagHeader:
    etag: str

    def get_header_mappings(self) -> Dict[str, str]:
        return {
            'etag': 'If-Match'
        }
