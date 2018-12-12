import os

from tests.base import CheckoutSdkTestCase
from checkout_sdk.common import Resource, HTTPResponse


class ResourceTests(CheckoutSdkTestCase):
    def test_resource(self):
        resource = Resource(HTTPResponse(
            200, {}, {"key": "value", "_links": {"self": "http://url"}}, 0))
        self.assertIsNotNone(resource.http_response)
        self.assertIsNone(resource.api_version)
        self.assertIsNotNone(resource.self_link)
