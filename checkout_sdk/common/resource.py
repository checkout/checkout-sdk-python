from checkout_sdk import constants
from checkout_sdk.common import HTTPResponse, Link


class Resource:
    def __init__(self, api_response):
        if not isinstance(api_response, HTTPResponse):
            raise TypeError(
                'api_response must be a valid instance of HTTPResponse')
        self._response = api_response

        self._links = {}
        links = self._response.body['_links']
        for key in links:
            self._links[key] = Link(links[key].get(
                'href'), links[key].get('title'))

    @property
    def http_response(self):
        """HTTP response with status, headers, JSON body and elapsed time (ms)."""
        return self._response

    @property
    def request_id(self):
        return self._response.headers.get(constants.REQUEST_ID_HEADER)

    @property
    def api_version(self):
        return self._response.headers.get(constants.API_VERSION_HEADER)

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
