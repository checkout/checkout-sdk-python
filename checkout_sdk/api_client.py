from checkout_sdk import ApiResponse


class ApiClient:
    def __init__(self, http_client):
        self._http_client = http_client

    def _build_response(self, status, headers, body, elapsed):
        return ApiResponse(status, headers, body, elapsed)
