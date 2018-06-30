import re

from checkout_sdk import HttpMethod

SNAKE_CASE_REGEX = re.compile(r'_([a-z])')


def _snake_to_camel_case(name):
    return SNAKE_CASE_REGEX.sub(lambda x: x.group(1).upper(), name)


class ApiClient:
    def __init__(self, http_client):
        self._http_client = http_client

    def _send_http_request(self, url, method, request):
        request = self._convert_json_case(request)
        return getattr(self._http_client, method.value.lower())(url, request)

    def _convert_json_case(self, json):
        output = {}
        for k, v in json.items():
            output[_snake_to_camel_case(k)] = self._convert_json_case(
                v) if isinstance(v, dict) else v
        return output
