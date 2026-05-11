from __future__ import absolute_import

import pytest

from checkout_sdk.networktokens.network_tokens import ProvisionNetworkTokenRequest, RequestCryptogramRequest, \
    DeleteNetworkTokenRequest, NetworkTokenRequestIdSource, NetworkTokenTransactionType, NetworkTokenInitiatedBy, \
    NetworkTokenDeleteReason
from tests.checkout_test_utils import assert_response

PLACEHOLDER_NETWORK_TOKEN_ID = 'nt_xgu3isllqfyu7ktpk5z2yxbwna'
PLACEHOLDER_INSTRUMENT_ID = 'src_wmlfc3zyhqzehihu7giusaaawu'


# tests
@pytest.mark.skip(reason='use network token endpoints on demand, requires preexisting instrument and network token ids')
def test_should_provision_network_token(oauth_api):
    request = build_provision_network_token_request()

    response = oauth_api.network_tokens.provision_network_token(request)
    assert_network_token_response(response)


@pytest.mark.skip(reason='use network token endpoints on demand, requires preexisting instrument and network token ids')
def test_should_get_network_token(oauth_api):
    response = oauth_api.network_tokens.get_network_token(PLACEHOLDER_NETWORK_TOKEN_ID)
    assert_network_token_response(response)


@pytest.mark.skip(reason='use network token endpoints on demand, requires preexisting instrument and network token ids')
def test_should_request_cryptogram(oauth_api):
    request = build_request_cryptogram_request()

    response = oauth_api.network_tokens.request_cryptogram(PLACEHOLDER_NETWORK_TOKEN_ID, request)
    assert_response(response, 'http_metadata', 'cryptogram')


@pytest.mark.skip(reason='use network token endpoints on demand, requires preexisting instrument and network token ids')
def test_should_delete_network_token(oauth_api):
    request = build_delete_network_token_request()

    response = oauth_api.network_tokens.delete_network_token(PLACEHOLDER_NETWORK_TOKEN_ID, request)
    assert_response(response, 'http_metadata')


# common methods

def build_provision_network_token_request() -> ProvisionNetworkTokenRequest:
    id_source = NetworkTokenRequestIdSource()
    id_source.id = PLACEHOLDER_INSTRUMENT_ID

    request = ProvisionNetworkTokenRequest()
    request.source = id_source
    return request


def build_request_cryptogram_request() -> RequestCryptogramRequest:
    request = RequestCryptogramRequest()
    request.transaction_type = NetworkTokenTransactionType.ECOM
    return request


def build_delete_network_token_request() -> DeleteNetworkTokenRequest:
    request = DeleteNetworkTokenRequest()
    request.initiated_by = NetworkTokenInitiatedBy.TOKEN_REQUESTOR
    request.reason = NetworkTokenDeleteReason.OTHER
    return request


def assert_network_token_response(response):
    assert_response(response,
                    'http_metadata',
                    'card',
                    'network_token')
