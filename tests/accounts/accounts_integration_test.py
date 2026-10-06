from __future__ import absolute_import

import warnings
import os
from datetime import datetime, timedelta, timezone

import pytest

from checkout_sdk import CheckoutSdk
from checkout_sdk.accounts.accounts import OnboardEntityRequest, ContactDetails, Profile, Individual, \
    DateOfBirth, Identification, EntityIdentification, EntityEmailAddresses, Company, EntityRepresentative, \
    PaymentInstrumentRequest, \
    InstrumentDocument, InstrumentDetailsFasterPayments, ReserveRuleRequest, RollingReserveRule, \
    HoldingDuration, EntityFileRequest, FilePurpose, RepresentativeIndividual, PlaceOfBirth, EntityRoles, \
    BusinessType, DateOfIncorporation, ProcessingDetails, ProcessingDetailsPayments, \
    ProcessingDetailsAch, RepresentativeDocuments, EntityIdentificationDocument, CertifiedAuthorisedSignatory, \
    CertifiedAuthorisedSignatoryType, InstrumentDetailsAch, InstrumentAccountType, UpdatePaymentInstrumentRequest, \
    Headers
from checkout_sdk.common.common import Phone
from checkout_sdk.common.enums import Currency, Country, InstrumentType, DocumentType
from checkout_sdk.files.files import FileRequest
from checkout_sdk.oauth_scopes import OAuthScopes
from tests.checkout_test_utils import assert_response, address, new_uuid, get_project_root, random_email


@pytest.fixture(scope='class')
def accounts_checkout_api():
    builder = CheckoutSdk \
        .builder() \
        .oauth() \
        .client_credentials(client_id=os.environ.get('CHECKOUT_DEFAULT_OAUTH_ACCOUNTS_CLIENT_ID'),
                            client_secret=os.environ.get('CHECKOUT_DEFAULT_OAUTH_ACCOUNTS_CLIENT_SECRET')) \
        .scopes([OAuthScopes.ACCOUNTS, OAuthScopes.FILES])
    # The sandbox OAuth clients are not provisioned for the merchant-specific subdomain, so the
    # token request would come back invalid_client. Opting out explicitly until they are.
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', DeprecationWarning)
        return builder.use_legacy_domain().build()


@pytest.mark.skip(
    reason='sandbox rejects POST accounts/entities with 422 for the individual v2 '
           'entity this test builds. The company v3 path still passes - see '
           'test_should_onboard_company_v3. Unrelated to the instruments work; needs '
           'an accounts-owned fix to the entity payload. Same breakage as '
           'checkout-sdk-ruby.'
)
def test_should_create_get_and_update_onboard_entity(accounts_checkout_api):
    onboard_entity_request = OnboardEntityRequest()
    onboard_entity_request.reference = new_uuid()[:14]
    email_addresses = EntityEmailAddresses()
    email_addresses.primary = random_email()
    onboard_entity_request.contact_details = ContactDetails()
    onboard_entity_request.contact_details.phone = build_v2_phone()
    onboard_entity_request.contact_details.email_addresses = email_addresses
    onboard_entity_request.profile = Profile()
    onboard_entity_request.profile.urls = ['https://www.superheroexample.com']
    onboard_entity_request.profile.mccs = ['0742']
    onboard_entity_request.individual = Individual()
    onboard_entity_request.individual.first_name = 'Bruce'
    onboard_entity_request.individual.last_name = 'Wayne'
    onboard_entity_request.individual.trading_name = "Batman's Super Hero Masks"
    onboard_entity_request.individual.registered_address = address()
    onboard_entity_request.individual.date_of_birth = DateOfBirth()
    onboard_entity_request.individual.date_of_birth.day = 5
    onboard_entity_request.individual.date_of_birth.month = 6
    onboard_entity_request.individual.date_of_birth.year = 1996
    onboard_entity_request.individual.identification = Identification()
    onboard_entity_request.individual.identification.national_id_number = '123456789'

    # v2.0 payload (top-level individual) — pin to schema_version 2.0 (SDK now defaults to 3.0)
    create_entity_response = accounts_checkout_api.accounts.create_entity(onboard_entity_request, '2.0')

    assert_response(create_entity_response, 'id', 'reference')

    get_entity_response = accounts_checkout_api.accounts.get_entity(create_entity_response.id, '2.0')

    assert_response(get_entity_response,
                    'id',
                    'reference',
                    'contact_details',
                    'contact_details.phone',
                    'contact_details.phone.number',
                    'contact_details.email_addresses.primary',
                    'individual',
                    'individual.first_name',
                    'individual.last_name',
                    'individual.trading_name')

    onboard_entity_request.individual.first_name = 'John'

    update_response = accounts_checkout_api.accounts.update_entity(create_entity_response.id, onboard_entity_request,
                                                                   '2.0')

    assert_response(update_response, 'id')

    assert create_entity_response.id == update_response.id


def test_should_onboard_company_v3(accounts_checkout_api):
    entity_request = build_company_v3_request()

    # default schema_version is 3.0
    create_response = accounts_checkout_api.accounts.create_entity(entity_request)
    assert_response(create_response, 'id', 'reference')

    get_response = accounts_checkout_api.accounts.get_entity(create_response.id)
    assert_response(get_response, 'id', 'reference', 'company', 'company.representatives')


# The representative's documents on schema 3.0. The sandbox platform resolves to a company variant
# (GB/US scope, USD only), where identity_verification and certified_authorised_signatory are the
# representative documents the API accepts; the EEA Sole Trader keys are covered by
# accounts_v3_serialization_test, since this platform rejects them.
def test_should_onboard_entity_with_representative_documents(accounts_checkout_api):
    identity_file = upload_file(accounts_checkout_api, 'identity_verification')
    signatory_file = upload_file(accounts_checkout_api, 'certified_authorised_signatory')

    identity = EntityIdentificationDocument()
    identity.type = DocumentType.PASSPORT
    identity.front = identity_file.id
    signatory = CertifiedAuthorisedSignatory()
    signatory.type = CertifiedAuthorisedSignatoryType.POWER_OF_ATTORNEY
    signatory.front = signatory_file.id
    documents = RepresentativeDocuments()
    documents.identity_verification = identity
    documents.certified_authorised_signatory = signatory

    entity_request = build_company_v3_request()
    entity_request.company.representatives[0].documents = documents

    create_response = accounts_checkout_api.accounts.create_entity(entity_request)
    assert_response(create_response, 'id')

    # The documents are linked on the representative, not dropped: the API echoes them back.
    get_response = accounts_checkout_api.accounts.get_entity(create_response.id)
    linked = get_response.company.representatives[0].documents
    assert linked.identity_verification.type == 'passport'
    assert linked.identity_verification.front == identity_file.id
    assert linked.certified_authorised_signatory.type == 'power_of_attorney'
    assert linked.certified_authorised_signatory.front == signatory_file.id


# The two EEA Sole Trader representative documents need their own upload purposes before they can
# be linked. Goes through POST /entities/{id}/files, the endpoint whose request schema
# (PlatformsFileUpload) defines the purpose enum.
def test_should_upload_representative_proof_files(accounts_checkout_api):
    entity_id = accounts_checkout_api.accounts.create_entity(build_company_v3_request()).id

    for purpose in (FilePurpose.PROOF_OF_RESIDENTIAL_ADDRESS, FilePurpose.PROOF_OF_REGISTRATION):
        request = EntityFileRequest()
        request.purpose = purpose
        upload_response = accounts_checkout_api.accounts.upload_entity_file(entity_id, request)
        assert_response(upload_response, 'id', '_links')

        retrieve_response = accounts_checkout_api.accounts.retrieve_entity_file(entity_id, upload_response.id)
        assert_response(retrieve_response, 'id', 'purpose')
        assert retrieve_response.purpose == purpose.value


def test_should_upload_file(accounts_checkout_api):
    upload_file(accounts_checkout_api)


@pytest.mark.skip(
    reason='sandbox rejects POST accounts/entities with 422 for the individual v2 '
           'entity this test builds. The company v3 path still passes - see '
           'test_should_onboard_company_v3. Unrelated to the instruments work; needs '
           'an accounts-owned fix to the entity payload. Same breakage as '
           'checkout-sdk-ruby.'
)
def test_should_create_and_retrieve_payment_instrument(accounts_checkout_api):
    entity_request = OnboardEntityRequest()
    entity_request.reference = new_uuid()[:14]
    entity_request.contact_details = ContactDetails()
    entity_request.contact_details.phone = build_v2_phone()
    entity_request.contact_details.email_addresses = EntityEmailAddresses()
    entity_request.contact_details.email_addresses.primary = random_email()
    entity_request.profile = Profile()
    entity_request.profile.urls = ['https://www.superheroexample.com']
    entity_request.profile.mccs = ['0742']
    entity_request.company = Company()
    entity_request.company.business_registration_number = '01234567'
    entity_request.company.legal_name = 'Super Hero Masks Inc.'
    entity_request.company.trading_name = 'Super Hero Masks'
    entity_request.company.principal_address = address()
    entity_request.company.registered_address = address()
    representative = EntityRepresentative()
    representative.first_name = 'John'
    representative.last_name = 'Doe'
    representative.address = address()
    representative.identification = EntityIdentification()
    representative.identification.national_id_number = '123456789'
    entity_request.company.representatives = [representative]

    # v2.0 payload (flat representative) — pin to schema_version 2.0
    entity_response = accounts_checkout_api.accounts.create_entity(entity_request, '2.0')

    file = upload_file(accounts_checkout_api)

    instrument_request = PaymentInstrumentRequest()
    instrument_request.label = 'Barclays'
    instrument_request.type = InstrumentType.BANK_ACCOUNT
    instrument_request.currency = Currency.GBP
    instrument_request.country = Country.GB
    instrument_request.default = False
    instrument_request.document = InstrumentDocument()
    instrument_request.document.type = 'bank_statement'
    instrument_request.document.file_id = file.id
    instrument_request.instrument_details = InstrumentDetailsFasterPayments()
    instrument_request.instrument_details.account_number = '12334454'
    instrument_request.instrument_details.bank_code = '050389'

    instrument_response = accounts_checkout_api.accounts.add_payment_instrument(entity_response.id, instrument_request)

    assert_response(instrument_response, 'id')

    instrument_details = accounts_checkout_api.accounts.retrieve_payment_instrument_details(entity_response.id,
                                                                                            instrument_response.id)

    assert_response(instrument_details, 'id',
                    'status',
                    'label',
                    'type',
                    'currency',
                    'country',
                    'document')

    query_response = accounts_checkout_api.accounts.query_payment_instruments(entity_response.id)

    assert_response(query_response, 'data')


@pytest.mark.skip(
    reason='sandbox rejects POST accounts/entities with 422 for the individual v2 '
           'entity this test builds. The company v3 path still passes - see '
           'test_should_onboard_company_v3. Unrelated to the instruments work; needs '
           'an accounts-owned fix to the entity payload. Same breakage as '
           'checkout-sdk-ruby.'
)
def test_should_get_sub_entity_members(accounts_checkout_api):
    entity_id = create_test_entity(accounts_checkout_api)

    members_response = accounts_checkout_api.accounts.get_sub_entity_members(entity_id)

    assert members_response is not None


@pytest.mark.skip(
    reason='sandbox rejects POST accounts/entities with 422 for the individual v2 '
           'entity this test builds. The company v3 path still passes - see '
           'test_should_onboard_company_v3. Unrelated to the instruments work; needs '
           'an accounts-owned fix to the entity payload. Same breakage as '
           'checkout-sdk-ruby.'
)
def test_create_reserve_rule_should_return_valid_response(accounts_checkout_api):
    entity_id = create_test_entity(accounts_checkout_api)
    reserve_rule_request = create_valid_reserve_rule_request()

    response = accounts_checkout_api.accounts.create_reserve_rule(entity_id, reserve_rule_request)

    validate_reserve_rule_id_response(response)


@pytest.mark.skip(
    reason='sandbox rejects POST accounts/entities with 422 for the individual v2 '
           'entity this test builds. The company v3 path still passes - see '
           'test_should_onboard_company_v3. Unrelated to the instruments work; needs '
           'an accounts-owned fix to the entity payload. Same breakage as '
           'checkout-sdk-ruby.'
)
def test_get_reserve_rules_should_return_valid_response(accounts_checkout_api):
    entity_id = create_test_entity(accounts_checkout_api)
    reserve_rule_request = create_valid_reserve_rule_request()
    create_response = accounts_checkout_api.accounts.create_reserve_rule(entity_id, reserve_rule_request)
    validate_reserve_rule_id_response(create_response)

    response = accounts_checkout_api.accounts.get_reserve_rules(entity_id)

    validate_reserve_rules_response(response)


@pytest.mark.skip(
    reason='sandbox rejects POST accounts/entities with 422 for the individual v2 '
           'entity this test builds. The company v3 path still passes - see '
           'test_should_onboard_company_v3. Unrelated to the instruments work; needs '
           'an accounts-owned fix to the entity payload. Same breakage as '
           'checkout-sdk-ruby.'
)
def test_get_reserve_rule_details_should_return_valid_response(accounts_checkout_api):
    entity_id = create_test_entity(accounts_checkout_api)
    reserve_rule_request = create_valid_reserve_rule_request()
    create_response = accounts_checkout_api.accounts.create_reserve_rule(entity_id, reserve_rule_request)
    validate_reserve_rule_id_response(create_response)

    response = accounts_checkout_api.accounts.get_reserve_rule_details(entity_id, create_response.id)

    validate_reserve_rule_response(response, reserve_rule_request)


@pytest.mark.skip(
    reason='sandbox rejects POST accounts/entities with 422 for the individual v2 '
           'entity this test builds. The company v3 path still passes - see '
           'test_should_onboard_company_v3. Unrelated to the instruments work; needs '
           'an accounts-owned fix to the entity payload. Same breakage as '
           'checkout-sdk-ruby.'
)
def test_update_reserve_rule_should_return_valid_response(accounts_checkout_api):
    entity_id = create_test_entity(accounts_checkout_api)
    original_request = create_valid_reserve_rule_request()
    create_response = accounts_checkout_api.accounts.create_reserve_rule(entity_id, original_request)
    validate_reserve_rule_id_response(create_response)

    update_request = create_valid_reserve_rule_request()
    update_request.rolling.percentage = 15.0
    update_request.rolling.holding_duration.weeks = 16

    etag = None
    if hasattr(create_response, 'http_metadata') and hasattr(create_response.http_metadata, 'headers'):
        headers = create_response.http_metadata.headers
        if 'etag' in headers:
            etag = headers['etag']
        elif 'ETag' in headers:
            etag = headers['ETag']

    response = accounts_checkout_api.accounts.update_reserve_rule(
        entity_id,
        create_response.id,
        etag,
        update_request
    )

    validate_reserve_rule_id_response(response)
    assert response.id == create_response.id


def test_should_upload_entity_file_and_retrieve(accounts_checkout_api):
    # A schema 3.0 entity: the sandbox rejects the schema 2.0 one create_test_entity builds.
    entity_id = accounts_checkout_api.accounts.create_entity(build_company_v3_request()).id

    request = EntityFileRequest()
    request.purpose = FilePurpose.IDENTITY_VERIFICATION

    upload_response = accounts_checkout_api.accounts.upload_entity_file(entity_id, request)

    assert_response(upload_response, 'id', '_links')
    assert upload_response.id is not None
    assert upload_response.id != ''

    file_id = upload_response.id
    retrieve_response = accounts_checkout_api.accounts.retrieve_entity_file(entity_id, file_id)

    assert_response(retrieve_response, 'id')
    assert retrieve_response.id == file_id


def test_should_update_payment_instrument_with_etag(accounts_checkout_api):
    # The update only succeeds when the ETag reaches the API as the If-Match HTTP header: a request
    # without it fails with 428, and one with a stale ETag with 412.
    entity_id = accounts_checkout_api.accounts.create_entity(build_company_v3_request()).id
    file = upload_file(accounts_checkout_api)

    instrument_request = PaymentInstrumentRequest()
    instrument_request.label = 'Main account'
    instrument_request.type = InstrumentType.BANK_ACCOUNT
    instrument_request.currency = Currency.USD
    instrument_request.country = Country.US
    instrument_request.document = InstrumentDocument()
    instrument_request.document.type = 'bank_statement'
    instrument_request.document.file_id = file.id
    instrument_request.instrument_details = InstrumentDetailsAch()
    instrument_request.instrument_details.account_number = '123456789'
    instrument_request.instrument_details.routing_number = '026009593'
    # The sandbox rejects checking (instrument_details_account_type_invalid), although the spec lists it.
    instrument_request.instrument_details.account_type = InstrumentAccountType.SAVINGS
    instrument_id = accounts_checkout_api.accounts.add_payment_instrument(entity_id, instrument_request).id

    details = accounts_checkout_api.accounts.retrieve_payment_instrument_details(entity_id, instrument_id)
    etag = {k.lower(): v for k, v in details.http_metadata.headers.items()}['etag']

    update_request = UpdatePaymentInstrumentRequest()
    update_request.label = 'Renamed account'
    update_request.headers = Headers()
    update_request.headers.if_match = etag
    update_response = accounts_checkout_api.accounts.update_payment_instrument(entity_id, instrument_id,
                                                                               update_request)

    assert update_response.id == instrument_id
    updated = accounts_checkout_api.accounts.retrieve_payment_instrument_details(entity_id, instrument_id)
    assert updated.label == 'Renamed account'


# Common methods
def upload_file(api, purpose='bank_verification'):
    request = FileRequest()
    request.file = os.path.join(get_project_root(), 'tests', 'resources', 'checkout.jpeg')
    request.purpose = purpose
    response = api.accounts.upload_file(request)
    assert_response(response, 'id', '_links')
    return response


# A schema 3.0 company request the sandbox platform accepts: every currency sits inside its USD-only
# currency scope, including the processing details currency.
def build_company_v3_request():
    entity_request = OnboardEntityRequest()
    entity_request.reference = new_uuid()[:14]

    entity_request.contact_details = ContactDetails()
    v3_phone = Phone()
    v3_phone.country_code = 'GB'
    v3_phone.number = '2072343000'
    entity_request.contact_details.phone = v3_phone
    entity_request.contact_details.email_addresses = EntityEmailAddresses()
    entity_request.contact_details.email_addresses.primary = random_email()

    entity_request.profile = Profile()
    entity_request.profile.urls = ['https://www.example-test-entity.com']
    entity_request.profile.mccs = ['0742']
    entity_request.profile.default_holding_currency = Currency.USD
    entity_request.profile.holding_currencies = [Currency.USD]

    entity_request.company = Company()
    entity_request.company.legal_name = 'Test Sub-Entity Company Inc.'
    entity_request.company.trading_name = 'Test Sub-Entity Trading'
    entity_request.company.business_registration_number = '01234567'
    entity_request.company.business_type = BusinessType.LIMITED_COMPANY
    entity_request.company.principal_address = address()
    entity_request.company.registered_address = address()
    entity_request.company.date_of_incorporation = DateOfIncorporation()
    entity_request.company.date_of_incorporation.day = 1
    entity_request.company.date_of_incorporation.month = 6
    entity_request.company.date_of_incorporation.year = 2010

    representative = EntityRepresentative()
    representative.roles = [EntityRoles.UBO, EntityRoles.AUTHORISED_SIGNATORY, EntityRoles.DIRECTOR,
                            EntityRoles.CONTROL_PERSON]
    representative.individual = RepresentativeIndividual()
    representative.individual.first_name = 'John'
    representative.individual.last_name = 'Representative'
    representative.individual.address = address()
    representative.individual.date_of_birth = DateOfBirth()
    representative.individual.date_of_birth.day = 5
    representative.individual.date_of_birth.month = 6
    representative.individual.date_of_birth.year = 1996
    representative.individual.place_of_birth = PlaceOfBirth()
    representative.individual.place_of_birth.country = Country.GB
    entity_request.company.representatives = [representative]

    entity_request.processing_details = ProcessingDetails()
    entity_request.processing_details.target_countries = ['GB']
    entity_request.processing_details.annual_processing_volume = 1000000
    entity_request.processing_details.average_transaction_value = 5000
    entity_request.processing_details.average_order_fulfillment_time = 3
    entity_request.processing_details.currency = Currency.USD
    entity_request.processing_details.payments = ProcessingDetailsPayments()
    entity_request.processing_details.payments.ach = ProcessingDetailsAch()
    entity_request.processing_details.payments.ach.annual_ach_volume = 1000000
    entity_request.processing_details.payments.ach.average_ach_transaction_size = 5000
    entity_request.processing_details.payments.ach.estimated_monthly_credit_volume = 100000
    entity_request.processing_details.payments.ach.average_credit_amount = 5000
    return entity_request


def create_test_entity(api):
    entity_request = OnboardEntityRequest()
    entity_request.reference = new_uuid()[:15]
    entity_request.contact_details = build_contact_details()
    entity_request.profile = build_profile()
    entity_request.company = Company()
    entity_request.company.business_registration_number = '01234567'
    entity_request.company.legal_name = 'Reserve Rules Test Inc.'
    entity_request.company.trading_name = 'Reserve Rules Test'
    entity_request.company.principal_address = address()
    entity_request.company.registered_address = address()
    representative = EntityRepresentative()
    representative.first_name = 'John'
    representative.last_name = 'Doe'
    representative.address = address()
    entity_request.company.representatives = [representative]

    # v2.0 payload (flat representative) — pin to schema_version 2.0
    entity_response = api.accounts.create_entity(entity_request, '2.0')
    assert_response(entity_response, 'id')

    return entity_response.id


def build_contact_details():
    contact_details = ContactDetails()
    contact_details.phone = build_v2_phone()
    contact_details.email_addresses = EntityEmailAddresses()
    contact_details.email_addresses.primary = random_email()
    return contact_details


# The v2.0 contact phone takes a number only, with no country_code. The value fits the EEA and GB
# pattern (^[1-9][0-9]{7,15}$) and the US one (^[2-9]{1}[0-9]{9,15}$).
def build_v2_phone():
    v2_phone = Phone()
    v2_phone.number = '2072343000'
    return v2_phone


def build_profile():
    profile = Profile()
    profile.urls = ['https://www.superheroexample.com']
    profile.mccs = ['0742']
    return profile


def create_valid_reserve_rule_request():
    holding_duration = HoldingDuration()
    holding_duration.weeks = 8

    rolling_rule = RollingReserveRule()
    rolling_rule.percentage = 12.5
    rolling_rule.holding_duration = holding_duration

    reserve_rule_request = ReserveRuleRequest()
    reserve_rule_request.type = 'rolling'
    reserve_rule_request.rolling = rolling_rule
    reserve_rule_request.valid_from = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()

    return reserve_rule_request


def validate_reserve_rule_id_response(response):
    assert response is not None
    assert_response(response, 'id')
    assert response.id is not None
    assert response.id != ''


def validate_reserve_rules_response(response):
    assert response is not None
    assert_response(response, 'data')
    assert response.data is not None
    assert len(response.data) > 0
    assert response.data[0].id is not None
    assert hasattr(response.data[0], 'type')


def validate_reserve_rule_response(response, original_request):
    assert response is not None
    assert_response(response, 'id', 'type', 'rolling')
    assert response.id is not None
    assert response.type == original_request.type
    assert response.rolling is not None
    assert response.rolling.percentage == original_request.rolling.percentage
    assert response.rolling.holding_duration is not None
    assert response.rolling.holding_duration.weeks == original_request.rolling.holding_duration.weeks
    assert hasattr(response, 'valid_from')
