import os
import pytest

from checkout_sdk import CheckoutSdk
from checkout_sdk.common.enums import DocumentType
from checkout_sdk.issuing.cardholders import CardholderRequest, CardholderDocument, CardholderType
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
