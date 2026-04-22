import pytest

from checkout_sdk.identities.faceauthentication.faceauthentication import (
    FaceAuthenticationRequest, FaceAuthenticationAttemptRequest, ClientInformation
)
from tests.checkout_test_utils import assert_response, new_uuid


# tests

@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_create_face_authentication(default_api):
    response = default_api.face_authentication.create_face_authentication(face_authentication_request())
    assert_face_authentication_response(response)


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_face_authentication(default_api):
    created = default_api.face_authentication.create_face_authentication(face_authentication_request())
    retrieved = default_api.face_authentication.get_face_authentication(created.id)
    assert_face_authentication_response(retrieved)
    assert retrieved.id == created.id


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_anonymize_face_authentication(default_api):
    created = default_api.face_authentication.create_face_authentication(face_authentication_request())
    response = default_api.face_authentication.anonymize_face_authentication(created.id)
    assert_response(response, 'http_metadata', 'id')


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_create_face_authentication_attempt(default_api):
    created = default_api.face_authentication.create_face_authentication(face_authentication_request())
    attempt = default_api.face_authentication.create_face_authentication_attempt(created.id,
                                                                                 face_authentication_attempt_request())
    assert_face_authentication_attempt_response(attempt)


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_face_authentication_attempts(default_api):
    created = default_api.face_authentication.create_face_authentication(face_authentication_request())
    created_attempt = default_api.face_authentication.create_face_authentication_attempt(
        created.id, face_authentication_attempt_request())
    attempts = default_api.face_authentication.get_face_authentication_attempts(created.id)
    assert_response(attempts, 'http_metadata', 'total_count', 'data')
    assert any(a.id == created_attempt.id for a in attempts.data)


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_get_face_authentication_attempt(default_api):
    created = default_api.face_authentication.create_face_authentication(face_authentication_request())
    created_attempt = default_api.face_authentication.create_face_authentication_attempt(
        created.id, face_authentication_attempt_request())
    retrieved = default_api.face_authentication.get_face_authentication_attempt(created.id, created_attempt.id)
    assert_face_authentication_attempt_response(retrieved)
    assert retrieved.id == created_attempt.id


@pytest.mark.skip(reason='Requires valid test environment setup')
def test_should_perform_face_authentication_workflow(default_api):
    created = default_api.face_authentication.create_face_authentication(face_authentication_request())
    assert_face_authentication_response(created)

    retrieved = default_api.face_authentication.get_face_authentication(created.id)
    assert_face_authentication_response(retrieved)
    assert retrieved.id == created.id

    attempt_request = face_authentication_attempt_request()
    created_attempt = default_api.face_authentication.create_face_authentication_attempt(created.id, attempt_request)
    assert_face_authentication_attempt_response(created_attempt)

    attempts = default_api.face_authentication.get_face_authentication_attempts(created.id)
    assert_response(attempts, 'http_metadata', 'total_count', 'data')

    retrieved_attempt = default_api.face_authentication.get_face_authentication_attempt(created.id, created_attempt.id)
    assert_face_authentication_attempt_response(retrieved_attempt)
    assert retrieved_attempt.id == created_attempt.id

    anonymized = default_api.face_authentication.anonymize_face_authentication(created.id)
    assert_response(anonymized, 'http_metadata', 'id')


# common methods

def face_authentication_request() -> FaceAuthenticationRequest:
    request = FaceAuthenticationRequest()
    request.applicant_id = new_uuid()
    request.user_journey_id = new_uuid()
    return request


def face_authentication_attempt_request() -> FaceAuthenticationAttemptRequest:
    client_information = ClientInformation()
    client_information.pre_selected_residence_country = 'US'
    client_information.pre_selected_language = 'en-US'

    request = FaceAuthenticationAttemptRequest()
    request.redirect_url = 'https://example.com/redirect'
    request.client_information = client_information
    return request


def assert_face_authentication_response(response):
    assert_response(response, 'http_metadata', 'id', 'applicant_id', 'status')


def assert_face_authentication_attempt_response(response):
    assert_response(response, 'http_metadata', 'id', 'status')
