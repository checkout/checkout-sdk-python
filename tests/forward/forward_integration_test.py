from __future__ import absolute_import

import pytest

from checkout_sdk.forward.forward import ForwardRequest, IdSource, NetworkToken, MethodType, DestinationRequest, \
    Headers, DlocalSignature, DlocalParameters
from tests.checkout_test_utils import assert_response


@pytest.mark.skip(reason='This test requires a valid id or Token source')
def test_should_forward_and_get_request(default_api):
    id_source = IdSource
    id_source.id = 'src_v5rgkf3gdtpuzjqesyxmyodnya'

    network_token = NetworkToken
    network_token.enabled = True
    network_token.request_cryptogram = False

    headers = Headers
    headers.encrypted = '<JWE encrypted JSON object with string values>'
    headers.raw = {
        'Idempotency-Key': 'xe4fad12367dfgrds',
        'Content-Type': 'application/json',
    }

    dlocal_parameters = DlocalParameters
    dlocal_parameters.secret_key = '9f439fe1a9f96e67b047d3c1a28c33a2e'

    signature = DlocalSignature
    signature.dlocal_parameters = dlocal_parameters

    destination_request = DestinationRequest
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

    forward_request = ForwardRequest
    forward_request.source = id_source
    forward_request.reference = 'ORD-5023-4E89'
    forward_request.processing_channel_id = 'pc_azsiyswl7bwe2ynjzujy7lcjca'
    forward_request.network_token = network_token
    forward_request.destination_request = destination_request

    response = default_api.forward.forward_request(forward_request)
    assert_response(response, 'request_id', 'destination_response')

    get_response = default_api.forward.get_forward_request(response['request_id'])
    assert_response(get_response, 'request_id', 'destination_request', 'destination_response')
