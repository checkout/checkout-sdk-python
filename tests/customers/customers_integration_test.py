from __future__ import absolute_import

import pytest

from checkout_sdk.customers.customers import CustomerRequest
from checkout_sdk.exception import CheckoutApiException
from tests.checkout_test_utils import assert_response, random_email, phone


def test_should_create_and_get_customer(default_api):
    email = random_email()
    customer_id = create_customer(default_api, email)
    response = default_api.customers.get(customer_id)
    assert_response(response,
                    'email',
                    'name',
                    'phone')
    assert email == response['email']


def test_should_create_and_update_customer(default_api):
    customer_id = create_customer(default_api, random_email())

    customer_request = CustomerRequest()
    customer_request.name = 'Another name'
    customer_request.email = random_email()

    default_api.customers.update(customer_id, customer_request)

    response_update = default_api.customers.get(customer_id)
    assert_response(response_update,
                    'email',
                    'name',
                    'phone')

    assert customer_request.name == response_update['name']


def test_should_create_and_delete_customer(default_api):
    customer_id = create_customer(default_api, random_email())
    default_api.customers.delete(customer_id)

    try:
        default_api.customers.get(customer_id)
        pytest.fail()
    except CheckoutApiException as err:
        assert err.args[0] == "The API response status code (404) does not indicate success."


def create_customer(default_api, email):
    customer_request = CustomerRequest()
    customer_request.email = email
    customer_request.name = 'Customer'
    customer_request.phone = phone()

    customer_response = default_api.customers.create(customer_request)
    assert_response(customer_response, 'id')
    return customer_response['id']
