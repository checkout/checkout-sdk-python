from __future__ import absolute_import

import os

from checkout_sdk.common.enums import Currency
from checkout_sdk.files.files import FileRequest
from checkout_sdk.marketplace.marketplace import OnboardEntityRequest, ContactDetails, Profile, Individual, \
    DateOfBirth, Identification, CreateTransferRequest, TransferType, TransferSource, TransferDestination, BalancesQuery
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

    get_entity_response = oauth_api.marketplace.get_entity(create_entity_response.id)

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

    update_response = oauth_api.marketplace.update_entity(create_entity_response.id, onboard_entity_request)

    assert_response(update_response, 'id')

    assert create_entity_response.id == update_response.id


def test_should_upload_file(oauth_api):
    request = FileRequest()
    request.file = os.path.join(get_project_root(), 'tests', 'resources', 'checkout.jpeg')
    request.purpose = 'identification'
    response = oauth_api.marketplace.upload_file(request)
    assert_response(response, 'id', '_links')


def test_should_initiate_transfer_of_funds(oauth_api):
    transfer_source = TransferSource()
    transfer_source.id = 'ent_kidtcgc3ge5unf4a5i6enhnr5m'
    transfer_source.amount = 100

    transfer_destination = TransferDestination()
    transfer_destination.id = 'ent_w4jelhppmfiufdnatam37wrfc4'

    transfer_request = CreateTransferRequest()
    transfer_request.transfer_type = TransferType.COMMISSION
    transfer_request.source = transfer_source
    transfer_request.destination = transfer_destination

    response = oauth_api.marketplace.initiate_transfer_of_funds(transfer_request)
    assert_response(response, 'id', 'status')
    assert 'pending' == response.status


def test_should_retrieve_entity_balances(oauth_api):
    query = BalancesQuery()
    query.query = "currency:" + Currency.GBP.value

    response = oauth_api.marketplace.retrieve_entity_balances('ent_kidtcgc3ge5unf4a5i6enhnr5m', query)
    assert_response(response, 'data')
    assert response.data.__len__() > 0
    for balance in response.data:
        assert_response(balance, 'descriptor',
                        'holding_currency',
                        'balances')
