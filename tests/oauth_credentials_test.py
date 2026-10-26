import json

import pytest
from requests import Response, Session
from requests.adapters import HTTPAdapter

from checkout_sdk.environment import Environment
from checkout_sdk.oauth_credentials import OAuthSdkCredentials


def token_response(request):
    response = Response()
    response.status_code = 200
    response.request = request
    response.url = request.url
    response._content = json.dumps(
        {'access_token': 'access_token', 'token_type': 'Bearer', 'expires_in': 3600}).encode('utf-8')
    return response


class TestOAuthSdkCredentials:
    """The token request carries the client id and secret, so it must never go out with TLS
    certificate verification turned off. The SDK leaves verification to the http_client the
    caller passed in, and to requests' defaults, instead of overriding it per request.

    Only the transport is stubbed: a real Session merges its settings into the request, so the
    test sees the same verify value the TLS handshake would.
    """

    @pytest.fixture(autouse=True)
    def no_ca_bundle_from_environment(self, monkeypatch):
        # requests reads these when verification is on, which would make the asserted value
        # depend on the machine running the tests.
        monkeypatch.delenv('REQUESTS_CA_BUNDLE', raising=False)
        monkeypatch.delenv('CURL_CA_BUNDLE', raising=False)

    @staticmethod
    def request_token(mocker, http_client: Session):
        send = mocker.patch.object(HTTPAdapter, 'send', autospec=True,
                                   side_effect=lambda adapter, request, **kwargs: token_response(request))
        credentials = OAuthSdkCredentials(http_client, Environment.sandbox(), 'client_id', 'client_secret',
                                          None, ['vault'])
        assert credentials.get_access_token().token == 'access_token'
        return send

    def test_should_verify_the_server_certificate_when_requesting_the_token(self, mocker):
        send = self.request_token(mocker, Session())

        assert send.call_count == 1
        assert send.call_args.kwargs['verify'] is True

    def test_should_use_the_ca_bundle_configured_on_the_http_client(self, mocker):
        http_client = Session()
        http_client.verify = '/path/to/ca-bundle.pem'

        send = self.request_token(mocker, http_client)

        assert send.call_args.kwargs['verify'] == '/path/to/ca-bundle.pem'
