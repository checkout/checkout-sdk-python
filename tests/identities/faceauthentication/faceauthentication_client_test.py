import pytest

from checkout_sdk.identities.faceauthentication.faceauthentication import (
    FaceAuthenticationRequest, FaceAuthenticationAttemptRequest
)
from checkout_sdk.identities.faceauthentication.faceauthentication_client import FaceAuthenticationClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return FaceAuthenticationClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


# tests

class TestFaceAuthenticationClient:

    def test_should_create_face_authentication(self, mocker, client: FaceAuthenticationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_face_authentication(FaceAuthenticationRequest()) == 'response'

    def test_should_get_face_authentication(self, mocker, client: FaceAuthenticationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_face_authentication('fav_mtta050yudd54y5iqb5ijh8jtvz') == 'response'

    def test_should_anonymize_face_authentication(self, mocker, client: FaceAuthenticationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.anonymize_face_authentication('fav_mtta050yudd54y5iqb5ijh8jtvz') == 'response'

    def test_should_create_face_authentication_attempt(self, mocker, client: FaceAuthenticationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_face_authentication_attempt('fav_mtta050yudd54y5iqb5ijh8jtvz',
                                                         FaceAuthenticationAttemptRequest()) == 'response'

    def test_should_get_face_authentication_attempts(self, mocker, client: FaceAuthenticationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_face_authentication_attempts('fav_mtta050yudd54y5iqb5ijh8jtvz') == 'response'

    def test_should_get_face_authentication_attempt(self, mocker, client: FaceAuthenticationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_face_authentication_attempt('fav_mtta050yudd54y5iqb5ijh8jtvz',
                                                      'fatp_nk1wbmmczqumwt95k3v39mhbh2w') == 'response'
