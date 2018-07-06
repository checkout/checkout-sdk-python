import requests
import time

from checkout_sdk import errors, constants, HttpResponse, HttpMethod
from urllib.parse import urljoin

http_headers_default = {
    'user-agent': 'checkout-sdk-python/{}'.format(constants.VERSION)
}


class HttpClient:
    def __init__(self, config):
        self.config = config

        # init Http Session (for pooling)
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

    def send(self, path, method=HttpMethod.GET, request=None):
        start = time.time()

        # call the interceptor as a hook to override the url, headers and/or request
        url, headers, request = self.interceptor(
            urljoin(self.config.api_base_url, path), self.headers, request)

        try:
            r = self._session.request(
                method=method.value,
                url=url,
                json=request,
                headers=headers,
                timeout=self.config.timeout/1000)
            elapsed = '{0:.2f}'.format((time.time() - start)*1000)

            r.raise_for_status()
            try:
                body = r.json()
            except ValueError:
                body = None

            return HttpResponse(r.status_code, r.headers, body, elapsed)
        except requests.exceptions.HTTPError as e:
            status_code_switch = {
                400: lambda: errors.BadRequestError,
                401: lambda: errors.AuthenticationError,
                404: lambda: errors.ResourceNotFoundError,
                422: lambda: errors.TooManyRequestsError,
                500: lambda: errors.ApiError
            }
            jsonResponse = e.response.json()
            errorCls = status_code_switch.get(e.response.status_code,
                                              errors.ApiError)()
            raise errorCls(
                event_id=jsonResponse['eventId'],
                http_status=e.response.status_code,
                error_code=jsonResponse['errorCode'],
                message=jsonResponse['message'],
                elapsed=elapsed)
        except requests.exceptions.Timeout as e:
            elapsed = time.time() - start
            raise errors.Timeout(elapsed=elapsed)
        except requests.exceptions.RequestException:
            raise errors.ApiError(
                message='Unexpected API connection error - please contact support@checkout.com')
