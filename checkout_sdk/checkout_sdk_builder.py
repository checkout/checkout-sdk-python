from __future__ import absolute_import

from checkout_sdk.default_http_client import DefaultHttpClientBuilder
from checkout_sdk.environment import Environment
from checkout_sdk.http_client_interface import HttpClientBuilderInterface


class CheckoutSdkBuilder:

    def __init__(self):
        self._environment = Environment.sandbox()
        self._http_client = DefaultHttpClientBuilder().get_client()

    def environment(self, environment: Environment):
        self._environment = environment
        return self

    def http_client_builder(self, http_client_builder: HttpClientBuilderInterface):
        self._http_client = http_client_builder.get_client()
        return self

    def build(self):
        raise NotImplementedError()
