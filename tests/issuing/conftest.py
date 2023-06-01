import os
import pytest

from checkout_sdk import CheckoutSdk
from checkout_sdk.common.enums import DocumentType
from checkout_sdk.issuing.cardholders import CardholderRequest, CardholderDocument, CardholderType
from checkout_sdk.issuing.cards import CardLifetime, LifetimeUnit, VirtualCardRequest
from checkout_sdk.oauth_scopes import OAuthScopes
from tests.checkout_test_utils import phone, address, assert_response


@pytest.fixture(scope='module', autouse=True)
def issuing_checkout_api():
    api = CheckoutSdk \
        .builder() \
        .oauth() \
        .client_credentials(client_id=os.environ.get('CHECKOUT_DEFAULT_OAUTH_ISSUING_CLIENT_ID'),
                            client_secret=os.environ.get('CHECKOUT_DEFAULT_OAUTH_ISSUING_CLIENT_SECRET')) \
        .scopes({OAuthScopes.ISSUING_CLIENT, OAuthScopes.ISSUING_CARD_MGMT,
                 OAuthScopes.ISSUING_CONTROLS_READ, OAuthScopes.ISSUING_CONTROLS_WRITE}) \
        .build()
    return api


@pytest.fixture(scope='module')
def cardholder(issuing_checkout_api):
    document = CardholderDocument()
    document.type = DocumentType.NATIONAL_IDENTITY_CARD
    document.front_document_id = 'file_6lbss42ezvoufcb2beo76rvwly'
    document.back_document_id = 'file_aaz5pemp6326zbuvevp6qroqu4'

    request = CardholderRequest()
    request.type = CardholderType.INDIVIDUAL
    request.reference = 'X-123456-N11'
    request.entity_id = 'ent_mujh2nia2ypezmw5fo2fofk7ka'
    request.first_name = 'John'
    request.middle_name = 'Fitzgerald'
    request.last_name = 'Kennedy'
    request.email = 'john.kennedy@myemaildomain.com'
    request.phone_number = phone()
    request.date_of_birth = '1985-05-15'
    request.billing_address = address()
    request.residency_address = address()
    request.document = document

    cardholder = issuing_checkout_api.issuing.create_cardholder(request)

    assert_response(cardholder, 'id')

    return cardholder


@pytest.fixture(scope='class')
def card(issuing_checkout_api, cardholder):
    request = get_card_request(cardholder)
    request.activate_card = False

    card = issuing_checkout_api.issuing.create_card(request)

    assert_response(card, 'id')
    return card


@pytest.fixture()
def active_card(issuing_checkout_api, cardholder):
    request = get_card_request(cardholder)
    request.activate_card = True

    card = issuing_checkout_api.issuing.create_card(request)

    assert_response(card, 'id')
    return card


def get_card_request(cardholder):
    lifetime = CardLifetime()
    lifetime.unit = LifetimeUnit.MONTHS
    lifetime.value = 6

    request = VirtualCardRequest()
    request.cardholder_id = cardholder.id
    request.card_product_id = 'pro_3fn6pv2ikshurn36dbd3iysyha'
    request.lifetime = lifetime
    request.reference = 'X-123456-N11'
    request.display_name = 'John Kennedy'
    request.is_single_use = False

    return request
