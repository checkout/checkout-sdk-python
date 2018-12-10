import pprint

from checkout_sdk import logger


class ApiClient:
    def __init__(self, http_client):
        self._http_client = http_client

    def _send_http_request(self, url, method, request=None):
        response = self._http_client.send(url, method, request)
        self._log_info(response)  # http status, elapsed
        self._log_debug('HTTP response:\n' + pprint.pformat(response.body))
        return response

    def _log_info(self, message, **kwargs):
        logger.info(message, **kwargs)

    def _log_debug(self, message, **kwargs):
        logger.debug(message, **kwargs)
