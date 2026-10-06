from enum import Enum
from typing import Dict

from checkout_sdk.common.common import Phone, Address
from checkout_sdk.common.common import ResidentialStatusType, AccountHolderIdentification
from checkout_sdk.common.enums import Currency, InstrumentType, Country, AccountType, AccountHolderType, DocumentType


class ScheduleFrequency(str, Enum):
    """How often funds are paid out to a sub-entity: the recurrence.frequency of a payout schedule."""
    WEEKLY = 'weekly'
    DAILY = 'daily'
    MONTHLY = 'monthly'


class DaySchedule(str, Enum):
    """The days of the week a weekly payout can take place on (by_day). For ISV (SaaS seller)
    sub-entities, only monday to friday are accepted."""
    MONDAY = 'monday'
    TUESDAY = 'tuesday'
    WEDNESDAY = 'wednesday'
    THURSDAY = 'thursday'
    FRIDAY = 'friday'
    SATURDAY = 'saturday'
    SUNDAY = 'sunday'


class BusinessType(str, Enum):
    """The legal type of the company (company.business_type). The union of the values every variant
    accepts; each variant accepts a subset, and the sole trader variants accept
    individual_or_sole_proprietorship only."""
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
    """The roles of a representative within the company (representatives[].roles). Each variant
    accepts a subset: director on GB Company Full (3.0) only; legal_representative on the EEA
    Company variants only; ubo only on the sole trader variants."""
    UBO = 'ubo'
    LEGAL_REPRESENTATIVE = 'legal_representative'
    AUTHORISED_SIGNATORY = 'authorised_signatory'
    DIRECTOR = 'director'
    CONTROL_PERSON = 'control_person'


class CompanyPosition(str, Enum):
    """The position of a representative within the company (representatives[].company_position), on
    EEA, GB and US Company Full (3.0) and US ISV Seller Company (3.0)."""
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
    """The classification of a representative's national identification number
    (individual.national_id_type), US ISV Seller variants (3.0) only."""
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
    # [Required] in every variant that takes email_addresses.
    # Format: email
    primary: str
    # The email address of the person responsible for PCI compliance at this sub-entity.
    # [Required] for the US ISV Seller variants (3.0), together with primary; not part of the other variants.
    # Format: email
    pci_compliance_contact: str


class Invitee:
    """The details of the user responsible for onboarding the sub-entity."""
    # The email of the user responsible for onboarding the sub-entity. The full onboarding variants
    # describe it as the main email address for this sub-entity, but it is the invitee's address.
    # [Required] in the hosted onboarding invite request; [Optional] in the Full and Lite onboarding
    # variants; not part of the US ISV Seller variants.
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
    # [Required] in the hosted onboarding invite request, where it is the only contact detail; [Optional]
    # in the Full and Lite onboarding variants; not part of the US ISV Seller variants.
    invitee: Invitee


class Profile:
    """Information about the profile of the sub-entity, primarily regarding the products and services
    offered."""
    # A collection of website URLs the sub-entity accepts payments on (str items).
    # [Required]
    # max 100 items; each item Format: uri, ^(http|https):\/\/\S{2,293}$, min 4 characters, max 300
    # characters
    urls: list  # str
    # The merchant category codes that most closely describe the business (str items).
    # [Required]
    # min 1 item, max 5 items; each item ^[0-9]{4}$
    mccs: list  # str
    # The default holding currency's three-letter ISO 4217 code.
    # [Required] for every v3.0 variant; [Optional] for the v2.0 Full variants; not part of the v2.0
    # Lite variants.
    # Format: iso-4217. On the US ISV Seller variants (3.0), USD only.
    default_holding_currency: Currency
    # The currencies in which incoming funds are held (Currency items).
    # [Required] for every v3.0 variant; [Optional] for the v2.0 Full variants; not part of the v2.0
    # Lite variants.
    # min 1 item on v3.0. Enum per variant:
    #   GB (3.0): AED, AUD, CAD, CHF, CZK, DKK, EUR, GBP, HKD, JPY, KWD, NOK, NZD, PLN, RON, SEK, SGD,
    #   USD, ZAR
    #   EEA (3.0) and EEA Company Full (2.0): the GB (3.0) list without KWD
    #   US and US ISV Seller (3.0): USD
    holding_currencies: list  # Currency


class EntityDocument:
    """Deprecated: not defined by any Accounts API onboarding schema. Referenced only by
    Company.document and EntityFinancialDocuments, both deprecated; retained so existing code keeps
    working."""
    # Deprecated: see the class docstring.
    file_id: str
    # Deprecated: see the class docstring.
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
    """The date of birth of the person according to the Gregorian calendar."""
    # The calendar day of the month they were born.
    # [Required]
    # min 1, max 31
    day: int
    # The month of the year they were born.
    # [Required]
    # min 1, max 12
    month: int
    # The year they were born.
    # [Required]
    # min 1900, max 2999
    year: int


class PlaceOfBirth:
    """The place of birth of the person."""
    # The country code (iso-3166-1 alpha-2).
    # [Required]
    # Format: iso-3166-1-alpha-2
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

    These four are the only keys any variant defines, and which apply depends on the onboarding
    variant: EEA Sole Trader Full (3.0) requires identity_verification, proof_of_residential_address
    and proof_of_registration; GB and US Sole Trader Full (3.0) require identity_verification; the
    EEA, GB and US Company Full (3.0) variants (person of interest) and US ISV Seller Company (3.0)
    accept identity_verification and certified_authorised_signatory, both optional; US ISV Seller
    Sole Trader (3.0) accepts identity_verification, optional.

    The API validates this object strictly (additionalProperties false), rejecting a key it does not
    recognise rather than ignoring it, only on the EEA, GB and US Company Full (3.0) person of
    interest and the EEA, GB and US Sole Trader Full (3.0) variants. It is not strict on the US ISV
    Seller variants (3.0) nor on v2.0.

    The v2.0 company representatives use this class too, with identity_verification only.

    Leave an attribute unset rather than assigning None: an attribute set to None is sent as null.
    """
    # The document to use to confirm the individual's identity.
    # [Optional] (required for the sole trader full variants)
    identity_verification: EntityIdentificationDocument
    # Certified authorised signatory document. Required when the legal representative or other role
    # owner is not registered on the certificate of incorporation.
    # [Optional] (EEA, GB and US Company Full (3.0) and US ISV Seller Company (3.0) only)
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
    # Verification documents for the individual representative. See RepresentativeDocuments: on the
    # EEA, GB and US Company Full (3.0) person of interest and the EEA, GB and US Sole Trader Full
    # (3.0) variants the API validates this object strictly and rejects any key the variant does not
    # define; on the US ISV Seller variants (3.0) and v2.0 it is not strict.
    # [Required] for the EEA, GB and US Sole Trader Full (3.0) variants and EEA Company Full (2.0);
    # [Optional] otherwise.
    documents: RepresentativeDocuments
    # The controlling company, when the representative is a company rather than an individual.
    # [Required] for a controlling company representative (EEA and GB Company Full (3.0) only).
    # The API reads only three attributes here, all [Required]: legal_name, trading_name and
    # registered_address. Leave the other Company attributes unset.
    company: 'Company'
    # v2.0 only, deprecated; use `individual` for v3.0
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
    """Deprecated: not defined by any Accounts API schema. financial_details carries the three amounts
    and the currency only. Retained so existing code keeps working."""
    # Deprecated: see the class docstring.
    bank_statement: EntityDocument
    # Deprecated: see the class docstring.
    financial_statement: EntityDocument


class EntityFinancialDetails:
    """Seller financial questions (financial_details): on the company of EEA and US Company Full and
    Lite (2.0), and on the individual of US Sole Trader Full and Lite (2.0)."""
    # The estimated annual processing volume. In minor units without decimals.
    # [Required] on the Full (2.0) variants; [Optional] on the Lite (2.0) variants.
    # min 0
    annual_processing_volume: int
    # The expected average transaction value. In minor units without decimals.
    # [Required] on the Full (2.0) variants; [Optional] on the Lite (2.0) variants.
    # min 0
    average_transaction_value: int
    # The expected highest transaction value. In minor units without decimals.
    # [Required] on the Full (2.0) variants; [Optional] on the Lite (2.0) variants.
    # min 0
    highest_transaction_value: int
    # Deprecated: not defined by any Accounts API schema; the API does not read it. Supporting
    # documents go on the top-level request documents (OnboardSubEntityDocuments) instead.
    documents: EntityFinancialDocuments
    # The currency used for the financial details provided.
    # [Required] on US Company Full and US Sole Trader Full (2.0); [Optional] on the other variants.
    currency: Currency


class DateOfIncorporation:
    """The date the company was incorporated, or the date the sole trader started trading."""
    # The day of the month the company was incorporated.
    # [Optional]
    # min 1, max 31
    day: int
    # The month the company was incorporated.
    # [Required]
    # min 1, max 12
    month: int
    # The year the company was incorporated.
    # [Required]
    # min 1500, max 2999
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
    """ACH payment processing details (processing_details.payments.ach), US ISV Seller variants (3.0)
    only."""
    # The estimated annual ACH processing volume in minor units without decimals.
    # [Required]
    # min 0
    annual_ach_volume: int
    # The expected average ACH transaction size in minor units without decimals.
    # [Required]
    # min 0
    average_ach_transaction_size: int
    # The estimated monthly volume of ACH credit transactions (for example, refunds issued to
    # customers) in minor units without decimals.
    # [Required]
    # min 0
    estimated_monthly_credit_volume: int
    # The average value of an ACH credit transaction (for example, a refund) in minor units without
    # decimals.
    # [Required]
    # min 0
    average_credit_amount: int


class ProcessingDetailsPayments:
    """Payment method-specific processing details (processing_details.payments), US ISV Seller
    variants (3.0) only."""
    # ACH payment processing details.
    # [Required]
    ach: ProcessingDetailsAch


class ProcessingDetails:
    """Information about the sub-entity's expected processing (processing_details). Part of every
    Accounts API v3.0 variant; not part of v2.0."""
    # The country code (iso-3166-1 alpha-2) where the settlement bank account is located.
    # [Required] for EEA, GB and US Company and Sole Trader Full (3.0); not part of the US ISV Seller
    # variants.
    # Format: iso-3166-1-alpha-2
    # [a-zA-Z]{2}
    # 2 characters
    settlement_country: str
    # Target country codes (iso-3166-1 alpha-2) with more than 10% expected volume processing with
    # Checkout.com (str items).
    # [Required]
    # min 1 item, max 10 items; each item Format: iso-3166-1-alpha-2, [a-zA-Z]{2}, 2 characters
    target_countries: list  # str
    # The estimated annual processing volume. In minor units without decimals.
    # [Required]
    # min 0
    annual_processing_volume: int
    # The expected average transaction value. In minor units without decimals.
    # [Required]
    # min 0
    average_transaction_value: int
    # The average time in days between accepting payment and fulfilling the order.
    # [Required] for the US ISV Seller variants (3.0); not part of the other variants.
    # min 0
    average_order_fulfillment_time: int
    # The expected highest transaction value. In minor units without decimals.
    # [Required] for EEA, GB and US Company and Sole Trader Full (3.0); not part of the US ISV Seller
    # variants.
    # min 0
    highest_transaction_value: int
    # The currency used for the processing details provided.
    # [Required]
    # Enum per variant: GBP on the GB variants, EUR on the EEA variants, USD on the US and US ISV
    # Seller variants.
    currency: Currency
    # Payment method-specific processing details.
    # [Required] for the US ISV Seller variants (3.0); not part of the other variants.
    payments: ProcessingDetailsPayments


class AdditionalInfo:
    """Deprecated: not defined by any Accounts API onboarding schema. Referenced only by
    OnboardEntityRequest.additional_info; retained so existing code keeps working."""
    # Deprecated: see the class docstring.
    field1: str
    # Deprecated: see the class docstring.
    field2: str
    # Deprecated: see the class docstring.
    field3: str


class AgreedTerms:
    """Details of the person (or sole trader) who agreed to the terms and conditions on behalf of the
    sub-entity, captured as evidence of consent to Checkout.com onboarding (agreed_terms). US ISV
    Seller variants (3.0) only."""
    # Date and time the terms were agreed in RFC 3339 or ISO 8601 format.
    # [Required]
    # Format: date-time
    date: str
    # IP address (IPv4 or IPv6) of the person at the time they agreed the terms.
    # [Required]
    ip_address: str
    # First and last name of the person who agreed to the terms.
    # [Required]
    name: str
    # Email address of the person who agreed to the terms.
    # [Required]
    # Format: email
    email: str
    # Identifier of the terms version that was agreed.
    # [Required]
    version: str


class SchemaVersionHeader:
    """The Accept header that selects the Accounts API payload version, for example
    'application/json;schema_version=3.0'. Built by AccountsClient from its schema_version argument."""
    # The Accept header value: application/json with a schema_version parameter.
    accept: str

    def get_header_mappings(self) -> Dict[str, str]:
        return {
            'accept': 'Accept'
        }


class OnboardEntityRequest:
    """The request body of POST /accounts/entities (onboard a sub-entity) and PUT
    /accounts/entities/{id} (update a sub-entity). One class covers every variant the API defines:
    the Accounts API v3.0 and v2.0 company and sole trader variants (EEA, GB and US, Full and Lite),
    the US ISV Seller variants (3.0), and the hosted onboarding invite request, which takes only
    reference, is_draft and contact_details (with invitee). Select the version with the
    schema_version argument of the client method. Leave unset the attributes the chosen variant does
    not define."""
    # A unique reference you can later use to identify the sub-entity. Immutable after creation.
    # [Required]
    # min 1 character, max 50 characters
    reference: str
    # Specifies whether the sub-entity details are in draft. Marking a sub-entity as a draft allows
    # its details to be updated without triggering due diligence checks. On the US ISV Seller
    # variants, POST always creates the sub-entity in Draft regardless of this field.
    # [Required] in the hosted onboarding invite request; [Optional] in the other variants.
    is_draft: bool
    # Information about the profile of the sub-entity, primarily regarding the products and services
    # offered.
    # [Required] for every variant except the hosted onboarding invite request, which does not take
    # it.
    profile: Profile
    # Contact details of this sub-entity.
    # [Required] for every variant except EEA Company Full (3.0), where it is [Optional]. In the
    # hosted onboarding invite request it carries invitee only.
    contact_details: ContactDetails
    # Information about the company represented by the sub-entity, or about the sole trader's
    # business on the v3.0 sole trader variants.
    # [Required] for every company variant and every v3.0 sole trader variant, US ISV Seller
    # included; not part of the v2.0 sole trader variants (they use individual) nor the hosted
    # onboarding invite request.
    company: Company
    # Information about the sub-entity's expected processing.
    # [Required] for every v3.0 variant; not part of v2.0 nor the hosted onboarding invite request.
    processing_details: ProcessingDetails
    # Details of the person who agreed to the terms and conditions on behalf of the sub-entity.
    # [Required] for the US ISV Seller variants (3.0); not part of the other variants.
    agreed_terms: AgreedTerms
    # The identifier of a seller category set up for your platform. Seller categories define the
    # pricing, capabilities and risk profile applied to sub-entities, and are configured during your
    # platform's onboarding with Checkout.com; contact your account manager for the list of available
    # identifiers.
    # [Required] for the US ISV Seller variants (3.0); not part of the other variants.
    seller_category: str
    # The documents used to support the verification of the company or business details.
    # [Required] for EEA, GB and US Company Full (3.0), EEA, GB and US Sole Trader Full (3.0), EEA
    # Company Full (2.0) and EEA Sole Trader Full (2.0); [Optional] for the other variants, US ISV
    # Seller included. Not part of the hosted onboarding invite request.
    documents: OnboardSubEntityDocuments
    # Deprecated: not defined by any Accounts API onboarding schema. Retained so existing code keeps
    # working; the API does not document reading it.
    additional_info: AdditionalInfo
    # v2.0 only, deprecated; a v3.0 sole trader is onboarded as a `company` with representatives.
    # Information about the individual represented by the sub-entity.
    # [Required] for the six v2.0 sole trader variants (EEA, GB and US, Full and Lite); not part of
    # the other variants.
    individual: Individual


class InstrumentDocument:
    """A legal document used to verify the bank account (document): on a bank_account
    PaymentInstrumentRequest, and on the deprecated AccountsPaymentInstrument."""
    # The document type. Enum: bank_statement.
    # [Optional] (defaults to bank_statement)
    type: str
    # The file ID of the uploaded document. The document must have been uploaded for the purpose of
    # bank_verification.
    # [Optional]
    file_id: str


class InstrumentDetails:
    """Details of the payment instrument being created (instrument_details). Base class: use
    InstrumentDetailsFasterPayments, InstrumentDetailsSepa or InstrumentDetailsAch for a bank_account
    instrument, and InstrumentDetailsCardToken for a card_token instrument."""


class InstrumentDetailsFasterPayments(InstrumentDetails):
    """Faster Payments bank account details of a bank_account payment instrument."""
    # The alphanumeric value that identifies the account.
    # [Required]
    account_number: str
    # The code that identifies the bank.
    # [Required]
    bank_code: str


class InstrumentDetailsSepa(InstrumentDetails):
    """SEPA bank account details of a bank_account payment instrument."""
    # The account's International Bank Account Number (IBAN).
    # [Required]
    # min 5 characters, max 34 characters
    iban: str
    # An 8 or 11 character code that identifies the bank or bank branch.
    # [Required]
    # Format: ISO 9362:2009
    swift_bic: str


class InstrumentDetailsCardToken(InstrumentDetails):
    """Card details of a card_token payment instrument."""
    # The token that identifies the card.
    # [Required]
    token: str


class InstrumentAccountType(str, Enum):
    """The type of bank account of an ACH payment instrument (instrument_details.account_type)."""
    SAVINGS = 'savings'
    CHECKING = 'checking'


class InstrumentDetailsAch(InstrumentDetails):
    """ACH bank account details of a bank_account payment instrument."""
    # The alphanumeric value that identifies the account.
    # [Required]
    account_number: str
    # The 9-digit American Bankers Association (ABA) routing number that identifies the financial
    # institution.
    # [Required]
    # ^[0-9]{9}$
    routing_number: str
    # The type of bank account.
    # [Required]
    account_type: InstrumentAccountType


class BankDetails:
    """Deprecated: part of the deprecated AccountsPaymentInstrument (AccountsPaymentInstrument.bank)
    only; retained so existing code keeps working. Not the shared common.common.BankDetails."""
    # Deprecated: see the class docstring.
    name: str
    # Deprecated: see the class docstring.
    branch: str
    # Deprecated: see the class docstring.
    address: Address


class AccountsAccountHolder:
    """Deprecated: the account holder of the deprecated AccountsPaymentInstrument
    (AccountsPaymentInstrument.account_holder) only; retained so existing code keeps working. Use
    AccountsCorporateAccountHolder or AccountsIndividualAccountHolder."""
    # Deprecated: see the class docstring.
    type: AccountHolderType
    # Deprecated: see the class docstring.
    tax_id: str
    # Deprecated: see the class docstring.
    date_of_birth: DateOfBirth
    # Deprecated: see the class docstring.
    country_of_birth: Country
    # Deprecated: see the class docstring.
    residential_status: ResidentialStatusType
    # Deprecated: see the class docstring.
    billing_address: Address
    # Deprecated: see the class docstring.
    phone: Phone
    # Deprecated: see the class docstring.
    identification: AccountHolderIdentification
    # Deprecated: see the class docstring.
    email: str


class AccountsCorporateAccountHolder(AccountsAccountHolder):
    """Deprecated: a corporate account holder of the deprecated AccountsPaymentInstrument; see
    AccountsAccountHolder."""
    # Deprecated: see the class docstring.
    company_name: str


class AccountsIndividualAccountHolder(AccountsAccountHolder):
    """Deprecated: an individual account holder of the deprecated AccountsPaymentInstrument; see
    AccountsAccountHolder."""
    # Deprecated: see the class docstring.
    first_name: str
    # Deprecated: see the class docstring.
    last_name: str


class AccountsPaymentInstrument:
    """Deprecated: the request body of AccountsClient.create_payment_instrument (POST
    /accounts/entities/{id}/instruments), itself deprecated in favour of add_payment_instrument. The
    API reference does not describe this endpoint. Use PaymentInstrumentRequest with
    add_payment_instrument instead; retained so existing code keeps working."""
    # Deprecated: see the class docstring. Always bank_account.
    type = InstrumentType.BANK_ACCOUNT
    # Deprecated: see the class docstring.
    label: str
    # Deprecated: see the class docstring.
    account_type: AccountType
    # Deprecated: see the class docstring.
    account_number: str
    # Deprecated: see the class docstring.
    bank_code: str
    # Deprecated: see the class docstring.
    branch_code: str
    # Deprecated: see the class docstring.
    iban: str
    # Deprecated: see the class docstring.
    bban: str
    # Deprecated: see the class docstring.
    swift_bic: str
    # Deprecated: see the class docstring.
    currency: Currency
    # Deprecated: see the class docstring.
    country: Country
    # Deprecated: see the class docstring.
    document: InstrumentDocument
    # Deprecated: see the class docstring.
    account_holder: AccountsAccountHolder
    # Deprecated: see the class docstring.
    bank: BankDetails


class PaymentInstrumentRequest:
    """The request body of POST /accounts/entities/{id}/payment-instruments (add a payment
    instrument), PlatformsPaymentInstrumentCreate. Two variants, selected by type: bank_account and
    card_token."""
    # A reference that you can use to identify the payment instrument.
    # [Required]
    # min 1 character, max 50 characters
    label: str
    # The instrument type. Enum: bank_account, card_token.
    # [Required]
    type: InstrumentType
    # The account's currency, as a three-letter ISO 4217 currency code.
    # [Required]
    # Format: ISO 4217
    # 3 characters
    currency: Currency
    # The account's country, as a two-letter ISO country code.
    # [Required] for bank_account; not part of card_token.
    # Format: ISO 3166-1
    country: Country
    # Deprecated: specifies whether the payment instrument should be set as the default payout
    # destination. For ad-hoc payouts, the payment instrument is explicitly specified in the payout
    # request; for scheduled payouts, the first payment instrument created for a given currency is
    # used for that currency's payout schedule. To change it, update the payout schedule.
    # [Optional] (bank_account only)
    default: bool
    # A legal document used to verify the bank account.
    # [Required] for bank_account; not part of card_token.
    document: InstrumentDocument
    # Details of the payment instrument being created: InstrumentDetailsFasterPayments,
    # InstrumentDetailsSepa or InstrumentDetailsAch for bank_account; InstrumentDetailsCardToken for
    # card_token.
    # [Required]
    instrument_details: InstrumentDetails


class Headers:
    """The headers object of PlatformsPaymentInstrumentUpdate (UpdatePaymentInstrumentRequest.headers).
    The API reference models it inside the request body, with the key if-match, but the API reads the
    ETag only from the If-Match HTTP header. AccountsClient.update_payment_instrument sends it as that
    header."""
    # The payment instrument ETag value, as returned in the ETag header of the GET. Sent as the If-Match
    # HTTP header; the update fails with 428 when it is missing and 412 when it does not match.
    # [Required]
    if_match: str


class UpdatePaymentInstrumentRequest:
    """The request body of PATCH /accounts/entities/{entityId}/payment-instruments/{id} (update a
    payment instrument), PlatformsPaymentInstrumentUpdate."""
    # A reference that you can use to identify the payment instrument.
    # [Optional]
    # min 1 character, max 50 characters
    label: str
    # Deprecated: specifies whether the payment instrument should be set as the default payout
    # destination. For scheduled payouts, the first payment instrument created for a given currency
    # is used for that currency's payout schedule; to change it, update the payout schedule.
    # [Optional]
    default: bool
    # The payment instrument ETag, sent as the If-Match HTTP header.
    # [Required] by the API: the update fails with 428 Precondition Required without it.
    headers: Headers


class ScheduleRequest:
    """Information about how often the payout schedule takes place (recurrence). Base class, selected
    by frequency: use ScheduleFrequencyDailyRequest, ScheduleFrequencyWeeklyRequest or
    ScheduleFrequencyMonthlyRequest."""
    # Used to indicate how often funds should be paid out to a sub-entity. Enum: daily, weekly,
    # monthly. For ISV (SaaS seller) sub-entities, the payout is based on the sub-entity's available
    # balance as of 00:00 in the sub-entity's time zone.
    # [Required]
    frequency: ScheduleFrequency

    def __init__(self, frequency_p: ScheduleFrequency):
        self.frequency = frequency_p


class ScheduleFrequencyDailyRequest(ScheduleRequest):
    """A daily payout schedule (frequency daily). For ISV (SaaS seller) sub-entities, a daily schedule
    runs on working days only (Monday to Friday); payouts do not take place on weekends."""
    def __init__(self):
        super().__init__(ScheduleFrequency.DAILY)


class ScheduleFrequencyMonthlyRequest(ScheduleRequest):
    """A monthly payout schedule (frequency monthly)."""
    # The day or days of the month the payout should take place (int items).
    # [Required]
    # each item min 1, max 28.
    # For ISV (SaaS seller) sub-entities, by_month_day accepts only the combinations
    # [1], [15], [1, 15] or [1, 16], in any order (min 1 item, max 2 items).
    by_month_day: list  # int

    def __init__(self):
        super().__init__(ScheduleFrequency.MONTHLY)


class ScheduleFrequencyWeeklyRequest(ScheduleRequest):
    """A weekly payout schedule (frequency weekly)."""
    # The day or days of the week the payout should take place (DaySchedule items).
    # [Required]
    # Enum: monday, tuesday, wednesday, thursday, friday, saturday, sunday.
    # For ISV (SaaS seller) sub-entities, by_day accepts working days only
    # (Monday to Friday); payouts set to take place on weekends are rejected.
    by_day: list  # DaySchedule

    def __init__(self):
        super().__init__(ScheduleFrequency.WEEKLY)


class UpdateScheduleRequest:
    """The payout schedule for one currency, in PUT /accounts/entities/{id}/payout-schedules. The
    client sends it keyed by the currency's three-letter ISO 4217 code. One class covers both
    variants the API defines: Standard and SaaS seller (ISV)."""
    # Indicates whether the payout schedule is enabled.
    # [Required] for ISV (SaaS seller) sub-entities; [Optional] otherwise.
    enabled: bool
    # The minimum available balance required for a payout to take place; below it, Checkout.com does
    # not send the payout instruction. For ISV (SaaS seller) sub-entities, in the minor units of the
    # schedule's currency, and defaults to 0 if you do not set it.
    # [Optional]
    threshold: int
    # The amount, in the minor units of the schedule's currency, to retain in the
    # sub-entity's available balance. ISV (SaaS seller) sub-entities only. Checkout.com pays out only
    # the funds above it, and generates no payout otherwise. Defaults to 0 if you do not set it.
    # [Optional] (ISV (SaaS seller) sub-entities only)
    # min 0
    balance_minimum: int
    # Indicates whether to carry forward any balance below the configured minimum
    # to the next payout. ISV (SaaS seller) sub-entities only.
    # Defaults to False if you do not set it.
    # [Optional] (ISV (SaaS seller) sub-entities only)
    carry_forward_enabled: bool
    # The ID of the platforms payment instrument used as the payout destination.
    # For ISV (SaaS seller) sub-entities, if included it must reference a verified payment
    # instrument, otherwise the request fails.
    # [Optional]
    payment_instrument_id: str
    # Information about how often the schedule takes place.
    # [Required] for ISV (SaaS seller) sub-entities; [Optional] otherwise.
    recurrence: ScheduleRequest


class PaymentInstrumentsQuery:
    """The query parameters of GET /accounts/entities/{id}/payment-instruments."""
    # The status of the sub-entity's payment instrument: its stage of verification, and whether it
    # can be used for payouts. Enum: pending, verified, unverified.
    # [Optional]
    status: str


class ReserveRuleType(str, Enum):
    """The type of a reserve rule (ReserveRuleRequest.type)."""
    ROLLING = 'rolling'


class HoldingDuration:
    """The length of time the collateral balance will be reserved for."""
    # The number of weeks the collateral balance is reserved for.
    # [Required]
    # min 2, max 104
    weeks: int


class RollingReserveRule:
    """The rolling reserve rule details (rolling)."""
    # The percentage of captured funds that will be reserved as a collateral balance.
    # [Required]
    # min 0, max 100
    percentage: float
    # The length of time the collateral balance will be reserved for.
    # [Required]
    holding_duration: HoldingDuration


class ReserveRuleRequest:
    """The request body of POST /accounts/entities/{id}/reserve-rules (ReserveRuleCreateRequest) and
    PUT /accounts/entities/{entityId}/reserve-rules/{id} (ReserveRuleUpdateRequest, sent with the
    If-Match header from the etag argument)."""
    # The reserve rule type. Enum: rolling.
    # [Required]
    type: ReserveRuleType
    # The rolling reserve rule details.
    # [Required]
    rolling: RollingReserveRule
    # The date and time the reserve rule will come into effect. Must be at least 15 minutes in the
    # future.
    # [Required] on create; not part of the update request.
    # Format: date-time
    valid_from: str


class FilePurpose(str, Enum):
    """The purpose of a sub-entity file upload (POST /entities/{entity_id}/files). The fourteen values
    the endpoint accepts (PlatformsFileUpload), plus two that it does not, noted below."""
    ADDITIONAL_DOCUMENT = 'additional_document'
    ARTICLES_OF_ASSOCIATION = 'articles_of_association'
    BANK_VERIFICATION = 'bank_verification'
    CERTIFIED_AUTHORISED_SIGNATORY = 'certified_authorised_signatory'
    COMPANY_OWNERSHIP = 'company_ownership'
    # Not an onboarding upload purpose: not among the values PlatformsFileUpload defines. Use
    # IDENTITY_VERIFICATION.
    IDENTIFICATION = 'identification'
    IDENTITY_VERIFICATION = 'identity_verification'
    # Not an onboarding upload purpose: POST /entities/{entity_id}/files does not accept it.
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
    """The request body of POST /entities/{entity_id}/files (PlatformsFileUpload)."""
    # The purpose of the file upload: the onboarding document the file is for.
    # [Required]
    purpose: FilePurpose


class EntityRequirementUpdateRequest:
    """The request body of PUT /accounts/entities/{id}/requirements/{requirementId} (resolve a
    requirement). The shape of value is defined by the requirement's _schema, returned from GET
    /accounts/entities/{id}/requirements/{requirementId}."""
    # The response to the requirement. The expected shape depends on the requirement and is defined
    # by the JSON Schema returned in the requirement details response. Common shapes include a file
    # reference (for document uploads), a primitive value, or a structured object. One of: object,
    # array, string, number, boolean.
    # [Required]
    value: object


class EtagHeader:
    """The If-Match header of PUT /accounts/entities/{entityId}/reserve-rules/{id}. Built by
    AccountsClient.update_reserve_rule from its etag argument."""
    # Identifies a specific version of a reserve rule to update.
    # [Required]
    etag: str

    def get_header_mappings(self) -> Dict[str, str]:
        return {
            'etag': 'If-Match'
        }
