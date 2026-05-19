import pytest

from tests._assertions import assert_api_call
from checkout_sdk.identities.faceauthentication.faceauthentication import (
    FaceAuthenticationRequest, FaceAuthenticationAttemptRequest
)
from checkout_sdk.identities.faceauthentication.faceauthentication_client import FaceAuthenticationClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return FaceAuthenticationClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


_FAV_ID = 'fav_mtta050yudd54y5iqb5ijh8jtvz'
_ATTEMPT_ID = 'fatp_nk1wbmmczqumwt95k3v39mhbh2w'


class TestFaceAuthenticationClient:

    def test_should_create_face_authentication(self, mocker, client: FaceAuthenticationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = FaceAuthenticationRequest()

        assert client.create_face_authentication(body) == 'response'
        assert_api_call(mock, 'face-authentications', body)

    def test_should_get_face_authentication(self, mocker, client: FaceAuthenticationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_face_authentication(_FAV_ID) == 'response'
        assert_api_call(mock, f'face-authentications/{_FAV_ID}')

    def test_should_anonymize_face_authentication(self, mocker, client: FaceAuthenticationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.anonymize_face_authentication(_FAV_ID) == 'response'
        assert_api_call(mock, f'face-authentications/{_FAV_ID}/anonymize')

    def test_should_create_face_authentication_attempt(self, mocker, client: FaceAuthenticationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = FaceAuthenticationAttemptRequest()

        assert client.create_face_authentication_attempt(_FAV_ID, body) == 'response'
        assert_api_call(mock, f'face-authentications/{_FAV_ID}/attempts', body)

    def test_should_get_face_authentication_attempts(self, mocker, client: FaceAuthenticationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_face_authentication_attempts(_FAV_ID) == 'response'
        assert_api_call(mock, f'face-authentications/{_FAV_ID}/attempts')

    def test_should_get_face_authentication_attempt(self, mocker, client: FaceAuthenticationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_face_authentication_attempt(_FAV_ID, _ATTEMPT_ID) == 'response'
        assert_api_call(mock, f'face-authentications/{_FAV_ID}/attempts/{_ATTEMPT_ID}')
