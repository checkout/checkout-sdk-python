from unittest.mock import MagicMock

import pytest

from checkout_sdk.accounts.accounts import OnboardEntityRequest
from checkout_sdk.accounts.accounts_client import AccountsClient
from checkout_sdk.api_client import ApiClient


# Exercises the REAL ApiClient header path (_process_custom_headers -> invoke), unlike
# accounts_client_test which mocks ApiClient. Asserts the Accept header actually reaching the wire.
@pytest.fixture
def client_and_http(mock_sdk_configuration):
    api_client = ApiClient(configuration=mock_sdk_configuration,
                           base_uri=mock_sdk_configuration.environment.base_uri)
    http_client = MagicMock()
    response = MagicMock()
    response.text = ''
    response.raise_for_status.return_value = None
    http_client.request.return_value = response
    api_client._http_client = http_client

    client = AccountsClient(api_client=api_client,
                            files_client=api_client,
                            configuration=mock_sdk_configuration)
    # the empty mock credentials resolve to no authorization; stub it (irrelevant to the header assertion)
    authorization = MagicMock()
    authorization.get_authorization_header.return_value = 'Bearer test'
    client._sdk_authorization = lambda *args, **kwargs: authorization
    return client, http_client


def _sent_accept(http_client):
    return http_client.request.call_args.kwargs['headers']['Accept']


class TestAccountsSchemaVersionHeader:

    def test_create_entity_sends_default_schema_version(self, client_and_http):
        client, http_client = client_and_http
        client.create_entity(OnboardEntityRequest())
        assert _sent_accept(http_client) == 'application/json;schema_version=3.0'

    def test_get_entity_sends_default_schema_version(self, client_and_http):
        client, http_client = client_and_http
        client.get_entity('entity_id')
        assert _sent_accept(http_client) == 'application/json;schema_version=3.0'

    def test_update_entity_sends_default_schema_version(self, client_and_http):
        client, http_client = client_and_http
        client.update_entity('entity_id', OnboardEntityRequest())
        assert _sent_accept(http_client) == 'application/json;schema_version=3.0'

    def test_get_entity_requirements_sends_default_schema_version(self, client_and_http):
        client, http_client = client_and_http
        client.get_entity_requirements('entity_id')
        assert _sent_accept(http_client) == 'application/json;schema_version=3.0'

    def test_override_schema_version(self, client_and_http):
        client, http_client = client_and_http
        client.get_entity('entity_id', schema_version='2.0')
        assert _sent_accept(http_client) == 'application/json;schema_version=2.0'

    def test_default_accept_untouched_for_other_operations(self, client_and_http):
        client, http_client = client_and_http
        # an operation without schema negotiation must keep the global default Accept
        client.get_sub_entity_members('entity_id')
        assert _sent_accept(http_client) == 'application/json'
