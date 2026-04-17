from __future__ import absolute_import

import pytest
import uuid

from checkout_sdk.forward.forward import ForwardRequest, IdSource, NetworkToken, MethodType, DestinationRequest, \
    Headers, DlocalSignature, DlocalParameters, SecretRequest
from tests.checkout_test_utils import assert_response


@pytest.mark.skip(reason='This test requires a valid id or Token source')
def test_should_forward_and_get_request(default_api):
    id_source = IdSource()
    id_source.id = 'src_v5rgkf3gdtpuzjqesyxmyodnya'

    network_token = NetworkToken()
    network_token.enabled = True
    network_token.request_cryptogram = False

    headers = Headers()
    headers.encrypted = '<JWE encrypted JSON object with string values>'
    headers.raw = {
        'Idempotency-Key': 'xe4fad12367dfgrds',
        'Content-Type': 'application/json',
    }

    dlocal_parameters = DlocalParameters()
    dlocal_parameters.secret_key = '9f439fe1a9f96e67b047d3c1a28c33a2e'

    signature = DlocalSignature()
    signature.dlocal_parameters = dlocal_parameters

    destination_request = DestinationRequest()
    destination_request.url = 'https://example.com/forward'
    destination_request.method = MethodType.POST
    destination_request.headers = headers
    destination_request.body = ('{"amount": 1000, "currency": "USD", "reference": "some_reference", "source": '
                                '{"type": "card", "number": "{{card_number}}", "expiry_month": "{{card_expiry_month}}",'
                                ' "expiry_year": "{{card_expiry_year_yyyy}}", "name": "Ali Farid"}, '
                                '"payment_type": "Regular", "authorization_type": "Final", "capture": true, '
                                '"processing_channel_id": "pc_xxxxxxxxxxx", "risk": {"enabled": false}, '
                                '"merchant_initiated": true}')
    destination_request.signature = signature

    forward_request = ForwardRequest()
    forward_request.source = id_source
    forward_request.reference = 'ORD-5023-4E89'
    forward_request.processing_channel_id = 'pc_azsiyswl7bwe2ynjzujy7lcjca'
    forward_request.network_token = network_token
    forward_request.destination_request = destination_request

    response = default_api.forward.forward_request(forward_request)
    assert_response(response, 'request_id', 'destination_response')

    get_response = default_api.forward.get_forward_request(response['request_id'])
    assert_response(get_response, 'request_id', 'destination_request', 'destination_response')


def build_create_secret_request(name: str = None, value: str = "secret_value", entity_id: str = None) -> SecretRequest:
    request = SecretRequest()
    request.name = name or f"secret_{str(uuid.uuid4()).replace('-', '')[:16]}"
    request.value = value
    request.entity_id = entity_id
    return request


def build_update_secret_request(value: str = "updated_value", entity_id: str = None) -> SecretRequest:
    request = SecretRequest()
    request.value = value
    request.entity_id = entity_id
    return request


def assert_secret_response(response, expected_name: str = None):
    assert_response(response, 'name', 'created_at', 'updated_at', 'version')
    if expected_name:
        assert response['name'] == expected_name


@pytest.mark.skip(reason='This test requires forward secrets scopes and valid credentials')
def test_should_create_list_update_delete_secret(default_api):
    # Create secret
    create_request = build_create_secret_request(value="initial_value")
    secret_name = create_request.name
    
    create_response = default_api.forward.create_secret(create_request)
    assert_secret_response(create_response, secret_name)
    
    # List secrets - should contain our secret
    list_response = default_api.forward.list_secrets()
    assert_response(list_response, 'data')
    assert any(secret['name'] == secret_name for secret in list_response['data'])
    
    # Update secret
    update_request = build_update_secret_request(value="new_updated_value")
    update_response = default_api.forward.update_secret(secret_name, update_request)
    assert_secret_response(update_response, secret_name)
    
    # Delete secret
    delete_response = default_api.forward.delete_secret(secret_name)
    # Delete should return empty response (204 No Content)
    assert delete_response is not None


@pytest.mark.skip(reason='This test requires forward secrets scopes and valid credentials')
def test_should_create_secret_with_entity_id(default_api):
    create_request = build_create_secret_request(entity_id="ent_test123")
    
    create_response = default_api.forward.create_secret(create_request)
    assert_secret_response(create_response, create_request.name)
    
    # Cleanup
    default_api.forward.delete_secret(create_request.name)
