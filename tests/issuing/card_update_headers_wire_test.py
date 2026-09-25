from unittest.mock import MagicMock

import pytest
from requests import HTTPError

from checkout_sdk.api_client import ApiClient
from checkout_sdk.exception import CheckoutApiException
from checkout_sdk.issuing.cards import CardUpdateHeaders, UpdateCardRequest
from checkout_sdk.issuing.issuing_client import IssuingClient


# Exercises the REAL ApiClient header path (_process_custom_headers -> invoke), unlike
# issuing_client_test which mocks ApiClient and can only assert the headers object was handed over.
# The header names are case sensitive and return-encrypted-cvv is lower case, which the default
# snake_case converter would render as Return-Encrypted-Cvv.
def _build(mock_sdk_configuration, status=200, body='{}'):
    api_client = ApiClient(configuration=mock_sdk_configuration,
                           base_uri=mock_sdk_configuration.environment.base_uri)
    http_client = MagicMock()
    response = MagicMock()
    response.status_code = status
    response.text = body
    response.headers = {'Content-Type': 'application/json'}
    response.json.return_value = __import__('json').loads(body)
    if status >= 400:
        response.raise_for_status.side_effect = HTTPError(response=response)
    else:
        response.raise_for_status.return_value = None
    http_client.request.return_value = response
    api_client._http_client = http_client

    authorization = MagicMock()
    authorization.get_authorization_header.return_value = 'Bearer test'

    client = IssuingClient(api_client=api_client, configuration=mock_sdk_configuration)
    client._sdk_authorization = lambda *args, **kwargs: authorization
    return client, http_client


def _sent_headers(http_client):
    return http_client.request.call_args.kwargs['headers']


class TestCardUpdateHeadersReachTheWire:

    def test_both_headers_use_their_exact_swagger_names(self, mock_sdk_configuration):
        client, http_client = _build(mock_sdk_configuration)
        headers = CardUpdateHeaders()
        headers.return_encrypted_cvv = 'true'
        headers.encryption_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A'

        client.update_card('crd_123', UpdateCardRequest(), headers)

        sent = _sent_headers(http_client)
        assert sent['return-encrypted-cvv'] == 'true'
        assert sent['Encryption-Key'] == 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A'
        assert 'Return-Encrypted-Cvv' not in sent

    def test_no_card_headers_are_sent_when_omitted(self, mock_sdk_configuration):
        client, http_client = _build(mock_sdk_configuration)

        client.update_card('crd_123', UpdateCardRequest())

        sent = _sent_headers(http_client)
        assert 'return-encrypted-cvv' not in sent
        assert 'Encryption-Key' not in sent

    def test_the_key_can_be_sent_without_the_flag(self, mock_sdk_configuration):
        client, http_client = _build(mock_sdk_configuration)
        headers = CardUpdateHeaders()
        headers.encryption_key = 'MIIBIjAN'

        client.update_card('crd_123', UpdateCardRequest(), headers)

        sent = _sent_headers(http_client)
        assert sent['Encryption-Key'] == 'MIIBIjAN'
        assert 'return-encrypted-cvv' not in sent

    def test_a_python_bool_would_send_the_capitalised_string(self, mock_sdk_configuration):
        """Documents why return_encrypted_cvv is declared str. ApiClient stringifies header
        values, so a bool reaches the wire as 'True', not the 'true' the spec shows. If a future
        change makes ApiClient render bools lowercase, this test should be replaced by one that
        asserts the bool path directly."""
        client, http_client = _build(mock_sdk_configuration)
        headers = CardUpdateHeaders()
        headers.return_encrypted_cvv = True

        client.update_card('crd_123', UpdateCardRequest(), headers)

        assert _sent_headers(http_client)['return-encrypted-cvv'] == 'True'

    def test_a_422_surfaces_the_encryption_key_required_error(self, mock_sdk_configuration):
        """The API answers 422 with error code encryption_key_required when return-encrypted-cvv
        is true without an Encryption-Key header."""
        client, _ = _build(mock_sdk_configuration, status=422, body='{'
                           '"request_id":"0HLHPN8802NUF:00000003",'
                           '"error_type":"request_invalid",'
                           '"error_codes":["encryption_key_required"]}')
        headers = CardUpdateHeaders()
        headers.return_encrypted_cvv = 'true'

        with pytest.raises(CheckoutApiException) as exc:
            client.update_card('crd_123', UpdateCardRequest(), headers)

        assert exc.value.error_type == 'request_invalid'
        assert 'encryption_key_required' in exc.value.error_details
        assert exc.value.request_id == '0HLHPN8802NUF:00000003'

    def test_a_successful_update_with_the_headers_still_has_no_encrypted_cvv(self, mock_sdk_configuration):
        """The 2026-09-17 spec (INT-1700) removed encrypted_cvv from update-card-response
        entirely, so return-encrypted-cvv/Encryption-Key no longer make the response carry it.
        This test previously asserted the opposite (added by INT-1695, when the field still
        existed)."""
        client, _ = _build(mock_sdk_configuration, body='{"last_modified_date":"2026-06-01T10:00:00Z"}')
        headers = CardUpdateHeaders()
        headers.return_encrypted_cvv = 'true'
        headers.encryption_key = 'MIIBIjAN'

        response = client.update_card('crd_123', UpdateCardRequest(), headers)

        assert response.last_modified_date == '2026-06-01T10:00:00Z'
        assert not hasattr(response, 'encrypted_cvv')

    def test_a_successful_update_without_the_headers_has_no_encrypted_cvv(self, mock_sdk_configuration):
        client, _ = _build(mock_sdk_configuration,
                           body='{"last_modified_date":"2026-06-01T10:00:00Z"}')

        response = client.update_card('crd_123', UpdateCardRequest())

        assert response.last_modified_date == '2026-06-01T10:00:00Z'
        assert not hasattr(response, 'encrypted_cvv')

    def test_update_card_response_round_trips_is_single_use_for_virtual_cards(self, mock_sdk_configuration):
        """The 2026-09-23 spec update split update-card-response into a virtual/physical
        discriminator; the virtual variant adds is_single_use."""
        client, _ = _build(mock_sdk_configuration, body='{'
                           '"type":"virtual",'
                           '"last_modified_date":"2026-06-01T10:00:00Z",'
                           '"is_single_use":true}')

        response = client.update_card('crd_123', UpdateCardRequest())

        assert response.is_single_use is True
