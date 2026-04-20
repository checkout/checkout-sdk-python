import pytest

from checkout_sdk.exception import CheckoutApiException
from checkout_sdk.identities.applicants.applicants import CreateApplicantRequest, UpdateApplicantRequest
from tests.checkout_test_utils import assert_response, random_email


# tests

@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_create_applicant(default_api):
    response = default_api.applicants.create_applicant(create_applicant_request())
    assert_applicant_response(response)


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_applicant(default_api):
    created = default_api.applicants.create_applicant(create_applicant_request())
    retrieved = default_api.applicants.get_applicant(created.id)
    assert_applicant_response(retrieved)
    assert retrieved.id == created.id
    assert retrieved.email == created.email


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_update_applicant(default_api):
    created = default_api.applicants.create_applicant(create_applicant_request())
    request = update_applicant_request()
    updated = default_api.applicants.update_applicant(created.id, request)
    assert_applicant_response(updated)
    assert updated.id == created.id
    assert updated.email == request.email
    assert updated.external_applicant_name == request.external_applicant_name


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_anonymize_applicant(default_api):
    created = default_api.applicants.create_applicant(create_applicant_request())
    response = default_api.applicants.anonymize_applicant(created.id)
    assert_response(response, 'http_metadata', 'id')
    assert response.id == created.id
    with pytest.raises(CheckoutApiException):
        default_api.applicants.get_applicant(created.id)


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_create_update_and_retrieve_applicant_workflow(default_api):
    created = default_api.applicants.create_applicant(create_applicant_request())
    assert_applicant_response(created)

    request = update_applicant_request()
    updated = default_api.applicants.update_applicant(created.id, request)
    assert_applicant_response(updated)
    assert updated.id == created.id

    retrieved = default_api.applicants.get_applicant(created.id)
    assert_applicant_response(retrieved)
    assert retrieved.id == created.id
    assert retrieved.email == request.email
    assert retrieved.external_applicant_name == request.external_applicant_name


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_validate_optional_fields(default_api):
    request = CreateApplicantRequest()
    request.email = random_email()
    response = default_api.applicants.create_applicant(request)
    assert_applicant_response(response)
    assert response.email == request.email


# common methods

def create_applicant_request() -> CreateApplicantRequest:
    request = CreateApplicantRequest()
    request.external_applicant_id = 'ext_test_applicant'
    request.email = random_email()
    request.external_applicant_name = 'Test Applicant Name'
    return request


def update_applicant_request() -> UpdateApplicantRequest:
    request = UpdateApplicantRequest()
    request.email = random_email()
    request.external_applicant_name = 'Updated Test Applicant Name'
    return request


def assert_applicant_response(response):
    assert_response(response, 'http_metadata', 'id', 'email')
