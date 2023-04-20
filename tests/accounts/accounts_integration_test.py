from __future__ import absolute_import

import os

import pytest

from checkout_sdk import CheckoutSdk
from checkout_sdk.accounts.accounts import OnboardEntityRequest, ContactDetails, Profile, Individual, \
    DateOfBirth, Identification, EntityEmailAddresses, Company, EntityRepresentative, PaymentInstrumentRequest, \
    InstrumentDocument, InstrumentDetailsFasterPayments
from checkout_sdk.checkout_api import CheckoutApi
from checkout_sdk.common.enums import Currency, Country, InstrumentType
from checkout_sdk.files.files import FileRequest
from checkout_sdk.oauth_scopes import OAuthScopes
from tests.checkout_test_utils import assert_response, phone, address, new_uuid, get_project_root, random_email


@pytest.fixture(scope='class')
def accounts_checkout_api():
    return CheckoutSdk \
        .builder() \
        .oauth() \
        .client_credentials(client_id=os.environ.get('CHECKOUT_DEFAULT_OAUTH_ACCOUNTS_CLIENT_ID'),
                            client_secret=os.environ.get('CHECKOUT_DEFAULT_OAUTH_ACCOUNTS_CLIENT_SECRET')) \
        .scopes([OAuthScopes.ACCOUNTS, OAuthScopes.FILES]) \
        .build()


def upload_file(oauth_api: CheckoutApi):
    request = FileRequest()
    request.file = os.path.join(get_project_root(), 'tests', 'resources', 'checkout.jpeg')
    request.purpose = 'bank_verification'
    response = oauth_api.accounts.upload_file(request)
    assert_response(response, 'id', '_links')
    return response


def test_should_create_get_and_update_onboard_entity(oauth_api):
    onboard_entity_request = OnboardEntityRequest()
    onboard_entity_request.reference = new_uuid()[:14]
    email_addresses = EntityEmailAddresses()
    email_addresses.primary = random_email()
    onboard_entity_request.contact_details = ContactDetails()
    onboard_entity_request.contact_details.phone = phone()
    onboard_entity_request.contact_details.email_addresses = email_addresses
    onboard_entity_request.profile = Profile()
    onboard_entity_request.profile.urls = ['https://www.superheroexample.com']
    onboard_entity_request.profile.mccs = ['0742']
    onboard_entity_request.individual = Individual()
    onboard_entity_request.individual.first_name = 'Bruce'
    onboard_entity_request.individual.last_name = 'Wayne'
    onboard_entity_request.individual.trading_name = "Batman's Super Hero Masks"
    onboard_entity_request.individual.registered_address = address()
    onboard_entity_request.individual.national_tax_id = 'TAX123456'
    onboard_entity_request.individual.date_of_birth = DateOfBirth()
    onboard_entity_request.individual.date_of_birth.day = 5
    onboard_entity_request.individual.date_of_birth.month = 6
    onboard_entity_request.individual.date_of_birth.year = 1996
    onboard_entity_request.individual.identification = Identification()
    onboard_entity_request.individual.identification.national_id_number = 'AB123456C'

    create_entity_response = oauth_api.accounts.create_entity(onboard_entity_request)

    assert_response(create_entity_response, 'id', 'reference')

    get_entity_response = oauth_api.accounts.get_entity(create_entity_response.id)

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
                    'individual.trading_name',
                    'individual.national_tax_id')

    onboard_entity_request.individual.first_name = 'John'

    update_response = oauth_api.accounts.update_entity(create_entity_response.id, onboard_entity_request)

    assert_response(update_response, 'id')

    assert create_entity_response.id == update_response.id


def test_should_upload_file(oauth_api):
    upload_file(oauth_api)


def test_should_create_and_retrieve_payment_instrument(accounts_checkout_api):
    entity_request = OnboardEntityRequest()
    entity_request.reference = new_uuid()[:14]
    entity_request.contact_details = ContactDetails()
    entity_request.contact_details.phone = phone()
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
    representative.identification = Identification()
    representative.identification.national_id_number = 'AB123456C'
    entity_request.company.representatives = [representative]

    entity_response = accounts_checkout_api.accounts.create_entity(entity_request)

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
