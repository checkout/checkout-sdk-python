from __future__ import absolute_import

import os

from checkout_sdk.files.files import FileRequest
from checkout_sdk.marketplace.marketplace import OnboardEntityRequest, ContactDetails, Profile, Individual, DateOfBirth, \
    Identification
from tests.checkout_test_utils import assert_response, phone, address, new_uuid, get_project_root


def test_should_create_get_and_update_onboard_entity(oauth_api):
    onboard_entity_request = OnboardEntityRequest()
    onboard_entity_request.reference = new_uuid()[:14]
    onboard_entity_request.contact_details = ContactDetails()
    onboard_entity_request.contact_details.phone = phone()
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

    create_entity_response = oauth_api.marketplace.create_entity(onboard_entity_request)

    assert_response(create_entity_response, 'id', 'reference')

    get_entity_response = oauth_api.marketplace.get_entity(create_entity_response['id'])

    assert_response(get_entity_response,
                    'id',
                    'reference',
                    'contact_details',
                    'contact_details.phone',
                    'contact_details.phone.number',
                    'individual',
                    'individual.first_name',
                    'individual.last_name',
                    'individual.trading_name',
                    'individual.national_tax_id')

    onboard_entity_request.individual.first_name = 'John'

    update_response = oauth_api.marketplace.update_entity(create_entity_response['id'], onboard_entity_request)

    assert_response(update_response, 'id')

    assert create_entity_response['id'] == update_response['id']


def test_should_upload_file(oauth_api):
    request = FileRequest()
    request.file = os.path.join(get_project_root(), 'tests', 'resources', 'checkout.jpeg')
    request.purpose = 'identification'
    response = oauth_api.marketplace.upload_file(request)
    assert_response(response, 'id', '_links')
