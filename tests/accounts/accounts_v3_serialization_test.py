import json

from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.common.common import Address
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
    FilePurpose,
)


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class TestAccountsV3Serialization:

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
        details.highest_transaction_value = 25000
        details.currency = Currency.GBP
        details.settlement_country = 'GB'
        details.target_countries = ['GB']
        details.payments = payments

        assert _serialize(details) == {
            'annual_processing_volume': 1000000,
            'average_transaction_value': 5000,
            'average_order_fulfillment_time': 3,
            'highest_transaction_value': 25000,
            'currency': 'GBP',
            'settlement_country': 'GB',
            'target_countries': ['GB'],
            'payments': {
                'ach': {
                    'annual_ach_volume': 1000000,
                    'average_ach_transaction_size': 5000,
                    'estimated_monthly_credit_volume': 100000,
                    'average_credit_amount': 5000,
                }
            },
        }

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

    def test_serializes_company_v3_fields(self):
        date_of_incorporation = DateOfIncorporation()
        date_of_incorporation.day = 1
        date_of_incorporation.month = 6
        date_of_incorporation.year = 2010
        company = Company()
        company.legal_name = 'Super Hero Masks Inc.'
        company.trading_name = 'Super Hero Masks'
        company.business_registration_number = '01234567'
        company.business_type = BusinessType.LIMITED_COMPANY
        company.additional_trading_names = ['SHM']
        company.is_registered_company = True
        company.date_of_incorporation = date_of_incorporation

        assert _serialize(company) == {
            'legal_name': 'Super Hero Masks Inc.',
            'trading_name': 'Super Hero Masks',
            'business_registration_number': '01234567',
            'business_type': 'limited_company',
            'additional_trading_names': ['SHM'],
            'is_registered_company': True,
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
        individual.national_id_number = 'AB123456C'
        individual.email_address = 'john@example.com'
        representative = EntityRepresentative()
        representative.id = 'rep_00000000000000000000000000'
        representative.individual = individual
        representative.company_position = CompanyPosition.CEO
        representative.ownership_percentage = 100
        representative.roles = [EntityRoles.UBO, EntityRoles.AUTHORISED_SIGNATORY,
                                EntityRoles.DIRECTOR, EntityRoles.CONTROL_PERSON]

        assert _serialize(representative) == {
            'id': 'rep_00000000000000000000000000',
            'individual': {
                'first_name': 'John',
                'last_name': 'Doe',
                'citizenships': [{'type': 'citizenship', 'country': 'US'}],
                'national_id_type': 'ssn',
                'national_id_number': 'AB123456C',
                'email_address': 'john@example.com',
            },
            'company_position': 'ceo',
            'ownership_percentage': 100,
            'roles': ['ubo', 'authorised_signatory', 'director', 'control_person'],
        }

    def test_serializes_representative_documents(self):
        identity = EntityIdentificationDocument()
        identity.type = DocumentType.PASSPORT
        identity.front = 'file_identity_front'
        identity.back = 'file_identity_back'
        signatory = CertifiedAuthorisedSignatory()
        signatory.type = CertifiedAuthorisedSignatoryType.POWER_OF_ATTORNEY
        signatory.front = 'file_signatory'
        residential = ProofOfResidentialAddress()
        residential.type = ProofOfResidentialAddressType.PROOF_OF_ADDRESS
        residential.front = 'file_residential'
        registration = ProofOfRegistration()
        registration.type = ProofOfRegistrationType.EXTRACT_FROM_TRADE_REGISTER
        registration.front = 'file_registration'
        documents = RepresentativeDocuments()
        documents.identity_verification = identity
        documents.certified_authorised_signatory = signatory
        documents.proof_of_residential_address = residential
        documents.proof_of_registration = registration

        assert _serialize(documents) == {
            'identity_verification': {'type': 'passport', 'front': 'file_identity_front', 'back': 'file_identity_back'},
            'certified_authorised_signatory': {'type': 'power_of_attorney', 'front': 'file_signatory'},
            'proof_of_residential_address': {'type': 'proof_of_address', 'front': 'file_residential'},
            'proof_of_registration': {'type': 'extract_from_trade_register', 'front': 'file_registration'},
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
            'proof_of_registration': {'type': 'extract_from_trade_register', 'front': 'file_proofofregistrationaaaaaaa'},
        }
        assert result['documents'] == {
            'bank_verification': {'type': 'bank_statement', 'front': 'file_bankverificationaaaaaaaaaa'}}
        # Key-level check on the raw body, so a naming change cannot pass silently.
        assert '"proof_of_residential_address": {' in body
        assert '"proof_of_registration": {' in body

    # The API rejects any key on company.representatives[].documents other than these four
    # (additionalProperties: false), so an attribute added here by mistake would fail the request.
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
        financial_statements.front = 'file_00000000000000000000000000'
        documents = OnboardSubEntityDocuments()
        documents.financial_statements = financial_statements

        assert _serialize(documents) == {
            'financial_statements': {
                'type': 'financial_statements',
                'front': 'file_00000000000000000000000000',
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
        company.business_type = BusinessType.LIMITED_COMPANY
        company.representatives = [representative]
        payments = ProcessingDetailsPayments()
        payments.ach = ProcessingDetailsAch()
        payments.ach.annual_ach_volume = 1000000
        processing_details = ProcessingDetails()
        processing_details.currency = Currency.GBP
        processing_details.payments = payments
        request = OnboardEntityRequest()
        request.reference = 'ref_1'
        request.company = company
        request.processing_details = processing_details

        result = _serialize(request)

        assert result['reference'] == 'ref_1'
        assert result['company']['legal_name'] == 'Super Hero Masks Inc.'
        assert result['company']['business_type'] == 'limited_company'
        assert result['company']['representatives'][0]['individual']['first_name'] == 'John'
        assert result['company']['representatives'][0]['roles'] == ['ubo']
        assert result['processing_details']['currency'] == 'GBP'
        assert result['processing_details']['payments']['ach']['annual_ach_volume'] == 1000000

    def test_serializes_all_thirteen_documents_fields(self):
        documents = OnboardSubEntityDocuments()

        identity_verification = EntityIdentificationDocument()
        identity_verification.type = DocumentType.NATIONAL_IDENTITY_CARD
        identity_verification.front = 'file_identity_front'
        identity_verification.back = 'file_identity_back'
        documents.identity_verification = identity_verification

        company_verification = CompanyVerification()
        company_verification.type = CompanyVerificationType.INCORPORATION_DOCUMENT
        company_verification.front = 'file_company_verification'
        documents.company_verification = company_verification

        articles_of_association = ArticlesOfAssociation()
        articles_of_association.type = ArticlesOfAssociationType.ARTICLES_OF_ASSOCIATION
        articles_of_association.front = 'file_articles_of_association'
        documents.articles_of_association = articles_of_association

        bank_verification = BankVerification()
        bank_verification.type = BankVerificationType.BANK_STATEMENT
        bank_verification.front = 'file_bank_verification'
        documents.bank_verification = bank_verification

        shareholder_structure = ShareholderStructure()
        shareholder_structure.type = ShareholderStructureType.CERTIFIED_SHAREHOLDER_STRUCTURE
        shareholder_structure.front = 'file_shareholder_structure'
        documents.shareholder_structure = shareholder_structure

        proof_of_legality = ProofOfLegality()
        proof_of_legality.type = ProofOfLegalityType.PROOF_OF_LEGALITY
        proof_of_legality.front = 'file_proof_of_legality'
        documents.proof_of_legality = proof_of_legality

        proof_of_principal_address = ProofOfPrincipalAddress()
        proof_of_principal_address.type = ProofOfPrincipalAddressType.PROOF_OF_ADDRESS
        proof_of_principal_address.front = 'file_proof_of_principal_address'
        documents.proof_of_principal_address = proof_of_principal_address

        tax_verification = TaxVerification()
        tax_verification.type = TaxVerificationType.EIN_LETTER
        tax_verification.front = 'file_tax_verification'
        documents.tax_verification = tax_verification

        financial_verification = FinancialVerification()
        financial_verification.type = FinancialVerificationType.FINANCIAL_STATEMENT
        financial_verification.front = 'file_financial_verification'
        documents.financial_verification = financial_verification

        financial_statements = FinancialStatements()
        financial_statements.type = FinancialStatementsType.FINANCIAL_STATEMENTS
        financial_statements.front = 'file_financial_statements'
        documents.financial_statements = financial_statements

        additional_document1 = AdditionalDocument()
        additional_document1.front = 'file_additional_document1'
        documents.additional_document1 = additional_document1
        additional_document2 = AdditionalDocument()
        additional_document2.front = 'file_additional_document2'
        documents.additional_document2 = additional_document2
        additional_document3 = AdditionalDocument()
        additional_document3.front = 'file_additional_document3'
        documents.additional_document3 = additional_document3

        result = _serialize(documents)

        expected_fields = [
            'identity_verification', 'company_verification', 'articles_of_association',
            'bank_verification', 'shareholder_structure', 'proof_of_legality',
            'proof_of_principal_address', 'tax_verification', 'financial_verification',
            'financial_statements', 'additional_document1', 'additional_document2',
            'additional_document3',
        ]
        assert sorted(result.keys()) == sorted(expected_fields)
        for field in expected_fields:
            assert 'front' in result[field], f'{field} must serialize a front'
        # identity_verification is the only document that carries a back
        assert result['identity_verification']['back'] == 'file_identity_back'
        assert result['articles_of_association'] == {
            'type': 'articles_of_association', 'front': 'file_articles_of_association'
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
