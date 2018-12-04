import requests
import time

from checkout_sdk import errors, constants, HTTPMethod
from checkout_sdk.common import HTTPResponse
from urllib.parse import urljoin

http_headers_default = {
    'user-agent': 'checkout-sdk-python/{}'.format(constants.VERSION)
}


class HTTPClient:
    def __init__(self, config):
        self.config = config

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
        headers = http_headers_default.copy()
        headers['authorization'] = self.config.secret_key
        return headers

    def close_session(self):
        self._session.close()

    def send(self, path, method=HTTPMethod.GET, request=None):
        start = time.time()

        # call the interceptor as a hook to override the url, headers and/or request
        url, headers, request = self.interceptor(
            urljoin(self.config.api_base_url, path), self.headers, request)

        try:
            r = self._session.request(
                method=method,
                url=url,
                json=request,
                headers=headers,
                timeout=self.config.timeout/1000)
            elapsed = self._calc_elapsed_time(start)

            r.raise_for_status()
            body = r.json()

            return HTTPResponse(r.status_code, r.headers, body, elapsed)
        except requests.exceptions.HTTPError as e:
            status_code_switch = {
                401: lambda: errors.AuthenticationError,
                403: lambda: errors.NotAllowedError,
                404: lambda: errors.ResourceNotFoundError,
                422: lambda: errors.ValidationError,
                429: lambda: errors.TooManyRequestsError
            }
            jsonResponse = e.response.json()
            print(jsonResponse)
            error_cls = status_code_switch.get(e.response.status_code,
                                               errors.ApiError)()
            raise error_cls(
                request_id=e.response.headers.get(
                    constants.REQUEST_ID_HEADER),
                api_version=e.response.headers.get(
                    constants.API_VERSION_HEADER),
                http_status=e.response.status_code,
                error_type=jsonResponse.get('error_type'),
                error_codes=jsonResponse.get('error_codes'),
                elapsed=elapsed)
        except requests.exceptions.Timeout as e:
            elapsed = self._calc_elapsed_time(start)
            raise errors.TimeoutError(elapsed=elapsed)
        except requests.exceptions.RequestException:
            raise IOError()

    def _calc_elapsed_time(self, start):
        return '{0:.2f}'.format((time.time() - start)*1000)
