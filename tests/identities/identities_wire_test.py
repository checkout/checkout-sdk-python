from unittest.mock import MagicMock

import pytest

from checkout_sdk.api_client import ApiClient
from checkout_sdk.identities.addressdocumentverification.addressdocumentverification_client import \
    AddressDocumentVerificationClient
from checkout_sdk.identities.entities import AttemptAssetsQueryFilter, AttemptsQueryFilter
from checkout_sdk.identities.faceauthentication.faceauthentication_client import FaceAuthenticationClient
from checkout_sdk.identities.iddocumentverification.iddocumentverification_client import \
    IdDocumentVerificationClient
from checkout_sdk.identities.identityverification.identityverification_client import \
    IdentityVerificationClient


# Exercises the REAL ApiClient params path (invoke -> _prepare_request_payload -> requests), unlike
# the four client tests which mock ApiClient and can only assert that the filter object was handed
# over. Nothing else in the SDK covers params reaching the wire. Follows the pattern of
# tests/accounts/accounts_schema_version_header_test.py.
@pytest.fixture
def api_and_http(mock_sdk_configuration):
    api_client = ApiClient(configuration=mock_sdk_configuration,
                           base_uri=mock_sdk_configuration.environment.base_uri)
    http_client = MagicMock()
    response = MagicMock()
    response.text = ''
    response.raise_for_status.return_value = None
    http_client.request.return_value = response
    api_client._http_client = http_client

    authorization = MagicMock()
    authorization.get_authorization_header.return_value = 'Bearer test'
    return api_client, http_client, authorization


def _client(cls, api_client, configuration, authorization):
    client = cls(api_client=api_client, configuration=configuration)
    client._sdk_authorization = lambda *args, **kwargs: authorization
    return client


def _sent_params(http_client):
    return http_client.request.call_args.kwargs['params']


def _sent_url(http_client):
    return http_client.request.call_args.kwargs['url']


def _pagination():
    query = AttemptsQueryFilter()
    query.skip = 5
    query.limit = 25
    return query


class TestAttemptsPaginationReachesTheWire:

    def test_address_document_verification_attempts_send_skip_and_limit(
            self, api_and_http, mock_sdk_configuration):
        api_client, http_client, authorization = api_and_http
        client = _client(AddressDocumentVerificationClient, api_client, mock_sdk_configuration,
                         authorization)

        client.get_address_document_verification_attempts('adv_123', _pagination())

        assert _sent_params(http_client) == {'skip': 5, 'limit': 25}
        assert _sent_url(http_client).endswith('address-document-verifications/adv_123/attempts')

    def test_id_document_verification_attempts_send_skip_and_limit(
            self, api_and_http, mock_sdk_configuration):
        api_client, http_client, authorization = api_and_http
        client = _client(IdDocumentVerificationClient, api_client, mock_sdk_configuration, authorization)

        client.get_id_document_verification_attempts('iddv_123', _pagination())

        assert _sent_params(http_client) == {'skip': 5, 'limit': 25}
        assert _sent_url(http_client).endswith('id-document-verifications/iddv_123/attempts')

    def test_identity_verification_attempts_send_skip_and_limit(
            self, api_and_http, mock_sdk_configuration):
        api_client, http_client, authorization = api_and_http
        client = _client(IdentityVerificationClient, api_client, mock_sdk_configuration, authorization)

        client.get_identity_verification_attempts('idv_123', _pagination())

        assert _sent_params(http_client) == {'skip': 5, 'limit': 25}
        assert _sent_url(http_client).endswith('identity-verifications/idv_123/attempts')

    def test_face_authentication_attempts_send_skip_and_limit(
            self, api_and_http, mock_sdk_configuration):
        api_client, http_client, authorization = api_and_http
        client = _client(FaceAuthenticationClient, api_client, mock_sdk_configuration, authorization)

        client.get_face_authentication_attempts('fav_123', _pagination())

        assert _sent_params(http_client) == {'skip': 5, 'limit': 25}
        assert _sent_url(http_client).endswith('face-authentications/fav_123/attempts')

    def test_attempt_assets_send_skip_and_limit(self, api_and_http, mock_sdk_configuration):
        api_client, http_client, authorization = api_and_http
        client = _client(AddressDocumentVerificationClient, api_client, mock_sdk_configuration,
                         authorization)

        query = AttemptAssetsQueryFilter()
        query.skip = 2
        query.limit = 50

        client.get_address_document_verification_attempt_assets('adv_123', 'adva_123', query)

        assert _sent_params(http_client) == {'skip': 2, 'limit': 50}
        assert _sent_url(http_client).endswith(
            'address-document-verifications/adv_123/attempts/adva_123/assets')

    def test_an_explicit_zero_skip_reaches_the_wire(self, api_and_http, mock_sdk_configuration):
        """skip=0 is a meaningful value. The PHP SDK drops it because its filter skips empty
        values; python must not."""
        api_client, http_client, authorization = api_and_http
        client = _client(IdentityVerificationClient, api_client, mock_sdk_configuration, authorization)

        query = AttemptsQueryFilter()
        query.skip = 0
        query.limit = 10

        client.get_identity_verification_attempts('idv_123', query)

        assert _sent_params(http_client) == {'skip': 0, 'limit': 10}

    def test_limit_only_sends_just_the_limit(self, api_and_http, mock_sdk_configuration):
        api_client, http_client, authorization = api_and_http
        client = _client(IdentityVerificationClient, api_client, mock_sdk_configuration, authorization)

        query = AttemptsQueryFilter()
        query.limit = 25

        client.get_identity_verification_attempts('idv_123', query)

        assert _sent_params(http_client) == {'limit': 25}

    def test_an_omitted_filter_sends_no_params(self, api_and_http, mock_sdk_configuration):
        api_client, http_client, authorization = api_and_http
        client = _client(IdentityVerificationClient, api_client, mock_sdk_configuration, authorization)

        client.get_identity_verification_attempts('idv_123')

        assert _sent_params(http_client) is None

    def test_an_empty_filter_sends_an_empty_params_object(self, api_and_http, mock_sdk_configuration):
        api_client, http_client, authorization = api_and_http
        client = _client(IdentityVerificationClient, api_client, mock_sdk_configuration, authorization)

        client.get_identity_verification_attempts('idv_123', AttemptsQueryFilter())

        assert _sent_params(http_client) == {}
