import pytest

from checkout_sdk.sessions.sessions import SessionRequest, AppSession, ThreeDsMethodCompletionRequest
from checkout_sdk.sessions.sessions_client import SessionsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return SessionsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestSessionsClient:

    def test_request_session(self, mocker, client: SessionsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.request_session(SessionRequest()) == 'response'

    def test_get_session_details(self, mocker, client: SessionsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_session_details('session_id', 'session_secret') == 'response'

    def test_update_session(self, mocker, client: SessionsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        assert client.update_session('session_id', AppSession()) == 'response'

    def test_complete_session(self, mocker, client: SessionsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post')
        client.complete_session('session_id')

    def test_update_3ds_method_completion(self, mocker, client: SessionsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.put')
        client.update_3ds_method_completion('session_id', ThreeDsMethodCompletionRequest(), 'session_secret')
