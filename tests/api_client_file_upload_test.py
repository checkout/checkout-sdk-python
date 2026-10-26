from unittest.mock import MagicMock

import pytest
from requests import ConnectionError, HTTPError

from checkout_sdk.api_client import ApiClient
from checkout_sdk.exception import CheckoutApiException, CheckoutException
from checkout_sdk.files.files import FileRequest


# Exercises the REAL ApiClient upload path (invoke -> get_file_request -> http_client.request).
# get_file_request opens the file and hands the open handle to requests, which reads it but never
# closes it, so invoke has to close it whatever the outcome of the request.
def _build(mock_sdk_configuration, request_side_effect=None, status=200):
    api_client = ApiClient(configuration=mock_sdk_configuration,
                           base_uri=mock_sdk_configuration.environment.base_uri)
    response = MagicMock()
    response.status_code = status
    response.text = '{"id": "file_123"}'
    response.headers = {'Content-Type': 'application/json'}
    response.json.return_value = {'id': 'file_123'}
    if status >= 400:
        response.raise_for_status.side_effect = HTTPError(response=response)
    http_client = MagicMock()
    http_client.request.return_value = response
    http_client.request.side_effect = request_side_effect
    api_client._http_client = http_client

    authorization = MagicMock()
    authorization.get_authorization_header.return_value = 'Bearer test'
    return api_client, http_client, authorization


def _file_request(tmp_path):
    path = tmp_path / 'evidence.pdf'
    path.write_bytes(b'%PDF-1.4')
    file_request = FileRequest()
    file_request.file = str(path)
    file_request.purpose = 'dispute_evidence'
    return file_request


def _sent_file(http_client):
    files = http_client.request.call_args.kwargs['files']
    return files['file'][1]


class TestApiClientFileUpload:

    def test_should_close_the_uploaded_file_after_a_successful_request(self, mock_sdk_configuration, tmp_path):
        api_client, http_client, authorization = _build(mock_sdk_configuration)

        response = api_client.submit_file('files', authorization, _file_request(tmp_path))

        assert response.id == 'file_123'
        assert _sent_file(http_client).closed

    def test_should_close_the_uploaded_file_when_the_api_returns_an_error(self, mock_sdk_configuration, tmp_path):
        api_client, http_client, authorization = _build(mock_sdk_configuration, status=422)

        with pytest.raises(CheckoutApiException):
            api_client.submit_file('files', authorization, _file_request(tmp_path))

        assert _sent_file(http_client).closed

    def test_should_close_the_uploaded_file_when_the_connection_fails(self, mock_sdk_configuration, tmp_path):
        api_client, http_client, authorization = _build(mock_sdk_configuration,
                                                        request_side_effect=ConnectionError('unreachable'))

        with pytest.raises(CheckoutException):
            api_client.submit_file('files', authorization, _file_request(tmp_path))

        assert _sent_file(http_client).closed
