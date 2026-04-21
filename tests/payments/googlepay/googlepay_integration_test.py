from __future__ import absolute_import

import pytest

from checkout_sdk.payments.googlepay.googlepay import GooglePayEnrollmentRequest, GooglePayRegisterDomainRequest
from tests.checkout_test_utils import assert_response


# tests

@pytest.mark.skip(reason='Requires a valid entity with Google Pay enrollment permissions')
def test_should_create_enrollment(default_api):
    request = create_enrollment_request()
    response = default_api.google_pay.create_enrollment(request)
    assert_enrollment_response(response)


@pytest.mark.skip(reason='Requires an actively enrolled Google Pay entity')
def test_should_register_domain(default_api):
    request = create_register_domain_request()
    response = default_api.google_pay.register_domain('ent_uzm3uxtssvmuxnyrfdffcyjxeu', request)
    assert response is not None


@pytest.mark.skip(reason='Requires an actively enrolled Google Pay entity')
def test_should_get_registered_domains(default_api):
    response = default_api.google_pay.get_registered_domains('ent_uzm3uxtssvmuxnyrfdffcyjxeu')
    assert_registered_domains_response(response)


@pytest.mark.skip(reason='Requires an actively enrolled Google Pay entity')
def test_should_get_enrollment_state(default_api):
    response = default_api.google_pay.get_enrollment_state('ent_uzm3uxtssvmuxnyrfdffcyjxeu')
    assert_enrollment_state_response(response)


# common methods

def create_enrollment_request() -> GooglePayEnrollmentRequest:
    request = GooglePayEnrollmentRequest()
    request.entity_id = 'ent_uzm3uxtssvmuxnyrfdffcyjxeu'
    request.email_address = 'test@example.com'
    request.accept_terms_of_service = True
    return request


def create_register_domain_request() -> GooglePayRegisterDomainRequest:
    request = GooglePayRegisterDomainRequest()
    request.web_domain = 'checkout-test-domain.com'
    return request


def assert_enrollment_response(response):
    assert_response(response, 'http_metadata', 'tos_accepted_time', 'state')


def assert_registered_domains_response(response):
    assert_response(response, 'http_metadata', 'domains')


def assert_enrollment_state_response(response):
    assert_response(response, 'http_metadata', 'state')
