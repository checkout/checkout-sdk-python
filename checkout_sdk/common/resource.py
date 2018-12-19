from checkout_sdk import constants
from checkout_sdk.common import ResponseDTO, HTTPResponse


class Resource(ResponseDTO):
    def __init__(self, http_response):
        if not isinstance(http_response, HTTPResponse):
            raise TypeError(
                'http_response must be a valid instance of HTTPResponse')

        super().__init__(http_response.body)
        self._response = http_response

    @property
    def http_response(self):
        """
        HTTP response with status, headers,
        JSON body and elapsed time (ms).
        """
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
        return hasattr(self._links, relation)

    def get_link(self, relation):
        return getattr(self._links, relation, None)
