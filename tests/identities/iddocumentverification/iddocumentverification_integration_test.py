import pytest

from checkout_sdk.identities.iddocumentverification.iddocumentverification import (
    IdDocumentVerificationRequest, IdDocumentVerificationAttemptRequest, DeclaredData
)
from checkout_sdk.identities.entities import AttemptAssetsQueryFilter, AttemptsQueryFilter
from tests.checkout_test_utils import assert_response, new_uuid


# tests

@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_create_id_document_verification(default_api):
    response = default_api.id_document_verification.create_id_document_verification(
        id_document_verification_request())
    assert_id_document_verification_response(response)


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_id_document_verification(default_api):
    created = default_api.id_document_verification.create_id_document_verification(
        id_document_verification_request())
    retrieved = default_api.id_document_verification.get_id_document_verification(created.id)
    assert_id_document_verification_response(retrieved)
    assert retrieved.id == created.id


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_anonymize_id_document_verification(default_api):
    created = default_api.id_document_verification.create_id_document_verification(
        id_document_verification_request())
    response = default_api.id_document_verification.anonymize_id_document_verification(created.id)
    assert_response(response, 'http_metadata', 'id')


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_create_id_document_verification_attempt(default_api):
    created = default_api.id_document_verification.create_id_document_verification(
        id_document_verification_request())
    attempt = default_api.id_document_verification.create_id_document_verification_attempt(
        created.id, id_document_verification_attempt_request())
    assert_id_document_verification_attempt_response(attempt)


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_id_document_verification_attempts(default_api):
    created = default_api.id_document_verification.create_id_document_verification(
        id_document_verification_request())
    created_attempt = default_api.id_document_verification.create_id_document_verification_attempt(
        created.id, id_document_verification_attempt_request())
    attempts = default_api.id_document_verification.get_id_document_verification_attempts(created.id)
    assert_response(attempts, 'http_metadata', 'total_count', 'data')
    assert any(a.id == created_attempt.id for a in attempts.data)


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_id_document_verification_attempt(default_api):
    created = default_api.id_document_verification.create_id_document_verification(
        id_document_verification_request())
    created_attempt = default_api.id_document_verification.create_id_document_verification_attempt(
        created.id, id_document_verification_attempt_request())
    retrieved = default_api.id_document_verification.get_id_document_verification_attempt(
        created.id, created_attempt.id)
    assert_id_document_verification_attempt_response(retrieved)
    assert retrieved.id == created_attempt.id


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_id_document_verification_report(default_api):
    created = default_api.id_document_verification.create_id_document_verification(
        id_document_verification_request())
    report = default_api.id_document_verification.get_id_document_verification_report(created.id)
    assert_response(report, 'http_metadata', 'pdf_report')


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_perform_id_document_verification_workflow(default_api):
    created = default_api.id_document_verification.create_id_document_verification(
        id_document_verification_request())
    assert_id_document_verification_response(created)

    retrieved = default_api.id_document_verification.get_id_document_verification(created.id)
    assert_id_document_verification_response(retrieved)
    assert retrieved.id == created.id

    attempt_request = id_document_verification_attempt_request()
    created_attempt = default_api.id_document_verification.create_id_document_verification_attempt(
        created.id, attempt_request)
    assert_id_document_verification_attempt_response(created_attempt)

    attempts = default_api.id_document_verification.get_id_document_verification_attempts(created.id)
    assert_response(attempts, 'http_metadata', 'total_count', 'data')

    retrieved_attempt = default_api.id_document_verification.get_id_document_verification_attempt(
        created.id, created_attempt.id)
    assert_id_document_verification_attempt_response(retrieved_attempt)
    assert retrieved_attempt.id == created_attempt.id

    report = default_api.id_document_verification.get_id_document_verification_report(created.id)
    assert_response(report, 'http_metadata', 'pdf_report')

    anonymized = default_api.id_document_verification.anonymize_id_document_verification(created.id)
    assert_response(anonymized, 'http_metadata', 'id')


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_id_document_verification_attempts_with_pagination(default_api):
    created = default_api.id_document_verification.create_id_document_verification(
        id_document_verification_request())
    default_api.id_document_verification.create_id_document_verification_attempt(
        created.id, id_document_verification_attempt_request())

    query = AttemptsQueryFilter()
    query.skip = 0
    query.limit = 1

    attempts = default_api.id_document_verification.get_id_document_verification_attempts(created.id, query)
    assert_response(attempts, 'http_metadata', 'total_count', 'skip', 'limit', 'data')
    assert attempts.limit == 1
    assert len(attempts.data) <= 1


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_id_document_verification_attempt_assets(default_api):
    created = default_api.id_document_verification.create_id_document_verification(
        id_document_verification_request())
    created_attempt = default_api.id_document_verification.create_id_document_verification_attempt(
        created.id, id_document_verification_attempt_request())

    query = AttemptAssetsQueryFilter()
    query.limit = 10

    assets = default_api.id_document_verification.get_id_document_verification_attempt_assets(
        created.id, created_attempt.id, query)
    assert_response(assets, 'http_metadata', 'total_count', 'skip', 'limit', 'data')
    for asset in assets.data:
        assert asset.type in ('document_front_image', 'document_back_image')
        assert asset._links.asset_url.href is not None


# common methods

def id_document_verification_request() -> IdDocumentVerificationRequest:
    declared_data = DeclaredData()
    declared_data.name = 'John Doe'

    request = IdDocumentVerificationRequest()
    request.applicant_id = new_uuid()
    request.user_journey_id = new_uuid()
    request.declared_data = declared_data
    return request


def id_document_verification_attempt_request() -> IdDocumentVerificationAttemptRequest:
    request = IdDocumentVerificationAttemptRequest()
    request.document_front = 'base64-encoded-front-image-data'
    request.document_back = 'base64-encoded-back-image-data'
    return request


def assert_id_document_verification_response(response):
    assert_response(response, 'http_metadata', 'id', 'applicant_id', 'status')


def assert_id_document_verification_attempt_response(response):
    assert_response(response, 'http_metadata', 'id', 'status')
