import time
from urllib.parse import urljoin
import requests

from checkout_sdk import errors, constants, HTTPMethod
from checkout_sdk.common import HTTPResponse

HTTP_HEADERS_DEFAULTS = {
    'user-agent': 'checkout-sdk-python/{}'.format(constants.VERSION)
}


class HTTPClient:
    def __init__(self, config):
        self._config = config

        # init HTTP Session (for pooling)
        self._session = requests.Session()

        # interceptor call is a mirror by default
        self.interceptor = lambda url, headers, request: (
            url, headers, request)

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @property
    def headers(self):
        headers = HTTP_HEADERS_DEFAULTS.copy()
        headers['authorization'] = self.config.secret_key
        return headers

    def close_session(self):
        self._session.close()

    def send(self, path, method=HTTPMethod.GET, request=None):
        start = time.time()

        # call the interceptor as a hook to override
        # the url, headers and/or request
        url, headers, request = self.interceptor(
            urljoin(self.config.api_base_url, path), self.headers, request)

        try:
            response = self._session.request(
                method=method,
                url=url,
                json=request,
                headers=headers,
                timeout=self.config.timeout / 1000)
            elapsed = self._calc_elapsed_time(start)

            response.raise_for_status()
            body = response.json()

            return HTTPResponse(response.status_code,
                                response.headers, body, elapsed)
        except requests.exceptions.HTTPError as err:
            status_code_switch = {
                401: errors.AuthenticationError,
                403: errors.NotAllowedError,
                404: errors.ResourceNotFoundError,
                422: errors.ValidationError,
                429: errors.TooManyRequestsError
            }

            try:
                json_response = err.response.json()
            except ValueError:
                json_response = {}
            error_cls = status_code_switch.get(err.response.status_code,
                                               errors.ApiError)

            raise error_cls(
                request_id=err.response.headers.get(
                    constants.REQUEST_ID_HEADER),
                api_version=err.response.headers.get(
                    constants.API_VERSION_HEADER),
                http_status=err.response.status_code,
                error_type=json_response.get('error_type'),
                error_codes=json_response.get('error_codes'),
                elapsed=elapsed)
        except requests.exceptions.Timeout:
            elapsed = self._calc_elapsed_time(start)
            raise errors.ApiTimeoutError(elapsed=elapsed)
        except requests.exceptions.RequestException:
            raise IOError()

    def _calc_elapsed_time(self, start):
        return '{0:.2f}'.format((time.time() - start) * 1000)
