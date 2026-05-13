from __future__ import absolute_import

from checkout_sdk.issuing.cardholders import CardholderType, CardholderRequest
from tests.checkout_test_utils import assert_response, phone, address


# tests

def test_should_create_cardholder(issuing_checkout_api, cardholder):
    assert_response(cardholder,
                    'id',
                    'type',
                    'status',
                    'reference')

    assert CardholderType.INDIVIDUAL == cardholder.type
    assert 'active' == cardholder.status
    assert 'X-123456-N11' == cardholder.reference


def test_should_get_cardholder(issuing_checkout_api, cardholder):
    cardholder_response = issuing_checkout_api.issuing.get_cardholder(cardholder.id)

    assert_response(cardholder_response,
                    'id',
                    'type',
                    'status',
                    'reference')

    assert CardholderType.INDIVIDUAL == cardholder_response.type
    assert 'Active' == cardholder_response.status
    assert 'X-123456-N11' == cardholder_response.reference


def test_should_update_cardholder(issuing_checkout_api, cardholder):
    request = build_update_cardholder_request()

    response = issuing_checkout_api.issuing.update_cardholder(cardholder.id, request)

    assert_response(response)
    assert response.http_metadata.status_code == 200


def test_should_get_cardholder_cards(issuing_checkout_api, cardholder):
    cardholder_response = issuing_checkout_api.issuing.get_cardholder_cards(cardholder.id)

    assert_response(cardholder_response, 'cards')

    for card in cardholder_response.cards:
        assert cardholder.id == card.cardholder_id


# common methods

def build_update_cardholder_request() -> CardholderRequest:
    request = CardholderRequest()
    request.first_name = 'John'
    request.middle_name = 'Fitzgerald'
    request.last_name = 'Kennedy'
    request.email = 'john.kennedy@myemaildomain.com'
    request.phone_number = phone()
    request.date_of_birth = '1985-05-15'
    request.billing_address = address()
    request.residency_address = address()
    return request
