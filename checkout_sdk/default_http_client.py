from __future__ import absolute_import

import requests

from checkout_sdk.http_client_interface import HttpClientBuilderInterface


class DefaultHttpClientBuilder(HttpClientBuilderInterface):

    def __init__(self):
        self.session = requests.Session()

    def get_client(self):
        return self.session
