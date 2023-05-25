from __future__ import absolute_import

from checkout_sdk.issuing.cardholders import CardholderType
from tests.checkout_test_utils import assert_response


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


def test_should_get_cardholder_cards(issuing_checkout_api, cardholder):
    cardholder_response = issuing_checkout_api.issuing.get_cardholder_cards(cardholder.id)

    assert_response(cardholder_response, 'cards')

    for card in cardholder_response.cards:
        assert cardholder.id == card.cardholder_id
