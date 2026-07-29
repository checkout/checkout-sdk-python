import json

from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.common.enums import Country, Currency
from checkout_sdk.accounts.accounts import (
    ProcessingDetails, ProcessingDetailsPayments, ProcessingDetailsAch,
    AgreedTerms, Company, BusinessType, DateOfIncorporation,
    EntityRepresentative, RepresentativeIndividual, Citizenship, NationalIdType,
    CompanyPosition, EntityRoles, FinancialStatements, FinancialStatementsType,
    OnboardSubEntityDocuments, OnboardEntityRequest,
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
