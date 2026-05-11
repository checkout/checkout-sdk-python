from __future__ import absolute_import

import os

import pytest

from checkout_sdk.exception import CheckoutApiException
from tests.checkout_test_utils import assert_response

INVALID_PROCESSING_CHANNEL_ID = 'pc_test_invalid_channel_id'


# tests

def test_should_get_available_payment_methods(oauth_api):
    response = oauth_api.payment_methods.get_available_payment_methods(
        os.environ.get('CHECKOUT_PROCESSING_CHANNEL_ID'))
    assert_get_available_payment_methods_response(response)


def test_should_get_available_payment_methods_with_specific_processing_channel(oauth_api):
    response = oauth_api.payment_methods.get_available_payment_methods(
        os.environ.get('CHECKOUT_PROCESSING_CHANNEL_ID'))
    assert_get_available_payment_methods_response(response)
    assert_methods_have_valid_structure(response)


def test_should_throw_with_invalid_processing_channel_id(oauth_api):
    with pytest.raises(CheckoutApiException) as exc_info:
        oauth_api.payment_methods.get_available_payment_methods(INVALID_PROCESSING_CHANNEL_ID)
    assert 'processing_channel_id_invalid' in exc_info.value.error_details


# common methods

def assert_get_available_payment_methods_response(response):
    assert_response(response,
                    'http_metadata',
                    'methods')
    assert len(response.methods) > 0


def assert_methods_have_valid_structure(response):
    for method in response.methods:
        assert hasattr(method, 'type')
        assert method.type is not None
