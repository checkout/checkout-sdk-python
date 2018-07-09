import re
import pprint

from checkout_sdk import HttpMethod, logger

SNAKE_CASE_REGEX = re.compile(r'_([a-z])')


def _snake_to_camel_case(name):
    return SNAKE_CASE_REGEX.sub(lambda x: x.group(1).upper(), name)


class ApiClient:
    def __init__(self, http_client):
        self._http_client = http_client

    def _send_http_request(self, url, method, request=None):
        if request:
            request = self._convert_json_case(request)

        response = self._http_client.send(url, method, request)
        self._log_info(response)        # http status, elapsed
        self._log_debug('HTTP response:\n'+pprint.pformat(response.body))
        return response

    def _convert_json_case(self, json):
        output = {}
        for k, v in json.items():
            output[_snake_to_camel_case(k)] = self._convert_json_case(
                v) if isinstance(v, dict) else v
        return output

    def _log_info(self, message, **kwargs):
        logger.info(message, **kwargs)

    def _log_debug(self, message, **kwargs):
        logger.debug(message, **kwargs)
