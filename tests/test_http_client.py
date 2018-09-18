import unittest
import os
import tests
import json

import checkout_sdk as sdk

from checkout_sdk import Config, HttpClient, HttpMethod, errors, constants
from tests.base import CheckoutSdkTestCase
from unittest.mock import MagicMock, Mock, patch
from urllib.parse import urljoin
from requests import Session


class HttpClientTests(CheckoutSdkTestCase):
    RESPONSE_BODY = json.dumps({'key': 'value'})
    PATH = 'test'
    TIMEOUT = constants.DEFAULT_TIMEOUT

    def setUp(self):
        super().setUp()

        self.mock_requests_patcher = patch('checkout_sdk.http_client.requests')
        self.mock_requests = self.mock_requests_patcher.start()

        self.session = MagicMock(spec=Session)
        self.mock_requests.Session = MagicMock(return_value=self.session)

    def tearDown(self):
        super().tearDown()
        self.mock_requests_patcher.stop()

    def set_mock_response(self, name, headers, body, status_code=200):
        response = Mock(name=name, status_code=status_code, headers=headers)
        response.json.return_value = body
        self.session.request = MagicMock(return_value=response)

    def test_http_client_get(self):
        config = Config()
        http_client = HttpClient(config)
        self.set_mock_response(
            'client_get', http_client.headers, self.RESPONSE_BODY)
        response = http_client.send(self.PATH, HttpMethod.GET)

        self.assertEqual(
            str(response), '{0.status} {0.elapsed}'.format(response))
        self.assertEqual(response.body, self.RESPONSE_BODY)
        self.assert_http_call_params(
            path=urljoin(config.api_base_url, self.PATH), method='GET', request=None, headers=response.headers)

    def assert_http_call_params(self, path, method, headers, request):
        self.session.request.assert_called_with(
            url=path,
            method=method,
            headers=headers,
            json=request,
            timeout=self.TIMEOUT/1000
        )
