from __future__ import absolute_import

from datetime import datetime


class OAuthAccessToken:
    token: str
    expiration_date: datetime

    def __init__(self, token: str, expiration_date: datetime):
        self.token = token
        self.expiration_date = expiration_date

    def is_valid(self):
        if self.token is None:
            return False
        return self.expiration_date > datetime.now()
