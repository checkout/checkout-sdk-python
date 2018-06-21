from checkout_sdk import ApiResponse


class ApiClient:
    def __init__(self, http_client):
        self._http_client = http_client

    def build_api_response(self, http_status, headers, body, json, elapsed):
        return ApiResponse(http_status, headers, body, json, elapsed)
