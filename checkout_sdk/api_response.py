class ApiResponse:
    def __init__(self, http_status, headers, body, json, elapsed):
        self.http_status = http_status
        self.headers = headers
        self.body = body        # text
        self.json = json        # dict
        self.elapsed = elapsed  # ms

    def __str__(self):
        return '{0.http_status} {0.elapsed}'.format(self)
