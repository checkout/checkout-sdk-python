import pytest

from tests._assertions import assert_api_call
from checkout_sdk.sessions.sessions import SessionRequest, AppSession, ThreeDsMethodCompletionRequest
from checkout_sdk.sessions.sessions_client import SessionsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return SessionsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestSessionsClient:

    def test_request_session(self, mocker, client: SessionsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = SessionRequest()

        assert client.request_session(body) == 'response'
        assert_api_call(mock, 'sessions', body)

    def test_get_session_details(self, mocker, client: SessionsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_session_details('session_id', 'session_secret') == 'response'
        assert_api_call(mock, 'sessions/session_id')

    def test_update_session(self, mocker, client: SessionsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        body = AppSession()

        assert client.update_session('session_id', body) == 'response'
        assert_api_call(mock, 'sessions/session_id/collect-data', body)

    def test_complete_session(self, mocker, client: SessionsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        client.complete_session('session_id')
        assert_api_call(mock, 'sessions/session_id/complete')

    def test_update_3ds_method_completion(self, mocker, client: SessionsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        body = ThreeDsMethodCompletionRequest()

        client.update_3ds_method_completion('session_id', body, 'session_secret')
        assert_api_call(mock, 'sessions/session_id/issuer-fingerprint', body)
