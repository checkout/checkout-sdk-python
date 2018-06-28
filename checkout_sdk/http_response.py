class HttpResponse:
    def __init__(self, status, headers, body, elapsed):
        self.status = status
        self.headers = headers
        self.body = body        # dict
        self.elapsed = elapsed  # ms

    def __str__(self):
        return '{0.status} {0.elapsed}'.format(self)
