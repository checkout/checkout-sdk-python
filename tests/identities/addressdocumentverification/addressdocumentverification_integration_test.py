import pytest

from checkout_sdk.identities.addressdocumentverification.addressdocumentverification import (
    AddressDocumentVerificationRequest, AddressDocumentVerificationAttemptRequest, DeclaredData
)
from checkout_sdk.identities.entities import AttemptAssetsQueryFilter, AttemptsQueryFilter
from tests.checkout_test_utils import assert_response, new_uuid


# tests

@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_create_address_document_verification(default_api):
    response = default_api.address_document_verification.create_address_document_verification(
        address_document_verification_request())
    assert_address_document_verification_response(response)


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_address_document_verification(default_api):
    created = default_api.address_document_verification.create_address_document_verification(
        address_document_verification_request())
    retrieved = default_api.address_document_verification.get_address_document_verification(created.id)
    assert_address_document_verification_response(retrieved)
    assert retrieved.id == created.id


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_address_document_verification_attempts(default_api):
    created = default_api.address_document_verification.create_address_document_verification(
        address_document_verification_request())
    created_attempt = default_api.address_document_verification.create_address_document_verification_attempt(
        created.id, address_document_verification_attempt_request())

    attempts = default_api.address_document_verification.get_address_document_verification_attempts(created.id)
    assert_response(attempts, 'http_metadata', 'total_count', 'skip', 'limit', 'data')
    assert any(a.id == created_attempt.id for a in attempts.data)


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_address_document_verification_attempts_with_pagination(default_api):
    created = default_api.address_document_verification.create_address_document_verification(
        address_document_verification_request())
    default_api.address_document_verification.create_address_document_verification_attempt(
        created.id, address_document_verification_attempt_request())

    query = AttemptsQueryFilter()
    query.skip = 0
    query.limit = 1

    attempts = default_api.address_document_verification.get_address_document_verification_attempts(
        created.id, query)
    assert_response(attempts, 'http_metadata', 'total_count', 'skip', 'limit', 'data')
    assert attempts.limit == 1
    assert len(attempts.data) <= 1


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_address_document_verification_attempt_assets(default_api):
    created = default_api.address_document_verification.create_address_document_verification(
        address_document_verification_request())
    created_attempt = default_api.address_document_verification.create_address_document_verification_attempt(
        created.id, address_document_verification_attempt_request())

    query = AttemptAssetsQueryFilter()
    query.limit = 10

    assets = default_api.address_document_verification.get_address_document_verification_attempt_assets(
        created.id, created_attempt.id, query)
    assert_response(assets, 'http_metadata', 'total_count', 'skip', 'limit', 'data')
    for asset in assets.data:
        assert asset.type == 'document'
        assert asset._links.asset_url.href is not None


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_address_document_verification_report(default_api):
    created = default_api.address_document_verification.create_address_document_verification(
        address_document_verification_request())
    report = default_api.address_document_verification.get_address_document_verification_report(created.id)
    assert_response(report, 'http_metadata', 'pdf_report')


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_anonymize_address_document_verification(default_api):
    created = default_api.address_document_verification.create_address_document_verification(
        address_document_verification_request())
    response = default_api.address_document_verification.anonymize_address_document_verification(created.id)
    assert_response(response, 'http_metadata', 'id')


# common methods

def address_document_verification_request() -> AddressDocumentVerificationRequest:
    declared_data = DeclaredData()
    declared_data.name = 'Hannah Bret'
    declared_data.birth_date = '1994-10-15'

    request = AddressDocumentVerificationRequest()
    request.applicant_id = new_uuid()
    request.user_journey_id = new_uuid()
    request.declared_data = declared_data
    return request


def address_document_verification_attempt_request() -> AddressDocumentVerificationAttemptRequest:
    request = AddressDocumentVerificationAttemptRequest()
    request.document = 'base64-encoded-document-image-data'
    return request


def assert_address_document_verification_response(response):
    assert_response(response, 'http_metadata', 'id', 'applicant_id', 'status')
