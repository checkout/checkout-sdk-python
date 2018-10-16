from checkout_sdk import Utils
from checkout_sdk.common import HttpResponse


class Resource:
    def __init__(self, api_response):
        if not isinstance(api_response, HttpResponse):
            raise TypeError(
                'api_response must be a valid instance of HttpResponse')
        self._response = api_response
        self._links = self._response.body['_links']

    @property
    def http_response(self):
        """Http response with status, headers, JSON body and elapsed time (ms)."""
        return self._response

    @property
    def links(self):
        return self._links

    @property
    def self_link(self):
        return self.get_link('self')

    def has_link(self, relation):
        return relation in self._links

    def get_link(self, relation):
        return self._links.get(relation, None)
