import json

from checkout_sdk.checkout_response import ResponseWrapper
from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.common.common import Address, Phone
from checkout_sdk.common.enums import Country, Currency, DocumentType
from checkout_sdk.accounts.accounts import (
    ProcessingDetails, ProcessingDetailsPayments, ProcessingDetailsAch,
    AgreedTerms, Company, BusinessType, DateOfIncorporation,
    EntityRepresentative, RepresentativeIndividual, Citizenship, NationalIdType,
    CompanyPosition, EntityRoles, FinancialStatements, FinancialStatementsType,
    OnboardSubEntityDocuments, OnboardEntityRequest,
    EntityIdentificationDocument, CompanyVerification, CompanyVerificationType,
    ArticlesOfAssociation, ArticlesOfAssociationType, BankVerification, BankVerificationType,
    ShareholderStructure, ShareholderStructureType, ProofOfLegality, ProofOfLegalityType,
    ProofOfPrincipalAddress, ProofOfPrincipalAddressType, AdditionalDocument,
    TaxVerification, TaxVerificationType, FinancialVerification, FinancialVerificationType,
    RepresentativeDocuments, CertifiedAuthorisedSignatory, CertifiedAuthorisedSignatoryType,
    ProofOfResidentialAddress, ProofOfResidentialAddressType, ProofOfRegistration, ProofOfRegistrationType,
    FilePurpose, EntityEmailAddresses, ContactDetails, Invitee, Profile, DateOfBirth, PlaceOfBirth,
    EntityFinancialDetails, Individual, Identification, EntityIdentification, EntityFileRequest,
)


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class TestAccountsV3Serialization:

    # The US ISV Seller (3.0) processing details: USD only, with average_order_fulfillment_time and
    # payments.ach, and without the settlement_country and highest_transaction_value the other
    # v3.0 variants take.
    def test_serializes_processing_details_with_payments(self):
        ach = ProcessingDetailsAch()
        ach.annual_ach_volume = 1000000
        ach.average_ach_transaction_size = 5000
        ach.estimated_monthly_credit_volume = 100000
        ach.average_credit_amount = 5000
        payments = ProcessingDetailsPayments()
        payments.ach = ach
        details = ProcessingDetails()
        details.annual_processing_volume = 1000000
        details.average_transaction_value = 5000
        details.average_order_fulfillment_time = 3
        details.currency = Currency.USD
        details.target_countries = ['US']
        details.payments = payments

        assert _serialize(details) == {
            'annual_processing_volume': 1000000,
            'average_transaction_value': 5000,
            'average_order_fulfillment_time': 3,
            'currency': 'USD',
            'target_countries': ['US'],
            'payments': {
                'ach': {
                    'annual_ach_volume': 1000000,
                    'average_ach_transaction_size': 5000,
                    'estimated_monthly_credit_volume': 100000,
                    'average_credit_amount': 5000,
                }
            },
        }

    # The US ISV Seller variants (3.0) require pci_compliance_contact next to primary.
    def test_serializes_entity_email_addresses_with_pci_compliance_contact(self):
        email_addresses = EntityEmailAddresses()
        email_addresses.primary = 'admin@superhero1234.com'
        email_addresses.pci_compliance_contact = 'pci@superhero1234.com'

        body = json.dumps(email_addresses, cls=JsonSerializer)

        assert json.loads(body) == {
            'primary': 'admin@superhero1234.com',
            'pci_compliance_contact': 'pci@superhero1234.com',
        }
        # Key-level check on the raw body, so a naming change cannot pass silently.
        assert '"pci_compliance_contact": "pci@superhero1234.com"' in body

    def test_serializes_agreed_terms(self):
        agreed_terms = AgreedTerms()
        agreed_terms.date = '2026-07-20T10:00:00Z'
        agreed_terms.ip_address = '203.0.113.42'
        agreed_terms.name = 'John Representative'
        agreed_terms.email = 'john@example.com'
        agreed_terms.version = '1.0'

        assert _serialize(agreed_terms) == {
            'date': '2026-07-20T10:00:00Z',
            'ip_address': '203.0.113.42',
            'name': 'John Representative',
            'email': 'john@example.com',
            'version': '1.0',
        }

    # US ISV Seller Sole Trader (3.0) is the only variant with is_registered_company, and it allows
    # only false, together with business_type individual_or_sole_proprietorship.
    def test_serializes_company_v3_fields(self):
        date_of_incorporation = DateOfIncorporation()
        date_of_incorporation.day = 1
        date_of_incorporation.month = 6
        date_of_incorporation.year = 2010
        company = Company()
        company.trading_name = 'Super Hero Masks'
        company.business_type = BusinessType.INDIVIDUAL_OR_SOLE_PROPRIETORSHIP
        company.additional_trading_names = ['SHM']
        company.is_registered_company = False
        company.date_of_incorporation = date_of_incorporation

        assert _serialize(company) == {
            'trading_name': 'Super Hero Masks',
            'business_type': 'individual_or_sole_proprietorship',
            'additional_trading_names': ['SHM'],
            'is_registered_company': False,
            'date_of_incorporation': {'day': 1, 'month': 6, 'year': 2010},
        }

    def test_serializes_representative_v3_fields(self):
        citizenship = Citizenship()
        citizenship.type = 'citizenship'
        citizenship.country = Country.US
        individual = RepresentativeIndividual()
        individual.first_name = 'John'
        individual.last_name = 'Doe'
        individual.citizenships = [citizenship]
        individual.national_id_type = NationalIdType.SSN
        individual.national_id_number = '123456789'
        individual.email_address = 'john@example.com'
        representative = EntityRepresentative()
        representative.id = 'rep_be6xo4i6ia8mq7vz27su1ma6li'
        representative.individual = individual
        representative.company_position = CompanyPosition.CEO
        representative.ownership_percentage = 100
        representative.roles = [EntityRoles.UBO, EntityRoles.AUTHORISED_SIGNATORY,
                                EntityRoles.DIRECTOR, EntityRoles.CONTROL_PERSON]

        assert _serialize(representative) == {
            'id': 'rep_be6xo4i6ia8mq7vz27su1ma6li',
            'individual': {
                'first_name': 'John',
                'last_name': 'Doe',
                'citizenships': [{'type': 'citizenship', 'country': 'US'}],
                'national_id_type': 'ssn',
                'national_id_number': '123456789',
                'email_address': 'john@example.com',
            },
            'company_position': 'ceo',
            'ownership_percentage': 100,
            'roles': ['ubo', 'authorised_signatory', 'director', 'control_person'],
        }

    def test_serializes_representative_documents(self):
        identity = EntityIdentificationDocument()
        identity.type = DocumentType.PASSPORT
        identity.front = 'file_ebxawxm4fesbgqtwtiuikwdviu'
        identity.back = 'file_3wb62nghcba73hmzz7rxfdpgtp'
        signatory = CertifiedAuthorisedSignatory()
        signatory.type = CertifiedAuthorisedSignatoryType.POWER_OF_ATTORNEY
        signatory.front = 'file_trjpkykozlhwurcfeie24lpp52'
        residential = ProofOfResidentialAddress()
        residential.type = ProofOfResidentialAddressType.PROOF_OF_ADDRESS
        residential.front = 'file_5dzmhwq66uettzacvm23zde6cj'
        registration = ProofOfRegistration()
        registration.type = ProofOfRegistrationType.EXTRACT_FROM_TRADE_REGISTER
        registration.front = 'file_hgf4rera4kdlmuv7nb4ehzkr5a'
        documents = RepresentativeDocuments()
        documents.identity_verification = identity
        documents.certified_authorised_signatory = signatory
        documents.proof_of_residential_address = residential
        documents.proof_of_registration = registration

        assert _serialize(documents) == {
            'identity_verification': {
                'type': 'passport',
                'front': 'file_ebxawxm4fesbgqtwtiuikwdviu',
                'back': 'file_3wb62nghcba73hmzz7rxfdpgtp',
            },
            'certified_authorised_signatory': {'type': 'power_of_attorney', 'front': 'file_trjpkykozlhwurcfeie24lpp52'},
            'proof_of_residential_address': {'type': 'proof_of_address', 'front': 'file_5dzmhwq66uettzacvm23zde6cj'},
            'proof_of_registration': {
                'type': 'extract_from_trade_register', 'front': 'file_hgf4rera4kdlmuv7nb4ehzkr5a'},
        }

    # Regression: EEA Sole Trader (3.0) needs proof_of_residential_address and proof_of_registration
    # on the representative, with bank_verification alone at the top level.
    def test_serializes_eea_sole_trader_representative_documents(self):
        identity = EntityIdentificationDocument()
        identity.type = DocumentType.PASSPORT
        identity.front = 'file_identityverificationaaaaaa'
        residential = ProofOfResidentialAddress()
        residential.type = ProofOfResidentialAddressType.PROOF_OF_ADDRESS
        residential.front = 'file_proofofresidentialaddressa'
        registration = ProofOfRegistration()
        registration.type = ProofOfRegistrationType.EXTRACT_FROM_TRADE_REGISTER
        registration.front = 'file_proofofregistrationaaaaaaa'
        rep_documents = RepresentativeDocuments()
        rep_documents.identity_verification = identity
        rep_documents.proof_of_residential_address = residential
        rep_documents.proof_of_registration = registration
        individual = RepresentativeIndividual()
        individual.first_name = 'Jane'
        individual.last_name = 'Doe'
        representative = EntityRepresentative()
        representative.individual = individual
        representative.roles = [EntityRoles.UBO]
        representative.documents = rep_documents
        company = Company()
        company.business_type = BusinessType.INDIVIDUAL_OR_SOLE_PROPRIETORSHIP
        company.representatives = [representative]
        bank = BankVerification()
        bank.type = BankVerificationType.BANK_STATEMENT
        bank.front = 'file_bankverificationaaaaaaaaaa'
        documents = OnboardSubEntityDocuments()
        documents.bank_verification = bank
        request = OnboardEntityRequest()
        request.reference = 'ref_sole_trader'
        request.company = company
        request.documents = documents

        body = json.dumps(request, cls=JsonSerializer)
        result = json.loads(body)

        assert result['company']['representatives'][0]['documents'] == {
            'identity_verification': {'type': 'passport', 'front': 'file_identityverificationaaaaaa'},
            'proof_of_residential_address': {'type': 'proof_of_address', 'front': 'file_proofofresidentialaddressa'},
            'proof_of_registration': {
                'type': 'extract_from_trade_register', 'front': 'file_proofofregistrationaaaaaaa'},
        }
        assert result['documents'] == {
            'bank_verification': {'type': 'bank_statement', 'front': 'file_bankverificationaaaaaaaaaa'}}
        # Key-level check on the raw body, so a naming change cannot pass silently.
        assert '"proof_of_residential_address": {' in body
        assert '"proof_of_registration": {' in body

    # No variant defines a key on company.representatives[].documents other than these four, and the
    # EEA, GB and US Company Full (3.0) person of interest and Sole Trader Full (3.0) variants reject
    # unknown keys (additionalProperties: false), so an attribute added here by mistake would fail
    # the request on those variants.
    def test_representative_documents_declares_only_the_keys_the_api_accepts(self):
        assert list(RepresentativeDocuments.__annotations__) == [
            'identity_verification',
            'certified_authorised_signatory',
            'proof_of_residential_address',
            'proof_of_registration',
        ]

    # Leaving an attribute unset omits it; assigning None sends null, which the docstring on
    # RepresentativeDocuments warns about.
    def test_representative_documents_unset_attributes_are_omitted_and_none_is_sent(self):
        registration = ProofOfRegistration()
        registration.type = ProofOfRegistrationType.OTHER
        registration.front = 'file_proofofregistrationaaaaaaa'
        documents = RepresentativeDocuments()
        documents.proof_of_registration = registration

        assert _serialize(documents) == {
            'proof_of_registration': {'type': 'other', 'front': 'file_proofofregistrationaaaaaaa'}}

        documents.identity_verification = None
        assert _serialize(documents)['identity_verification'] is None

    # EEA and GB Company Full (3.0) allow a representative that is a company:
    # { company: { legal_name, trading_name, registered_address }, ownership_percentage }.
    def test_serializes_controlling_company_representative(self):
        address = Address()
        address.address_line1 = '1 Main Street'
        address.city = 'London'
        address.zip = 'W1T 4TJ'
        address.country = Country.GB
        company = Company()
        company.legal_name = 'Parent Holdings Ltd'
        company.trading_name = 'Parent Holdings'
        company.registered_address = address
        representative = EntityRepresentative()
        representative.company = company
        representative.ownership_percentage = 60

        assert _serialize(representative) == {
            'company': {
                'legal_name': 'Parent Holdings Ltd',
                'trading_name': 'Parent Holdings',
                'registered_address': {
                    'address_line1': '1 Main Street', 'city': 'London', 'zip': 'W1T 4TJ', 'country': 'GB'},
            },
            'ownership_percentage': 60,
        }

    def test_serializes_financial_statements_document(self):
        financial_statements = FinancialStatements()
        financial_statements.type = FinancialStatementsType.FINANCIAL_STATEMENTS
        financial_statements.front = 'file_xwc7fyfsezfda35wxcimpsw6q2'
        documents = OnboardSubEntityDocuments()
        documents.financial_statements = financial_statements

        assert _serialize(documents) == {
            'financial_statements': {
                'type': 'financial_statements',
                'front': 'file_xwc7fyfsezfda35wxcimpsw6q2',
            }
        }

    def test_serializes_onboard_entity_request_with_agreed_terms_and_seller_category(self):
        agreed_terms = AgreedTerms()
        agreed_terms.date = '2026-07-20T10:00:00Z'
        agreed_terms.ip_address = '203.0.113.42'
        agreed_terms.name = 'John Representative'
        agreed_terms.email = 'john@example.com'
        agreed_terms.version = '1.0'
        request = OnboardEntityRequest()
        request.reference = 'ref_1'
        request.is_draft = False
        request.agreed_terms = agreed_terms
        request.seller_category = 'saas'

        assert _serialize(request) == {
            'reference': 'ref_1',
            'is_draft': False,
            'seller_category': 'saas',
            'agreed_terms': {
                'date': '2026-07-20T10:00:00Z',
                'ip_address': '203.0.113.42',
                'name': 'John Representative',
                'email': 'john@example.com',
                'version': '1.0',
            },
        }

    def test_serializes_full_onboard_entity_request_v3(self):
        individual = RepresentativeIndividual()
        individual.first_name = 'John'
        individual.last_name = 'Doe'
        representative = EntityRepresentative()
        representative.individual = individual
        representative.roles = [EntityRoles.UBO]
        company = Company()
        company.legal_name = 'Super Hero Masks Inc.'
        company.business_type = BusinessType.PRIVATE_CORPORATION
        company.representatives = [representative]
        payments = ProcessingDetailsPayments()
        payments.ach = ProcessingDetailsAch()
        payments.ach.annual_ach_volume = 1000000
        processing_details = ProcessingDetails()
        processing_details.currency = Currency.USD
        processing_details.payments = payments
        request = OnboardEntityRequest()
        request.reference = 'ref_1'
        request.company = company
        request.processing_details = processing_details

        result = _serialize(request)

        assert result['reference'] == 'ref_1'
        assert result['company']['legal_name'] == 'Super Hero Masks Inc.'
        assert result['company']['business_type'] == 'private_corporation'
        assert result['company']['representatives'][0]['individual']['first_name'] == 'John'
        assert result['company']['representatives'][0]['roles'] == ['ubo']
        assert result['processing_details']['currency'] == 'USD'
        assert result['processing_details']['payments']['ach']['annual_ach_volume'] == 1000000

    def test_serializes_all_thirteen_documents_fields(self):
        documents = OnboardSubEntityDocuments()

        identity_verification = EntityIdentificationDocument()
        identity_verification.type = DocumentType.NATIONAL_IDENTITY_CARD
        identity_verification.front = 'file_ebxawxm4fesbgqtwtiuikwdviu'
        identity_verification.back = 'file_3wb62nghcba73hmzz7rxfdpgtp'
        documents.identity_verification = identity_verification

        company_verification = CompanyVerification()
        company_verification.type = CompanyVerificationType.INCORPORATION_DOCUMENT
        company_verification.front = 'file_std7uf52bx3hvqvoiiyne6fx6m'
        documents.company_verification = company_verification

        articles_of_association = ArticlesOfAssociation()
        articles_of_association.type = ArticlesOfAssociationType.ARTICLES_OF_ASSOCIATION
        articles_of_association.front = 'file_734v2ecg5yxaqrvomqqnpjxgqw'
        documents.articles_of_association = articles_of_association

        bank_verification = BankVerification()
        bank_verification.type = BankVerificationType.BANK_STATEMENT
        bank_verification.front = 'file_3aeeozugysd4ivxus6ytlwwh7a'
        documents.bank_verification = bank_verification

        shareholder_structure = ShareholderStructure()
        shareholder_structure.type = ShareholderStructureType.CERTIFIED_SHAREHOLDER_STRUCTURE
        shareholder_structure.front = 'file_xfkfxrkzawbxgl7tz7c27qdnz5'
        documents.shareholder_structure = shareholder_structure

        proof_of_legality = ProofOfLegality()
        proof_of_legality.type = ProofOfLegalityType.PROOF_OF_LEGALITY
        proof_of_legality.front = 'file_zhlrertry7amktnhskyj5g4hvb'
        documents.proof_of_legality = proof_of_legality

        proof_of_principal_address = ProofOfPrincipalAddress()
        proof_of_principal_address.type = ProofOfPrincipalAddressType.PROOF_OF_ADDRESS
        proof_of_principal_address.front = 'file_lk6ym6bhljxnvnvabzphglsllv'
        documents.proof_of_principal_address = proof_of_principal_address

        tax_verification = TaxVerification()
        tax_verification.type = TaxVerificationType.EIN_LETTER
        tax_verification.front = 'file_vexm5xyve2qwdmgzzk5fceyoxw'
        documents.tax_verification = tax_verification

        financial_verification = FinancialVerification()
        financial_verification.type = FinancialVerificationType.FINANCIAL_STATEMENT
        financial_verification.front = 'file_smwugkyjp2oyaaj4stcu2rzrrc'
        documents.financial_verification = financial_verification

        financial_statements = FinancialStatements()
        financial_statements.type = FinancialStatementsType.FINANCIAL_STATEMENTS
        financial_statements.front = 'file_sddb4dghum37xzptw3zdiegg3n'
        documents.financial_statements = financial_statements

        additional_document1 = AdditionalDocument()
        additional_document1.front = 'file_5hvmsac5bzbmg7lnypr4so2h43'
        documents.additional_document1 = additional_document1
        additional_document2 = AdditionalDocument()
        additional_document2.front = 'file_mh2fyxtghcalxx77gsfb3gk77t'
        documents.additional_document2 = additional_document2
        additional_document3 = AdditionalDocument()
        additional_document3.front = 'file_ok7jhmf4nzkcudzyh5v5q2kc6d'
        documents.additional_document3 = additional_document3

        assert _serialize(documents) == {
            'identity_verification': {
                'type': 'national_identity_card',
                'front': 'file_ebxawxm4fesbgqtwtiuikwdviu',
                'back': 'file_3wb62nghcba73hmzz7rxfdpgtp',
            },
            'company_verification': {'type': 'incorporation_document', 'front': 'file_std7uf52bx3hvqvoiiyne6fx6m'},
            'articles_of_association': {
                'type': 'articles_of_association', 'front': 'file_734v2ecg5yxaqrvomqqnpjxgqw'},
            'bank_verification': {'type': 'bank_statement', 'front': 'file_3aeeozugysd4ivxus6ytlwwh7a'},
            'shareholder_structure': {
                'type': 'certified_shareholder_structure', 'front': 'file_xfkfxrkzawbxgl7tz7c27qdnz5'},
            'proof_of_legality': {'type': 'proof_of_legality', 'front': 'file_zhlrertry7amktnhskyj5g4hvb'},
            'proof_of_principal_address': {'type': 'proof_of_address', 'front': 'file_lk6ym6bhljxnvnvabzphglsllv'},
            'tax_verification': {'type': 'ein_letter', 'front': 'file_vexm5xyve2qwdmgzzk5fceyoxw'},
            'financial_verification': {'type': 'financial_statement', 'front': 'file_smwugkyjp2oyaaj4stcu2rzrrc'},
            'financial_statements': {'type': 'financial_statements', 'front': 'file_sddb4dghum37xzptw3zdiegg3n'},
            # The additional documents take a front only; the spec defines no type for them.
            'additional_document1': {'front': 'file_5hvmsac5bzbmg7lnypr4so2h43'},
            'additional_document2': {'front': 'file_mh2fyxtghcalxx77gsfb3gk77t'},
            'additional_document3': {'front': 'file_ok7jhmf4nzkcudzyh5v5q2kc6d'},
        }

    # POST /entities/{entity_id}/files sends the purpose's value on the wire; the first fourteen are
    # the PlatformsFileUpload enum, the last two are not accepted by that endpoint.
    def test_file_purpose_enum_values(self):
        assert {p.name: p.value for p in FilePurpose} == {
            'ADDITIONAL_DOCUMENT': 'additional_document',
            'ARTICLES_OF_ASSOCIATION': 'articles_of_association',
            'BANK_VERIFICATION': 'bank_verification',
            'CERTIFIED_AUTHORISED_SIGNATORY': 'certified_authorised_signatory',
            'COMPANY_OWNERSHIP': 'company_ownership',
            'IDENTITY_VERIFICATION': 'identity_verification',
            'COMPANY_VERIFICATION': 'company_verification',
            'FINANCIAL_VERIFICATION': 'financial_verification',
            'TAX_VERIFICATION': 'tax_verification',
            'PROOF_OF_LEGALITY': 'proof_of_legality',
            'PROOF_OF_PRINCIPAL_ADDRESS': 'proof_of_principal_address',
            'SHAREHOLDER_STRUCTURE': 'shareholder_structure',
            'PROOF_OF_RESIDENTIAL_ADDRESS': 'proof_of_residential_address',
            'PROOF_OF_REGISTRATION': 'proof_of_registration',
            'IDENTIFICATION': 'identification',
            'DISPUTE_EVIDENCE': 'dispute_evidence',
        }

    def test_entity_roles_enum_values(self):
        assert [r.value for r in EntityRoles] == [
            'ubo', 'legal_representative', 'authorised_signatory', 'director', 'control_person',
        ]

    def test_company_position_enum_values(self):
        assert [p.value for p in CompanyPosition] == [
            'ceo', 'cfo', 'coo', 'managing_member', 'general_partner', 'president',
            'vice_president', 'treasurer', 'other_senior_management',
            'other_executive_officer', 'other_non_executive_non_senior',
        ]

    def test_business_type_enum_values(self):
        assert [b.value for b in BusinessType] == [
            'individual_or_sole_proprietorship', 'general_partnership', 'limited_partnership',
            'scottish_limited_partnership', 'public_limited_company', 'limited_company',
            'limited_liability_corporation', 'private_corporation', 'publicly_traded_corporation',
            'professional_association', 'unincorporated_association', 'auto_entrepreneur',
            'government_agency', 'non_profit_entity', 'trust', 'club_or_society',
            'regulated_financial_institution', 'cftc_registered_entity', 'sec_registered_entity',
        ]

    def test_document_type_enum_values(self):
        assert [d.value for d in DocumentType] == [
            'passport', 'national_identity_card', 'driving_license', 'citizen_card', 'residence_permit',
            'electoral_id',
        ]

    def test_company_verification_type_enum_values(self):
        assert [t.value for t in CompanyVerificationType] == ['incorporation_document', 'articles_of_association']

    def test_articles_of_association_type_enum_values(self):
        assert [t.value for t in ArticlesOfAssociationType] == ['memorandum_of_association', 'articles_of_association']

    def test_tax_verification_type_enum_values(self):
        assert [t.value for t in TaxVerificationType] == ['ein_letter']

    def test_shareholder_structure_type_enum_values(self):
        assert [t.value for t in ShareholderStructureType] == ['certified_shareholder_structure']

    def test_proof_of_legality_type_enum_values(self):
        assert [t.value for t in ProofOfLegalityType] == ['proof_of_legality']

    def test_proof_of_principal_address_type_enum_values(self):
        assert [t.value for t in ProofOfPrincipalAddressType] == ['proof_of_address']

    def test_financial_verification_type_enum_values(self):
        assert [t.value for t in FinancialVerificationType] == ['financial_statement']

    def test_national_id_type_enum_values(self):
        assert [t.value for t in NationalIdType] == [
            'ssn', 'itin', 'passport', 'driving_license', 'national_id_card', 'residence_permit', 'other',
        ]

    # US Company Full (3.0): phone with an ISO alpha-2 country_code, email_addresses and invitee.
    def test_serializes_contact_details(self):
        phone = Phone()
        phone.country_code = 'US'
        phone.number = '4155678900'
        email_addresses = EntityEmailAddresses()
        email_addresses.primary = 'admin@superhero1234.com'
        invitee = Invitee()
        invitee.email = 'invitee@superhero1234.com'
        contact_details = ContactDetails()
        contact_details.phone = phone
        contact_details.email_addresses = email_addresses
        contact_details.invitee = invitee

        assert _serialize(contact_details) == {
            'phone': {'country_code': 'US', 'number': '4155678900'},
            'email_addresses': {'primary': 'admin@superhero1234.com'},
            'invitee': {'email': 'invitee@superhero1234.com'},
        }

    # PlatformsHostedOnboardInviteRequest takes reference, is_draft and contact_details.invitee only.
    def test_serializes_hosted_onboarding_invite_request(self):
        invitee = Invitee()
        invitee.email = 'invitee@superhero1234.com'
        request = OnboardEntityRequest()
        request.reference = 'superhero1234'
        request.is_draft = True
        request.contact_details = ContactDetails()
        request.contact_details.invitee = invitee

        assert _serialize(request) == {
            'reference': 'superhero1234',
            'is_draft': True,
            'contact_details': {'invitee': {'email': 'invitee@superhero1234.com'}},
        }

    def test_serializes_company_eea_full_fields(self):
        principal_address = Address()
        principal_address.address_line1 = '12 Rue de Rivoli'
        principal_address.city = 'Paris'
        principal_address.zip = '75001'
        principal_address.country = Country.FR
        registered_address = Address()
        registered_address.address_line1 = '8 Avenue de l\'Opera'
        registered_address.city = 'Paris'
        registered_address.zip = '75002'
        registered_address.country = Country.FR
        date_of_incorporation = DateOfIncorporation()
        date_of_incorporation.month = 6
        date_of_incorporation.year = 2010
        date_of_birth = DateOfBirth()
        date_of_birth.day = 5
        date_of_birth.month = 6
        date_of_birth.year = 1980
        place_of_birth = PlaceOfBirth()
        place_of_birth.country = Country.FR
        individual = RepresentativeIndividual()
        individual.first_name = 'Marie'
        individual.last_name = 'Dupont'
        individual.date_of_birth = date_of_birth
        individual.place_of_birth = place_of_birth
        individual.address = principal_address
        representative = EntityRepresentative()
        representative.individual = individual
        representative.roles = [EntityRoles.UBO, EntityRoles.DIRECTOR]
        representative.ownership_percentage = 100
        company = Company()
        company.legal_name = 'Super Hero Masques SAS'
        company.trading_name = 'Super Hero Masques'
        company.business_registration_number = '123456789'
        company.business_type = BusinessType.LIMITED_COMPANY
        company.date_of_incorporation = date_of_incorporation
        company.regulatory_licence_number = 'FR-12345678'
        company.principal_address = principal_address
        company.registered_address = registered_address
        company.representatives = [representative]

        assert _serialize(company) == {
            'legal_name': 'Super Hero Masques SAS',
            'trading_name': 'Super Hero Masques',
            'business_registration_number': '123456789',
            'business_type': 'limited_company',
            'date_of_incorporation': {'month': 6, 'year': 2010},
            'regulatory_licence_number': 'FR-12345678',
            'principal_address': {
                'address_line1': '12 Rue de Rivoli', 'city': 'Paris', 'zip': '75001', 'country': 'FR'},
            'registered_address': {
                'address_line1': '8 Avenue de l\'Opera', 'city': 'Paris', 'zip': '75002', 'country': 'FR'},
            'representatives': [{
                'individual': {
                    'first_name': 'Marie',
                    'last_name': 'Dupont',
                    'date_of_birth': {'day': 5, 'month': 6, 'year': 1980},
                    'place_of_birth': {'country': 'FR'},
                    'address': {
                        'address_line1': '12 Rue de Rivoli', 'city': 'Paris', 'zip': '75001', 'country': 'FR'},
                },
                'roles': ['ubo', 'director'],
                'ownership_percentage': 100,
            }],
        }

    # EEA Company Full (2.0) company.financial_details, EUR only.
    def test_serializes_company_financial_details_v2(self):
        financial_details = EntityFinancialDetails()
        financial_details.annual_processing_volume = 120000
        financial_details.average_transaction_value = 500
        financial_details.highest_transaction_value = 2500
        financial_details.currency = Currency.EUR

        assert _serialize(financial_details) == {
            'annual_processing_volume': 120000,
            'average_transaction_value': 500,
            'highest_transaction_value': 2500,
            'currency': 'EUR',
        }

    # US Sole Trader Full (2.0) individual: identification and financial_details (USD), no place_of_birth.
    def test_serializes_individual_v2_us_sole_trader(self):
        registered_address = Address()
        registered_address.address_line1 = '123 Main Street'
        registered_address.city = 'San Francisco'
        registered_address.state = 'CA'
        registered_address.zip = '94105'
        registered_address.country = Country.US
        date_of_birth = DateOfBirth()
        date_of_birth.day = 15
        date_of_birth.month = 1
        date_of_birth.year = 1990
        identification = Identification()
        identification.national_id_number = '123456789'
        financial_details = EntityFinancialDetails()
        financial_details.annual_processing_volume = 120000
        financial_details.average_transaction_value = 500
        financial_details.highest_transaction_value = 2500
        financial_details.currency = Currency.USD
        individual = Individual()
        individual.first_name = 'Hannah'
        individual.middle_name = 'Grace'
        individual.last_name = 'Bret'
        individual.trading_name = 'Hannah\'s Goods'
        individual.registered_address = registered_address
        individual.date_of_birth = date_of_birth
        individual.identification = identification
        individual.financial_details = financial_details

        assert _serialize(individual) == {
            'first_name': 'Hannah',
            'middle_name': 'Grace',
            'last_name': 'Bret',
            'trading_name': 'Hannah\'s Goods',
            'registered_address': {
                'address_line1': '123 Main Street', 'city': 'San Francisco', 'state': 'CA', 'zip': '94105',
                'country': 'US'},
            'date_of_birth': {'day': 15, 'month': 1, 'year': 1990},
            'identification': {'national_id_number': '123456789'},
            'financial_details': {
                'annual_processing_volume': 120000,
                'average_transaction_value': 500,
                'highest_transaction_value': 2500,
                'currency': 'USD',
            },
        }

    # EEA Sole Trader Full (2.0) individual: place_of_birth, no identification nor financial_details.
    def test_serializes_individual_v2_eea_sole_trader(self):
        registered_address = Address()
        registered_address.address_line1 = '12 Rue de Rivoli'
        registered_address.city = 'Paris'
        registered_address.zip = '75001'
        registered_address.country = Country.FR
        date_of_birth = DateOfBirth()
        date_of_birth.day = 5
        date_of_birth.month = 6
        date_of_birth.year = 1980
        place_of_birth = PlaceOfBirth()
        place_of_birth.country = Country.FR
        individual = Individual()
        individual.first_name = 'Marie'
        individual.middle_name = 'Claire'
        individual.last_name = 'Dupont'
        individual.trading_name = 'Masques Marie'
        individual.registered_address = registered_address
        individual.date_of_birth = date_of_birth
        individual.place_of_birth = place_of_birth

        assert _serialize(individual) == {
            'first_name': 'Marie',
            'middle_name': 'Claire',
            'last_name': 'Dupont',
            'trading_name': 'Masques Marie',
            'registered_address': {
                'address_line1': '12 Rue de Rivoli', 'city': 'Paris', 'zip': '75001', 'country': 'FR'},
            'date_of_birth': {'day': 5, 'month': 6, 'year': 1980},
            'place_of_birth': {'country': 'FR'},
        }

    # US ISV Seller (3.0) is the variant that takes every RepresentativeIndividual attribute.
    def test_serializes_representative_individual_all_fields(self):
        date_of_birth = DateOfBirth()
        date_of_birth.day = 15
        date_of_birth.month = 1
        date_of_birth.year = 1990
        place_of_birth = PlaceOfBirth()
        place_of_birth.country = Country.US
        citizenship = Citizenship()
        citizenship.type = 'citizenship'
        citizenship.country = Country.US
        phone = Phone()
        phone.country_code = 'US'
        phone.number = '4155678901'
        address = Address()
        address.address_line1 = '123 Main Street'
        address.city = 'San Francisco'
        address.state = 'CA'
        address.zip = '94105'
        address.country = Country.US
        individual = RepresentativeIndividual()
        individual.first_name = 'Toby'
        individual.middle_name = 'James'
        individual.last_name = 'Arden'
        individual.date_of_birth = date_of_birth
        individual.place_of_birth = place_of_birth
        individual.citizenships = [citizenship]
        individual.national_id_type = NationalIdType.SSN
        individual.national_id_number = '123456789'
        individual.email_address = 'toby.arden@example.com'
        individual.phone = phone
        individual.address = address

        assert _serialize(individual) == {
            'first_name': 'Toby',
            'middle_name': 'James',
            'last_name': 'Arden',
            'date_of_birth': {'day': 15, 'month': 1, 'year': 1990},
            'place_of_birth': {'country': 'US'},
            'citizenships': [{'type': 'citizenship', 'country': 'US'}],
            'national_id_type': 'ssn',
            'national_id_number': '123456789',
            'email_address': 'toby.arden@example.com',
            'phone': {'country_code': 'US', 'number': '4155678901'},
            'address': {
                'address_line1': '123 Main Street', 'city': 'San Francisco', 'state': 'CA', 'zip': '94105',
                'country': 'US'},
        }

    # US Company Full (2.0) flat representative: identification, phone with number only, no
    # place_of_birth.
    def test_serializes_representative_v2_us_company_fields(self):
        date_of_birth = DateOfBirth()
        date_of_birth.day = 15
        date_of_birth.month = 1
        date_of_birth.year = 1990
        phone = Phone()
        phone.number = '4155678901'
        address = Address()
        address.address_line1 = '123 Main Street'
        address.city = 'San Francisco'
        address.state = 'CA'
        address.zip = '94105'
        address.country = Country.US
        identification = EntityIdentification()
        identification.national_id_number = '123456789'
        representative = EntityRepresentative()
        representative.first_name = 'Toby'
        representative.middle_name = 'James'
        representative.last_name = 'Arden'
        representative.date_of_birth = date_of_birth
        representative.phone = phone
        representative.address = address
        representative.identification = identification
        representative.roles = [EntityRoles.UBO, EntityRoles.CONTROL_PERSON]

        assert _serialize(representative) == {
            'first_name': 'Toby',
            'middle_name': 'James',
            'last_name': 'Arden',
            'date_of_birth': {'day': 15, 'month': 1, 'year': 1990},
            'phone': {'number': '4155678901'},
            'address': {
                'address_line1': '123 Main Street', 'city': 'San Francisco', 'state': 'CA', 'zip': '94105',
                'country': 'US'},
            'identification': {'national_id_number': '123456789'},
            'roles': ['ubo', 'control_person'],
        }

    # EEA Company Full (2.0) flat representative: place_of_birth, no identification.
    def test_serializes_representative_v2_eea_company_fields(self):
        date_of_birth = DateOfBirth()
        date_of_birth.day = 5
        date_of_birth.month = 6
        date_of_birth.year = 1980
        place_of_birth = PlaceOfBirth()
        place_of_birth.country = Country.FR
        phone = Phone()
        phone.number = '142681234'
        address = Address()
        address.address_line1 = '12 Rue de Rivoli'
        address.city = 'Paris'
        address.zip = '75001'
        address.country = Country.FR
        representative = EntityRepresentative()
        representative.first_name = 'Marie'
        representative.middle_name = 'Claire'
        representative.last_name = 'Dupont'
        representative.date_of_birth = date_of_birth
        representative.place_of_birth = place_of_birth
        representative.phone = phone
        representative.address = address
        representative.roles = [EntityRoles.LEGAL_REPRESENTATIVE]

        assert _serialize(representative) == {
            'first_name': 'Marie',
            'middle_name': 'Claire',
            'last_name': 'Dupont',
            'date_of_birth': {'day': 5, 'month': 6, 'year': 1980},
            'place_of_birth': {'country': 'FR'},
            'phone': {'number': '142681234'},
            'address': {'address_line1': '12 Rue de Rivoli', 'city': 'Paris', 'zip': '75001', 'country': 'FR'},
            'roles': ['legal_representative'],
        }

    # individual.identification (US Sole Trader, 2.0) and company.representatives[].identification
    # (US Company, 2.0) both carry a nine digit national_id_number only.
    def test_serializes_identification(self):
        identification = Identification()
        identification.national_id_number = '123456789'
        entity_identification = EntityIdentification()
        entity_identification.national_id_number = '123456789'

        assert _serialize(identification) == {'national_id_number': '123456789'}
        assert _serialize(entity_identification) == {'national_id_number': '123456789'}

    def test_serializes_entity_file_request(self):
        request = EntityFileRequest()
        request.purpose = FilePurpose.IDENTITY_VERIFICATION

        body = json.dumps(request, cls=JsonSerializer)

        assert json.loads(body) == {'purpose': 'identity_verification'}
        # Key-level check on the raw body, so a naming change cannot pass silently.
        assert '"purpose": "identity_verification"' in body

    # components.schemas["USISVSellerCompany3-0"].example in the swagger, built from the SDK classes.
    def test_roundtrips_us_isv_seller_company_example(self):
        agreed_terms = AgreedTerms()
        agreed_terms.date = '2026-07-02T10:30:00.0000000+00:00'
        agreed_terms.ip_address = '8.8.8.8'
        agreed_terms.name = 'Toby Arden'
        agreed_terms.email = 'toby.arden@example.com'
        agreed_terms.version = 'cko-platform-terms-1.0.0'
        ach = ProcessingDetailsAch()
        ach.annual_ach_volume = 100000
        ach.average_ach_transaction_size = 5000
        ach.estimated_monthly_credit_volume = 50000
        ach.average_credit_amount = 2500
        processing_details = ProcessingDetails()
        processing_details.annual_processing_volume = 1000
        processing_details.average_transaction_value = 2000
        processing_details.average_order_fulfillment_time = 3
        processing_details.target_countries = ['US']
        processing_details.currency = Currency.USD
        processing_details.payments = ProcessingDetailsPayments()
        processing_details.payments.ach = ach
        contact_phone = Phone()
        contact_phone.number = '4155678900'
        contact_phone.country_code = 'US'
        contact_details = ContactDetails()
        contact_details.phone = contact_phone
        contact_details.email_addresses = EntityEmailAddresses()
        contact_details.email_addresses.primary = 'toby.arden@example.com'
        contact_details.email_addresses.pci_compliance_contact = 'pci.contact@example.com'
        profile = Profile()
        profile.urls = ['https://www.isv-seller-example.com']
        profile.mccs = ['5551']
        profile.holding_currencies = [Currency.USD]
        profile.default_holding_currency = Currency.USD
        address = Address()
        address.address_line1 = '123 Main Street'
        address.city = 'San Francisco'
        address.state = 'CA'
        address.zip = '94105'
        address.country = Country.US
        date_of_incorporation = DateOfIncorporation()
        date_of_incorporation.year = 2025
        date_of_incorporation.month = 10
        date_of_incorporation.day = 1

        ubo = RepresentativeIndividual()
        ubo.first_name = 'Toby'
        ubo.last_name = 'Arden'
        ubo.email_address = 'toby.arden@example.com'
        ubo.national_id_type = NationalIdType.SSN
        ubo.national_id_number = '123456789'
        ubo.date_of_birth = DateOfBirth()
        ubo.date_of_birth.day = 15
        ubo.date_of_birth.month = 1
        ubo.date_of_birth.year = 1990
        ubo.place_of_birth = PlaceOfBirth()
        ubo.place_of_birth.country = Country.US
        ubo.citizenships = [Citizenship()]
        ubo.citizenships[0].country = Country.US
        ubo.phone = Phone()
        ubo.phone.country_code = 'US'
        ubo.phone.number = '4155678901'
        ubo.address = address
        first = EntityRepresentative()
        first.roles = [EntityRoles.UBO, EntityRoles.CONTROL_PERSON]
        first.ownership_percentage = 25
        first.company_position = CompanyPosition.CEO
        first.individual = ubo

        signatory = RepresentativeIndividual()
        signatory.first_name = 'Alex'
        signatory.last_name = 'Morgan'
        signatory.email_address = 'alex.morgan@example.com'
        signatory.national_id_type = NationalIdType.SSN
        signatory.national_id_number = '987654321'
        signatory.date_of_birth = DateOfBirth()
        signatory.date_of_birth.day = 22
        signatory.date_of_birth.month = 6
        signatory.date_of_birth.year = 1985
        signatory.place_of_birth = PlaceOfBirth()
        signatory.place_of_birth.country = Country.US
        signatory.citizenships = [Citizenship()]
        signatory.citizenships[0].country = Country.US
        signatory.phone = Phone()
        signatory.phone.country_code = 'US'
        signatory.phone.number = '4155678902'
        signatory.address = address
        second = EntityRepresentative()
        second.roles = [EntityRoles.AUTHORISED_SIGNATORY]
        second.individual = signatory

        company = Company()
        company.business_registration_number = '12-3456789'
        company.business_type = BusinessType.PRIVATE_CORPORATION
        company.legal_name = 'ISV Seller Example Inc'
        company.trading_name = 'ISV Seller Example'
        company.registered_address = address
        company.principal_address = address
        company.date_of_incorporation = date_of_incorporation
        company.representatives = [first, second]
        request = OnboardEntityRequest()
        request.reference = 'isv-seller-example001'
        request.agreed_terms = agreed_terms
        request.seller_category = 'cat_retail_001'
        request.processing_details = processing_details
        request.contact_details = contact_details
        request.profile = profile
        request.company = company

        assert _serialize(request) == {
            'reference': 'isv-seller-example001',
            'agreed_terms': {
                'date': '2026-07-02T10:30:00.0000000+00:00',
                'ip_address': '8.8.8.8',
                'name': 'Toby Arden',
                'email': 'toby.arden@example.com',
                'version': 'cko-platform-terms-1.0.0',
            },
            'seller_category': 'cat_retail_001',
            'processing_details': {
                'annual_processing_volume': 1000,
                'average_transaction_value': 2000,
                'average_order_fulfillment_time': 3,
                'target_countries': ['US'],
                'currency': 'USD',
                'payments': {
                    'ach': {
                        'annual_ach_volume': 100000,
                        'average_ach_transaction_size': 5000,
                        'estimated_monthly_credit_volume': 50000,
                        'average_credit_amount': 2500,
                    },
                },
            },
            'contact_details': {
                'phone': {'number': '4155678900', 'country_code': 'US'},
                'email_addresses': {
                    'primary': 'toby.arden@example.com',
                    'pci_compliance_contact': 'pci.contact@example.com',
                },
            },
            'profile': {
                'urls': ['https://www.isv-seller-example.com'],
                'mccs': ['5551'],
                'holding_currencies': ['USD'],
                'default_holding_currency': 'USD',
            },
            'company': {
                'business_registration_number': '12-3456789',
                'business_type': 'private_corporation',
                'legal_name': 'ISV Seller Example Inc',
                'trading_name': 'ISV Seller Example',
                'registered_address': {
                    'address_line1': '123 Main Street',
                    'city': 'San Francisco',
                    'state': 'CA',
                    'zip': '94105',
                    'country': 'US',
                },
                'principal_address': {
                    'address_line1': '123 Main Street',
                    'city': 'San Francisco',
                    'state': 'CA',
                    'zip': '94105',
                    'country': 'US',
                },
                'date_of_incorporation': {'year': 2025, 'month': 10, 'day': 1},
                'representatives': [
                    {
                        'roles': ['ubo', 'control_person'],
                        'ownership_percentage': 25,
                        'company_position': 'ceo',
                        'individual': {
                            'first_name': 'Toby',
                            'last_name': 'Arden',
                            'email_address': 'toby.arden@example.com',
                            'national_id_type': 'ssn',
                            'national_id_number': '123456789',
                            'date_of_birth': {'day': 15, 'month': 1, 'year': 1990},
                            'place_of_birth': {'country': 'US'},
                            'citizenships': [{'country': 'US'}],
                            'phone': {'country_code': 'US', 'number': '4155678901'},
                            'address': {
                                'address_line1': '123 Main Street',
                                'city': 'San Francisco',
                                'state': 'CA',
                                'zip': '94105',
                                'country': 'US',
                            },
                        },
                    },
                    {
                        'roles': ['authorised_signatory'],
                        'individual': {
                            'first_name': 'Alex',
                            'last_name': 'Morgan',
                            'email_address': 'alex.morgan@example.com',
                            'national_id_type': 'ssn',
                            'national_id_number': '987654321',
                            'date_of_birth': {'day': 22, 'month': 6, 'year': 1985},
                            'place_of_birth': {'country': 'US'},
                            'citizenships': [{'country': 'US'}],
                            'phone': {'country_code': 'US', 'number': '4155678902'},
                            'address': {
                                'address_line1': '123 Main Street',
                                'city': 'San Francisco',
                                'state': 'CA',
                                'zip': '94105',
                                'country': 'US',
                            },
                        },
                    },
                ],
            },
        }

    # components.schemas["USISVSellerSoleTrader3-0"].example in the swagger, built from the SDK classes.
    def test_roundtrips_us_isv_seller_sole_trader_example(self):
        agreed_terms = AgreedTerms()
        agreed_terms.date = '2026-07-02T10:30:00.0000000+00:00'
        agreed_terms.ip_address = '8.8.8.8'
        agreed_terms.name = 'Hannah Bret'
        agreed_terms.email = 'hannah.bret@example.com'
        agreed_terms.version = 'cko-platform-terms-1.0.0'
        ach = ProcessingDetailsAch()
        ach.annual_ach_volume = 100000
        ach.average_ach_transaction_size = 5000
        ach.estimated_monthly_credit_volume = 50000
        ach.average_credit_amount = 2500
        processing_details = ProcessingDetails()
        processing_details.annual_processing_volume = 1000
        processing_details.average_transaction_value = 2000
        processing_details.average_order_fulfillment_time = 3
        processing_details.target_countries = ['US']
        processing_details.currency = Currency.USD
        processing_details.payments = ProcessingDetailsPayments()
        processing_details.payments.ach = ach
        contact_phone = Phone()
        contact_phone.number = '4155678900'
        contact_phone.country_code = 'US'
        contact_details = ContactDetails()
        contact_details.phone = contact_phone
        contact_details.email_addresses = EntityEmailAddresses()
        contact_details.email_addresses.primary = 'hannah.bret@example.com'
        contact_details.email_addresses.pci_compliance_contact = 'pci.contact@example.com'
        profile = Profile()
        profile.urls = ['https://www.isv-sole-trader-example.com']
        profile.mccs = ['5551']
        profile.holding_currencies = [Currency.USD]
        profile.default_holding_currency = Currency.USD
        address = Address()
        address.address_line1 = '123 Main Street'
        address.city = 'San Francisco'
        address.state = 'CA'
        address.zip = '94105'
        address.country = Country.US
        date_of_incorporation = DateOfIncorporation()
        date_of_incorporation.year = 2025
        date_of_incorporation.month = 10
        date_of_incorporation.day = 1

        individual = RepresentativeIndividual()
        individual.first_name = 'Hannah'
        individual.last_name = 'Bret'
        individual.email_address = 'hannah.bret@example.com'
        individual.national_id_type = NationalIdType.SSN
        individual.national_id_number = '123456789'
        individual.date_of_birth = DateOfBirth()
        individual.date_of_birth.day = 15
        individual.date_of_birth.month = 1
        individual.date_of_birth.year = 1990
        individual.place_of_birth = PlaceOfBirth()
        individual.place_of_birth.country = Country.US
        individual.citizenships = [Citizenship()]
        individual.citizenships[0].country = Country.US
        individual.phone = Phone()
        individual.phone.country_code = 'US'
        individual.phone.number = '4155678901'
        individual.address = address
        representative = EntityRepresentative()
        representative.roles = [EntityRoles.UBO]
        representative.ownership_percentage = 100
        representative.individual = individual

        company = Company()
        company.business_type = BusinessType.INDIVIDUAL_OR_SOLE_PROPRIETORSHIP
        company.is_registered_company = False
        company.trading_name = 'Hannah\'s Goods'
        company.date_of_incorporation = date_of_incorporation
        company.principal_address = address
        company.representatives = [representative]
        request = OnboardEntityRequest()
        request.reference = 'isv-sole-trader-example001'
        request.agreed_terms = agreed_terms
        request.seller_category = 'cat_retail_001'
        request.processing_details = processing_details
        request.contact_details = contact_details
        request.profile = profile
        request.company = company

        assert _serialize(request) == {
            'reference': 'isv-sole-trader-example001',
            'agreed_terms': {
                'date': '2026-07-02T10:30:00.0000000+00:00',
                'ip_address': '8.8.8.8',
                'name': 'Hannah Bret',
                'email': 'hannah.bret@example.com',
                'version': 'cko-platform-terms-1.0.0',
            },
            'seller_category': 'cat_retail_001',
            'processing_details': {
                'annual_processing_volume': 1000,
                'average_transaction_value': 2000,
                'average_order_fulfillment_time': 3,
                'target_countries': ['US'],
                'currency': 'USD',
                'payments': {
                    'ach': {
                        'annual_ach_volume': 100000,
                        'average_ach_transaction_size': 5000,
                        'estimated_monthly_credit_volume': 50000,
                        'average_credit_amount': 2500,
                    },
                },
            },
            'contact_details': {
                'phone': {'number': '4155678900', 'country_code': 'US'},
                'email_addresses': {
                    'primary': 'hannah.bret@example.com',
                    'pci_compliance_contact': 'pci.contact@example.com',
                },
            },
            'profile': {
                'urls': ['https://www.isv-sole-trader-example.com'],
                'mccs': ['5551'],
                'holding_currencies': ['USD'],
                'default_holding_currency': 'USD',
            },
            'company': {
                'business_type': 'individual_or_sole_proprietorship',
                'is_registered_company': False,
                'trading_name': 'Hannah\'s Goods',
                'date_of_incorporation': {'year': 2025, 'month': 10, 'day': 1},
                'principal_address': {
                    'address_line1': '123 Main Street',
                    'city': 'San Francisco',
                    'state': 'CA',
                    'zip': '94105',
                    'country': 'US',
                },
                'representatives': [
                    {
                        'roles': ['ubo'],
                        'ownership_percentage': 100,
                        'individual': {
                            'first_name': 'Hannah',
                            'last_name': 'Bret',
                            'email_address': 'hannah.bret@example.com',
                            'national_id_type': 'ssn',
                            'national_id_number': '123456789',
                            'date_of_birth': {'day': 15, 'month': 1, 'year': 1990},
                            'place_of_birth': {'country': 'US'},
                            'citizenships': [{'country': 'US'}],
                            'phone': {'country_code': 'US', 'number': '4155678901'},
                            'address': {
                                'address_line1': '123 Main Street',
                                'city': 'San Francisco',
                                'state': 'CA',
                                'zip': '94105',
                                'country': 'US',
                            },
                        },
                    },
                ],
            },
        }


class TestEntityFileResponseShape:
    """Response-shape tests for POST and GET /entities/{entity_id}/files.

    Python has no typed response classes; ApiClient wraps the parsed JSON in ResponseWrapper, which
    wraps nested dicts recursively. Every value is a field-level example from the swagger
    (PlatformsFileUploadResponse and PlatformsFileRetrieveResponse).
    """

    def test_exposes_every_upload_response_field(self):
        response = ResponseWrapper(None, {
            'id': 'file_6lbss42ezvoufcb2beo76rvwly',
            'maximum_size_in_bytes': 4194304,
            'document_types_for_purpose': ['image/jpeg', 'image/png', 'image/jpg'],
            '_links': {
                'upload': {
                    'href': 'https://s3.eu-west-1.amazonaws.com/mp-files-api-staging-prod/'
                            'ent_ociwguf5a5fe3ndmpnvpnwsi3e/file_6lbss42ezvoufcb2beo76rvwly'
                            '?AWSAccessKeyId=ASIX4BFJOBCQFLAMPKU3&Expires=1661355993&x-amz-security-token=some_token',
                },
                'self': {'href': 'https://files.checkout.com/files/file_6lbss42ezvoufcb2beo76rvwly'},
            },
        })

        assert response.id == 'file_6lbss42ezvoufcb2beo76rvwly'
        assert response.maximum_size_in_bytes == 4194304
        assert response.document_types_for_purpose == ['image/jpeg', 'image/png', 'image/jpg']
        assert response._links.upload.href == (
            'https://s3.eu-west-1.amazonaws.com/mp-files-api-staging-prod/ent_ociwguf5a5fe3ndmpnvpnwsi3e/'
            'file_6lbss42ezvoufcb2beo76rvwly?AWSAccessKeyId=ASIX4BFJOBCQFLAMPKU3&Expires=1661355993'
            '&x-amz-security-token=some_token')
        assert response._links.self.href == 'https://files.checkout.com/files/file_6lbss42ezvoufcb2beo76rvwly'

    def test_exposes_every_retrieve_response_field(self):
        response = ResponseWrapper(None, {
            'id': 'file_6lbss42ezvoufcb2beo76rvwly',
            'status': 'invalid',
            'status_reasons': ['InvalidMimeType'],
            'size': 1024,
            'mime_type': 'application/pdf',
            'uploaded_on': '2020-12-01T15:01:01.0000000+00:00',
            'purpose': 'identity_verification',
            '_links': {
                'download': {
                    'href': 'https://s3.eu-west-1.amazonaws.com/mp-files-api-clean-prod/'
                            'ent_ociwguf5a5fe3ndmpnvpnwsi3e/file_6lbss42ezvoufcb2beo76rvwly'
                            '?X-Amz-Expires=3600&x-amz-security-token=some_token',
                },
                'self': {'href': 'https://files.checkout.com/files/file_6lbss42ezvoufcb2beo76rvwly'},
            },
        })

        assert response.id == 'file_6lbss42ezvoufcb2beo76rvwly'
        assert response.status == 'invalid'
        assert response.status_reasons == ['InvalidMimeType']
        assert response.size == 1024
        assert response.mime_type == 'application/pdf'
        # The SDK does not parse response dates: the seven fractional digits reach the caller unchanged.
        assert response.uploaded_on == '2020-12-01T15:01:01.0000000+00:00'
        assert response.purpose == 'identity_verification'
        assert response._links.download.href == (
            'https://s3.eu-west-1.amazonaws.com/mp-files-api-clean-prod/ent_ociwguf5a5fe3ndmpnvpnwsi3e/'
            'file_6lbss42ezvoufcb2beo76rvwly?X-Amz-Expires=3600&x-amz-security-token=some_token')
        assert response._links.self.href == 'https://files.checkout.com/files/file_6lbss42ezvoufcb2beo76rvwly'
