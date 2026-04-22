import pytest

from checkout_sdk.identities.identityverification.identityverification import (
    IdentityVerificationRequest, IdentityVerificationAndAttemptRequest,
    IdentityVerificationAttemptRequest, DeclaredData, ClientInformation
)
from tests.checkout_test_utils import assert_response, new_uuid


# tests

@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_create_identity_verification_and_attempt(default_api):
    response = default_api.identity_verification.create_identity_verification_and_attempt(
        identity_verification_and_attempt_request())
    assert_identity_verification_and_attempt_response(response)


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_create_identity_verification(default_api):
    response = default_api.identity_verification.create_identity_verification(
        identity_verification_request())
    assert_identity_verification_response(response)


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_identity_verification(default_api):
    created = default_api.identity_verification.create_identity_verification(
        identity_verification_request())
    retrieved = default_api.identity_verification.get_identity_verification(created.id)
    assert_identity_verification_response(retrieved)
    assert retrieved.id == created.id


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_anonymize_identity_verification(default_api):
    created = default_api.identity_verification.create_identity_verification(
        identity_verification_request())
    response = default_api.identity_verification.anonymize_identity_verification(created.id)
    assert_response(response, 'http_metadata', 'id')


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_create_identity_verification_attempt(default_api):
    created = default_api.identity_verification.create_identity_verification(
        identity_verification_request())
    attempt = default_api.identity_verification.create_identity_verification_attempt(
        created.id, identity_verification_attempt_request())
    assert_identity_verification_attempt_response(attempt)


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_identity_verification_attempts(default_api):
    created = default_api.identity_verification.create_identity_verification(
        identity_verification_request())
    created_attempt = default_api.identity_verification.create_identity_verification_attempt(
        created.id, identity_verification_attempt_request())
    attempts = default_api.identity_verification.get_identity_verification_attempts(created.id)
    assert_response(attempts, 'http_metadata', 'total_count', 'data')
    assert any(a.id == created_attempt.id for a in attempts.data)


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_identity_verification_attempt(default_api):
    created = default_api.identity_verification.create_identity_verification(
        identity_verification_request())
    created_attempt = default_api.identity_verification.create_identity_verification_attempt(
        created.id, identity_verification_attempt_request())
    retrieved = default_api.identity_verification.get_identity_verification_attempt(
        created.id, created_attempt.id)
    assert_identity_verification_attempt_response(retrieved)
    assert retrieved.id == created_attempt.id


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_identity_verification_report(default_api):
    created = default_api.identity_verification.create_identity_verification(
        identity_verification_request())
    report = default_api.identity_verification.get_identity_verification_report(created.id)
    assert_response(report, 'http_metadata', 'signed_url')


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_perform_complete_identity_verification_workflow(default_api):
    created_with_attempt = default_api.identity_verification.create_identity_verification_and_attempt(
        identity_verification_and_attempt_request())
    assert_identity_verification_and_attempt_response(created_with_attempt)

    retrieved = default_api.identity_verification.get_identity_verification(created_with_attempt.id)
    assert_identity_verification_response(retrieved)
    assert retrieved.id == created_with_attempt.id

    attempt = default_api.identity_verification.create_identity_verification_attempt(
        created_with_attempt.id, identity_verification_attempt_request())
    assert_identity_verification_attempt_response(attempt)

    attempts = default_api.identity_verification.get_identity_verification_attempts(created_with_attempt.id)
    assert_response(attempts, 'http_metadata', 'total_count', 'data')
    assert any(a.id == attempt.id for a in attempts.data)

    retrieved_attempt = default_api.identity_verification.get_identity_verification_attempt(
        created_with_attempt.id, attempt.id)
    assert_identity_verification_attempt_response(retrieved_attempt)
    assert retrieved_attempt.id == attempt.id

    report = default_api.identity_verification.get_identity_verification_report(created_with_attempt.id)
    assert_response(report, 'http_metadata', 'signed_url')

    anonymized = default_api.identity_verification.anonymize_identity_verification(created_with_attempt.id)
    assert_response(anonymized, 'http_metadata', 'id')


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_perform_separate_create_and_attempt_workflow(default_api):
    created = default_api.identity_verification.create_identity_verification(
        identity_verification_request())
    assert_identity_verification_response(created)

    retrieved = default_api.identity_verification.get_identity_verification(created.id)
    assert_identity_verification_response(retrieved)
    assert retrieved.id == created.id

    attempt = default_api.identity_verification.create_identity_verification_attempt(
        created.id, identity_verification_attempt_request())
    assert_identity_verification_attempt_response(attempt)

    attempts = default_api.identity_verification.get_identity_verification_attempts(created.id)
    assert_response(attempts, 'http_metadata', 'total_count', 'data')
    assert any(a.id == attempt.id for a in attempts.data)

    retrieved_attempt = default_api.identity_verification.get_identity_verification_attempt(
        created.id, attempt.id)
    assert_identity_verification_attempt_response(retrieved_attempt)
    assert retrieved_attempt.id == attempt.id

    report = default_api.identity_verification.get_identity_verification_report(created.id)
    assert_response(report, 'http_metadata', 'signed_url')

    anonymized = default_api.identity_verification.anonymize_identity_verification(created.id)
    assert_response(anonymized, 'http_metadata', 'id')


# common methods

def identity_verification_and_attempt_request() -> IdentityVerificationAndAttemptRequest:
    declared_data = DeclaredData()
    declared_data.name = 'John Doe'

    request = IdentityVerificationAndAttemptRequest()
    request.applicant_id = new_uuid()
    request.user_journey_id = new_uuid()
    request.redirect_url = 'https://example.com/redirect'
    request.declared_data = declared_data
    return request


def identity_verification_request() -> IdentityVerificationRequest:
    declared_data = DeclaredData()
    declared_data.name = 'John Doe'

    request = IdentityVerificationRequest()
    request.applicant_id = new_uuid()
    request.user_journey_id = new_uuid()
    request.declared_data = declared_data
    return request


def identity_verification_attempt_request() -> IdentityVerificationAttemptRequest:
    client_information = ClientInformation()
    client_information.pre_selected_residence_country = 'US'
    client_information.pre_selected_language = 'en-US'

    request = IdentityVerificationAttemptRequest()
    request.redirect_url = 'https://example.com/redirect'
    request.client_information = client_information
    return request


def assert_identity_verification_and_attempt_response(response):
    assert_response(response, 'http_metadata', 'id', 'applicant_id', 'status', 'redirect_url')


def assert_identity_verification_response(response):
    assert_response(response, 'http_metadata', 'id', 'applicant_id', 'status')


def assert_identity_verification_attempt_response(response):
    assert_response(response, 'http_metadata', 'id', 'status')
