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
    """Email addresses for this sub-entity."""
    # The main email address for this sub-entity.
    # [Required]
    # Format: email
    primary: str


class Invitee:
    """The details of the user responsible for onboarding the sub-entity."""
    # The main email address for this sub-entity. Despite the spec's wording, this is the address of
    # the invitee, the user responsible for onboarding the sub-entity.
    # [Optional]
    # Format: email
    email: str


class ContactDetails:
    """Contact details of the sub-entity."""
    # The phone number of the sub-entity.
    # [Required] for every Accounts API v2.0 variant and the US ISV Seller variants; [Optional] for
    # the other v3.0 variants.
    # On v3.0 country_code is required and is the ISO 3166-1 alpha-2 country where the number is
    # registered (for example 'FR'), not the dialling code; v2.0 takes number only. number is the
    # number without the country calling code, and its format depends on the variant:
    #   v3.0 EEA: ^[0-9]{6,13}$, min 6 characters, max 13 characters
    #   v3.0 GB: ^[0-9]{7,11}$, min 7 characters, max 11 characters
    #   v3.0 US and US ISV Seller: ^[1-9][0-9]{9,16}$, min 10 characters, max 16 characters
    #   v2.0: ^[1-9][0-9]{7,15}$, min 8 characters, max 16 characters; on the US v2.0 variants
    #   ^[2-9]{1}[0-9]{9,15}$, min 10 characters
    phone: Phone
    # Email addresses for this sub-entity.
    # [Required] for every Accounts API v2.0 variant and the US ISV Seller variants; [Optional] for
    # the other v3.0 variants.
    email_addresses: EntityEmailAddresses
    # The details of the user responsible for onboarding the sub-entity.
    # [Optional] (not part of the US ISV Seller variants)
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
    """The document to use to confirm an individual's identity (identity_verification): on a
    representative (Accounts API v3.0), or at the top level of the v2.0 sole trader variants."""
    # The type of document used for identity verification.
    # [Required]
    type: DocumentType
    # The ID of the front side of the document as represented within Checkout.com systems.
    # [Required]
    # ^file_[a-z2-7]{26}$
    # 31 characters
    front: str
    # The ID of the back side of the document as represented within Checkout.com systems.
    # [Optional]
    # ^file_[a-z2-7]{26}$
    # 31 characters
    back: str


class EntityIdentification:
    """The identification of a representative on the Accounts API v2.0 US Company variants."""
    # Social Security Number (SSN), or Individual Taxpayer Identification Number (ITIN) for non-US
    # citizens.
    # [Required]
    # ^\d{9}$
    # 9 characters
    national_id_number: str
    # Deprecated: not defined by the Accounts API, the identification object carries
    # national_id_number only. Retained so existing code keeps working; the API does not read it.
    document: EntityIdentificationDocument


class DateOfBirth:
    day: int
    month: int
    year: int


class PlaceOfBirth:
    country: Country


class CompanyVerificationType(str, Enum):
    """The document types accepted as company verification. articles_of_association is accepted on
    the US Company (2.0) variants only; articles of association sent as their own document use
    ArticlesOfAssociationType instead."""
    INCORPORATION_DOCUMENT = 'incorporation_document'
    ARTICLES_OF_ASSOCIATION = 'articles_of_association'


class CompanyVerification:
    """The document to use to confirm the company's identity (certified by a power of attorney within
    the last 3 months)."""
    # The type of document used for company verification.
    # [Required]
    type: CompanyVerificationType
    # The ID of the front side of the document as represented within Checkout.com systems.
    # [Required]
    # ^file_[a-z2-7]{26}$
    # 31 characters
    front: str


class TaxVerificationType(str, Enum):
    """The document type accepted as tax verification: an IRS-issued Employer Identification Number
    letter."""
    EIN_LETTER = 'ein_letter'


class TaxVerification:
    """IRS-issued Employer Identification Number document used to verify the entity's tax
    identification (US variants)."""
    # The type of IRS-issued document used for tax verification.
    # [Required]
    type: TaxVerificationType
    # The ID of the front side of the document as represented within Checkout.com systems.
    # [Required]
    # ^file_[a-z2-7]{26}$
    # 31 characters
    front: str


class ArticlesOfAssociationType(str, Enum):
    """The document types accepted as memorandum or articles of association."""
    MEMORANDUM_OF_ASSOCIATION = "memorandum_of_association"
    ARTICLES_OF_ASSOCIATION = "articles_of_association"


class ArticlesOfAssociation:
    """Memorandum or Articles of Association document."""
    # The type of document used.
    # [Required]
    type: ArticlesOfAssociationType
    # The ID of the front side of the document as represented within Checkout.com systems.
    # [Required]
    # ^file_[a-z2-7]{26}$
    # 31 characters
    front: str


class BankVerificationType(str, Enum):
    """The document type accepted as bank verification."""
    BANK_STATEMENT = 'bank_statement'


class BankVerification:
    """A document showing transactions from the last 3 months."""
    # The type of document being used as bank verification.
    # [Required]
    type: BankVerificationType
    # The ID of the front side of the document as represented within Checkout.com systems.
    # [Required]
    # ^file_[a-z2-7]{26}$
    # 31 characters
    front: str


class ShareholderStructureType(str, Enum):
    """The document type accepted as a certified shareholder structure."""
    CERTIFIED_SHAREHOLDER_STRUCTURE = 'certified_shareholder_structure'


class ShareholderStructure:
    """Shareholder structure chart (including % of shares) certified by a competent authority
    individual and dated within the last 3 months."""
    # The type of document.
    # [Required]
    type: ShareholderStructureType
    # The ID of the front side of the document as represented within Checkout.com systems.
    # [Required]
    # ^file_[a-z2-7]{26}$
    # 31 characters
    front: str


class ProofOfLegalityType(str, Enum):
    """The document type accepted as proof of legality."""
    PROOF_OF_LEGALITY = 'proof_of_legality'


class ProofOfLegality:
    """A regulatory licence document required for the company to operate (when applicable)."""
    # The type of document used for proof of legality.
    # [Required]
    type: ProofOfLegalityType
    # The ID of the front side of the document as represented within Checkout.com systems.
    # [Required]
    # ^file_[a-z2-7]{26}$
    # 31 characters
    front: str


class ProofOfPrincipalAddressType(str, Enum):
    """The document type accepted as proof of the company's principal place of business. Carries the
    same proof_of_address value as ProofOfResidentialAddressType, but the API defines the two as
    separate enums on separate documents."""
    PROOF_OF_ADDRESS = 'proof_of_address'


class ProofOfPrincipalAddress:
    """Proof of the company's principal place of business."""
    # The type of document being used as address verification.
    # [Required]
    type: ProofOfPrincipalAddressType
    # The ID of the front side of the document as represented within Checkout.com systems.
    # [Required]
    # ^file_[a-z2-7]{26}$
    # 31 characters
    front: str


class AdditionalDocument:
    """Additional space for documents to be provided when requested. Carries a file ID only; the API
    defines no document type for it."""
    # The ID of the front side of the document as represented within Checkout.com systems.
    # [Required]
    # ^file_[a-z2-7]{26}$
    # 31 characters
    front: str


class FinancialVerificationType(str, Enum):
    """The document type accepted as financial verification. Note the singular financial_statement;
    FinancialStatementsType is a different enum."""
    FINANCIAL_STATEMENT = 'financial_statement'


class FinancialVerification:
    """Financial statement document. Becomes mandatory depending on the answer provided for
    annual_processing_volume; the sub-entity's status changes to requirements_due when it is
    needed."""
    # The type of the file.
    # [Required]
    type: FinancialVerificationType
    # The ID of the front side of the document as represented within Checkout.com systems.
    # [Required]
    # ^file_[a-z2-7]{26}$
    # 31 characters
    front: str


class FinancialStatementsType(str, Enum):
    """The document type accepted as financial statements (US ISV Seller variants). Note the plural
    financial_statements; FinancialVerificationType is a different enum."""
    FINANCIAL_STATEMENTS = 'financial_statements'


class FinancialStatements:
    """Audited or management-prepared financial statements (when applicable). US ISV Seller variants
    only."""
    # The type of document.
    # [Required]
    type: FinancialStatementsType
    # The ID of the front side of the document as represented within Checkout.com systems.
    # [Required]
    # ^file_[a-z2-7]{26}$
    # 31 characters
    front: str


class OnboardSubEntityDocuments:
    """The top-level request documents (OnboardEntityRequest.documents). The API ignores keys it does
    not recognise here rather than rejecting them, so a misplaced document is dropped silently. The
    representative's own documents go on EntityRepresentative.documents (RepresentativeDocuments)."""
    # The document to use to confirm the individual's identity.
    # [Required] for the six sole trader variants of Accounts API v2.0 (EEA, GB and US, Full and
    # Lite), the only variants that take it at this level. On v3.0 it belongs on the representative.
    identity_verification: EntityIdentificationDocument
    # The document to use to confirm the company's identity (certified by a power of attorney within
    # the last 3 months).
    # [Required] for EEA Company Full (2.0 and 3.0) and GB Company Full (2.0); [Optional] for the other
    # company variants and the US ISV Seller variants.
    company_verification: CompanyVerification
    # Memorandum or Articles of Association document.
    # [Required] for EEA and GB Company Full (3.0); [Optional] for US Company Full (3.0) and the US ISV
    # Seller variants.
    articles_of_association: ArticlesOfAssociation
    # A document showing transactions from the last 3 months.
    # [Required] for EEA Company Full (3.0) and the EEA, GB and US Sole Trader Full (3.0) variants;
    # [Optional] for GB and US Company Full (3.0) and EEA Company Full and Lite (2.0).
    bank_verification: BankVerification
    # Shareholder structure chart (including % of shares) certified by a competent authority
    # individual and dated within the last 3 months.
    # [Required] for EEA and GB Company Full (3.0); [Optional] for US Company Full (3.0) and US ISV
    # Seller Company (3.0).
    shareholder_structure: ShareholderStructure
    # A regulatory licence document required for the company to operate (when applicable).
    # [Optional] (EEA, GB and US Company Full (3.0) and the US ISV Seller variants)
    proof_of_legality: ProofOfLegality
    # Proof of the company's principal place of business.
    # [Optional] (EEA, GB and US Company Full (3.0) and the US ISV Seller variants)
    proof_of_principal_address: ProofOfPrincipalAddress
    # Additional space for documents to be provided when requested.
    # [Optional] (EEA, GB and US Company and Sole Trader Full (3.0); not the US ISV Seller variants)
    additional_document1: AdditionalDocument
    # Additional space for documents to be provided when requested.
    # [Optional] (EEA, GB and US Company and Sole Trader Full (3.0); not the US ISV Seller variants)
    additional_document2: AdditionalDocument
    # Additional space for documents to be provided when requested.
    # [Optional] (EEA, GB and US Company and Sole Trader Full (3.0); not the US ISV Seller variants)
    additional_document3: AdditionalDocument
    # IRS-issued Employer Identification Number document used to verify the entity's tax
    # identification.
    # [Optional] (US Company variants and the US ISV Seller variants only)
    tax_verification: TaxVerification
    # Financial statement document. Becomes mandatory depending on the answer provided for
    # annual_processing_volume.
    # [Optional] (EEA Company Full and Lite (2.0) only)
    financial_verification: FinancialVerification
    # Audited or management-prepared financial statements (when applicable).
    # [Optional] (US ISV Seller variants only)
    financial_statements: FinancialStatements


class CertifiedAuthorisedSignatoryType(str, Enum):
    """The document type accepted as a representative's certified authorised signatory document."""
    POWER_OF_ATTORNEY = 'power_of_attorney'


class CertifiedAuthorisedSignatory:
    """Certified authorised signatory document. Required when the legal representative or other role
    owner is not registered on the certificate of incorporation. Representative documents only,
    EEA, GB and US Company Full (3.0) and US ISV Seller Company (3.0)."""
    # The type of document.
    # [Required]
    type: CertifiedAuthorisedSignatoryType
    # The ID of the front side of the document as represented within Checkout.com systems.
    # [Required]
    # ^file_[a-z2-7]{26}$
    # 31 characters
    front: str


class ProofOfResidentialAddressType(str, Enum):
    """The document type accepted as a representative's proof of residential address (EEA Sole Trader
    Full (3.0)). Carries the same proof_of_address value as ProofOfPrincipalAddressType, but the API
    defines the two as separate enums on separate documents."""
    PROOF_OF_ADDRESS = 'proof_of_address'


class ProofOfResidentialAddress:
    """Proof of residential address of the representative. Representative documents only, EEA Sole
    Trader Full (3.0)."""
    # The type of document being used as address verification.
    # [Required]
    type: ProofOfResidentialAddressType
    # The ID of the front side of the document as represented within Checkout.com systems.
    # [Required]
    # ^file_[a-z2-7]{26}$
    # 31 characters
    front: str


class ProofOfRegistrationType(str, Enum):
    """The document types accepted as a sole trader's proof of registration (EEA Sole Trader Full
    (3.0))."""
    EXTRACT_FROM_TRADE_REGISTER = 'extract_from_trade_register'
    OTHER = 'other'


class ProofOfRegistration:
    """Proof of the sole trader's registration, for example an extract from a trade register.
    Representative documents only, EEA Sole Trader Full (3.0)."""
    # The type of document being used as proof of registration.
    # [Required]
    type: ProofOfRegistrationType
    # The ID of the front side of the document as represented within Checkout.com systems.
    # [Required]
    # ^file_[a-z2-7]{26}$
    # 31 characters
    front: str


class RepresentativeDocuments:
    """Verification documents for an individual representative, sent as
    company.representatives[].documents (Accounts API v3.0).

    The API validates this object strictly: a key it does not recognise is rejected, not ignored.
    These four are the only keys it accepts, and which apply depends on the onboarding variant:
    EEA Sole Trader Full (3.0) requires identity_verification, proof_of_residential_address and
    proof_of_registration; GB and US Sole Trader Full (3.0) require identity_verification; the
    EEA, GB and US Company Full (3.0) variants accept identity_verification and
    certified_authorised_signatory, both optional.

    Leave an attribute unset rather than assigning None: an attribute set to None is sent as null.
    """
    # The document to use to confirm the individual's identity.
    # [Optional] (required for the sole trader full variants)
    identity_verification: EntityIdentificationDocument
    # Certified authorised signatory document. Required when the legal representative or other role
    # owner is not registered on the certificate of incorporation.
    # [Optional] (company full variants only)
    certified_authorised_signatory: CertifiedAuthorisedSignatory
    # Proof of residential address of the representative.
    # [Optional] (required for EEA Sole Trader Full (3.0), and only valid there)
    proof_of_residential_address: ProofOfResidentialAddress
    # Proof of the sole trader's registration, for example an extract from a trade register.
    # [Optional] (required for EEA Sole Trader Full (3.0), and only valid there)
    proof_of_registration: ProofOfRegistration


class Citizenship:
    """A citizenship or legal-status record (US ISV Seller variants)."""
    # The type of citizenship or legal status (for example citizenship or residency).
    # [Optional]
    type: str
    # The two-letter ISO 3166-1 alpha-2 country code.
    # [Required]
    # Format: iso-3166-1-alpha-2
    country: Country


class RepresentativeIndividual:
    """The personal details of a company representative (company.representatives[].individual),
    Accounts API v3.0."""
    # The representative's first name.
    # [Required]
    # min 2 characters, max 50 characters
    first_name: str
    # The representative's middle name. Required if it appears in official documents.
    # [Optional]
    # min 2 characters, max 50 characters
    middle_name: str
    # The representative's last name.
    # [Required]
    # min 2 characters, max 50 characters
    last_name: str
    # The date of birth of the person according to the Gregorian calendar.
    # [Required]
    date_of_birth: DateOfBirth
    # The place of birth of the person.
    # [Required]
    place_of_birth: PlaceOfBirth
    # The list of citizenships or legal statuses for the representative (Citizenship items).
    # [Required] for the US ISV Seller variants only; not part of the other v3.0 schemas, leave unset
    # for them.
    citizenships: list  # Citizenship
    # The classification of the national identification number provided.
    # [Required] for the US ISV Seller variants only; not part of the other v3.0 schemas, leave unset
    # for them.
    national_id_type: NationalIdType
    # The representative's national identification number.
    # [Required] for the US ISV Seller variants; [Optional] for the other v3.0 variants.
    # The format depends on the variant:
    #   US ISV Seller: the number for the national_id_type given. ^[a-zA-Z0-9\-]+$, min 5 characters,
    #   max 16 characters.
    #   Other v3.0 variants: a Social Security Number (SSN) or Individual Taxpayer Identification
    #   Number (ITIN), US residents only. ^\d{9}$, 9 characters.
    national_id_number: str
    # The representative's personal email address.
    # [Required] for the US ISV Seller variants; [Optional] for the other v3.0 variants.
    # Format: email
    email_address: str
    # The representative's phone number.
    # [Required] for the US ISV Seller variants; [Optional] for the other v3.0 variants.
    phone: Phone
    # The representative's address.
    # [Required]
    address: Address


class EntityRepresentative:
    """A representative of the sub-entity. One class covers every shape the Accounts API defines:
    the v3.0 person of interest (individual, roles, company_position, ownership_percentage,
    documents), the v3.0 controlling company of EEA and GB Company Full (company,
    ownership_percentage), and the v2.0 company representative (the flat person fields, roles,
    documents and, on the US variants, identification)."""
    # v3.0 (Accounts API v3.0)
    # The representative's id.
    # [Optional]
    # ^rep_[a-z0-9]{26}$
    # 30 characters
    id: str
    # Information about the individual representing the sub-entity.
    # [Required] for every v3.0 person of interest.
    individual: RepresentativeIndividual
    # The individual's roles within the company (EntityRoles items). For sole traders, must be ubo
    # only.
    # [Required] for every variant except EEA and US Company Lite (2.0), where it is [Optional].
    roles: list  # accounts.EntityRoles
    # The position of the representative within the company (required for the control_person role).
    # [Optional] (EEA, GB and US Company Full (3.0) and US ISV Seller Company (3.0))
    company_position: CompanyPosition
    # The percentage ownership of the UBO or controlling company (required when over 25%).
    # [Optional]
    # min 25, max 100 on the EEA, GB and US Company Full (3.0) variants; min 0, max 100 on the US ISV
    # Seller variants
    ownership_percentage: int
    # Verification documents for the individual representative. See RepresentativeDocuments: the API
    # validates this object strictly and rejects any key other than its four.
    # [Required] for the EEA, GB and US Sole Trader Full (3.0) variants; [Optional] otherwise.
    documents: RepresentativeDocuments
    # The controlling company, when the representative is a company rather than an individual.
    # [Required] for a controlling company representative (EEA and GB Company Full (3.0) only).
    # The API reads only three attributes here, all [Required]: legal_name, trading_name and
    # registered_address. Leave the other Company attributes unset.
    company: 'Company'
    # v2.0 only — deprecated; use `individual` for v3.0
    # The representative's first name.
    # [Required] (v2.0)
    # min 2 characters, max 50 characters
    first_name: str
    # The representative's middle name. Required if it appears in official documents.
    # [Optional]
    # min 2 characters, max 50 characters
    middle_name: str
    # The representative's last name.
    # [Required] (v2.0)
    # min 2 characters, max 50 characters
    last_name: str
    # The representative's address.
    # [Required] (v2.0)
    address: Address
    # The representative's identification. US Company (2.0) only.
    # [Required] for US Company Full (2.0); [Optional] for US Company Lite (2.0).
    identification: EntityIdentification
    # The representative's phone number.
    # [Optional]
    phone: Phone
    # The date of birth of the person according to the Gregorian calendar.
    # [Required] for the v2.0 Full variants; [Optional] for the v2.0 Lite variants.
    date_of_birth: DateOfBirth
    # The place of birth of the person.
    # [Required] for EEA Company Full (2.0); [Optional] for EEA Company Lite (2.0). Not part of the
    # other v2.0 variants.
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
    """Information about the company represented by the sub-entity: on every company and v3.0 sole
    trader variant, and as the controlling company of an EntityRepresentative (where only
    legal_name, trading_name and registered_address apply)."""
    # The sub-entity's business registration number: a Commercial Registration or Ministry of
    # Commerce certificate number, or an equivalent registration number.
    # [Required] for the Full variants and US ISV Seller Company (3.0); [Optional] for the Lite (2.0)
    # variants. Not part of the sole trader variants.
    # The format depends on the variant:
    #   EEA: min 2 characters, max 39 characters; a SIRET number for sub-entities based in France.
    #   GB (3.0): a Companies House number, 8 characters, matching one of the three alternatives of
    #   the spec's pattern, ^(A|B|C)$:
    #     A: ((AC|CE|CS|FC|FE|GE|GS|IC|LP|NC|NF|NI|NL|NO|NP|OC|OE|PC|R0|RC|SA|SC|SE|SF|SG|SI|SL|SO|SR|SZ|ZC|\d{2})\d{6})
    #     B: ((IP|SP|RS)[A-Z\d]{6})
    #     C: (SL\d{5}[\dA])
    #   GB (2.0) accepts the same pattern case-insensitively.
    #   US: an Employer Identification Number (EIN), ^[0-9]{9}$, 9 characters; US ISV Seller Company
    #   (3.0) also accepts the hyphenated form, ^[0-9]{2}-?[0-9]{7}$, min 9 characters, max 11.
    business_registration_number: str
    # The legal type of the company. Must be individual_or_sole_proprietorship for the sole trader
    # variants.
    # [Required], except on EEA and US Company Lite (2.0) where it is [Optional]. Not part of GB
    # Company Full and Lite (2.0).
    business_type: BusinessType
    # The legal name of the sub-entity.
    # [Required] for every company variant and the controlling company; not part of the sole trader
    # variants.
    # min 2 characters, max 300 characters
    legal_name: str
    # The trading name of the sub-entity, also referred to as 'doing business as'.
    # [Required]
    # min 2 characters, max 300 characters
    trading_name: str
    # The collection of additional trading names for the sub-entity.
    # [Optional] (US ISV Seller variants only)
    additional_trading_names: list  # str
    # Indicates whether the sub-entity is a registered legal entity. Must be False for US ISV Seller
    # Sole Trader (3.0).
    # [Required] for US ISV Seller Sole Trader (3.0); not part of the other variants.
    is_registered_company: bool
    # The date the company was incorporated, or the date the sole trader started trading.
    # [Required] for every v3.0 variant; [Optional] for EEA, GB and US Company Full (2.0).
    date_of_incorporation: DateOfIncorporation
    # The regulatory licence number of the company.
    # [Optional] (EEA Company Full (3.0) only)
    # ^[a-zA-Z0-9\-]+$
    # min 4 characters, max 32 characters
    regulatory_licence_number: str
    # The primary location where business is performed.
    # [Required] for every company and v3.0 sole trader variant.
    principal_address: Address
    # The registered address of the company.
    # [Required] for every company variant and the controlling company; not part of the sole trader
    # variants.
    registered_address: Address
    # Information about the representatives of this company (EntityRepresentative items).
    # [Required]
    # min 1 item; max 1 item for the sole trader variants (the individual themselves, with roles
    # [ubo]), max 5 on v2.0, max 25 on EEA, GB and US Company Full (3.0), no maximum on US ISV Seller
    # Company (3.0)
    representatives: list  # EntityRepresentative
    # Deprecated: not defined by any Accounts API company schema. Retained so existing code keeps
    # working; the API does not read it.
    document: EntityDocument
    # Seller financial questions and supporting documents.
    # [Required] for EEA and US Company Full (2.0); [Optional] for EEA and US Company Lite (2.0). Not
    # part of the other variants.
    financial_details: EntityFinancialDetails


class Identification:
    """The identification of the individual on the Accounts API v2.0 US Sole Trader variants."""
    # Social Security Number (SSN), or Individual Taxpayer Identification Number (ITIN) for non-US
    # citizens.
    # [Required]
    # ^\d{9}$
    # 9 characters
    national_id_number: str
    # Deprecated: not defined by the Accounts API, the identification object carries
    # national_id_number only. Retained so existing code keeps working; the API does not read it.
    document: EntityIdentificationDocument


class Individual:
    """The top-level individual of the Accounts API v2.0 sole trader variants."""
    # The individual's first name.
    # [Required]
    # min 2 characters, max 50 characters
    first_name: str
    # The individual's middle name. Required if it appears in official documents.
    # [Optional]
    # min 2 characters, max 50 characters
    middle_name: str
    # The individual's last name.
    # [Required]
    # min 2 characters, max 50 characters
    last_name: str
    # The trading name of the sub-entity, also referred to as 'doing business as'.
    # [Required]
    # min 2 characters, max 300 characters
    trading_name: str
    # Deprecated: not defined by any Accounts API schema. Retained so existing code keeps working; the
    # API does not read it.
    national_tax_id: str
    # The registered address of the sole trader's business.
    # [Required]
    registered_address: Address
    # The date of birth of the person according to the Gregorian calendar.
    # [Required], except on GB Sole Trader Lite (2.0) where it is [Optional].
    date_of_birth: DateOfBirth
    # The place of birth of the person.
    # [Required] for EEA Sole Trader Full and Lite (2.0); not part of the other v2.0 variants.
    place_of_birth: PlaceOfBirth
    # The individual's identification. US Sole Trader (2.0) only.
    # [Required] for US Sole Trader Full (2.0); [Optional] for US Sole Trader Lite (2.0).
    identification: Identification
    # Seller financial questions and supporting documents. US Sole Trader (2.0) only.
    # [Required] for US Sole Trader Full (2.0); [Optional] for US Sole Trader Lite (2.0).
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
    # For ISV (SaaS seller) sub-entities, a daily schedule runs on working days only
    # (Monday to Friday); payouts do not take place on weekends.
    def __init__(self):
        super().__init__(ScheduleFrequency.DAILY)


class ScheduleFrequencyMonthlyRequest(ScheduleRequest):
    # For ISV (SaaS seller) sub-entities, by_month_day accepts only the combinations
    # [1], [15], [1, 15] or [1, 16], in any order.
    by_month_day: list  # int

    def __init__(self):
        super().__init__(ScheduleFrequency.MONTHLY)


class ScheduleFrequencyWeeklyRequest(ScheduleRequest):
    # For ISV (SaaS seller) sub-entities, by_day accepts working days only
    # (Monday to Friday); payouts set to take place on weekends are rejected.
    by_day: list  # DaySchedule

    def __init__(self):
        super().__init__(ScheduleFrequency.WEEKLY)


class UpdateScheduleRequest:
    enabled: bool
    threshold: int
    # The amount, in the minor units of the schedule's currency, to retain in the
    # sub-entity's available balance. ISV (SaaS seller) sub-entities only. Min 0.
    balance_minimum: int
    # Indicates whether to carry forward any balance below the configured minimum
    # to the next payout. ISV (SaaS seller) sub-entities only.
    carry_forward_enabled: bool
    # The ID of the platforms payment instrument used as the payout destination.
    payment_instrument_id: str
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
