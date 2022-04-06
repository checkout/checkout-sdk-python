from __future__ import absolute_import


class Environment:

    def __init__(self, base_uri,
                 authorization_uri,
                 files_uri,
                 transfers_uri,
                 balances_uri,
                 is_sandbox):
        self.base_uri = base_uri
        self.authorization_uri = authorization_uri
        self.files_uri = files_uri
        self.transfers_uri = transfers_uri
        self.balances_uri = balances_uri
        self.is_sandbox = is_sandbox

    @staticmethod
    def sandbox():
        return Environment(base_uri='https://api.sandbox.checkout.com/',
                           authorization_uri='https://access.sandbox.checkout.com/connect/token',
                           files_uri='https://files.sandbox.checkout.com/',
                           transfers_uri='https://transfers.sandbox.checkout.com/',
                           balances_uri='https://balances.sandbox.checkout.com/',
                           is_sandbox=True)

    @staticmethod
    def production():
        return Environment(base_uri='https://api.checkout.com/',
                           authorization_uri='https://access.checkout.com/connect/token',
                           files_uri='https://files.checkout.com/',
                           transfers_uri='https://transfers.checkout.com/',
                           balances_uri='https://balances.checkout.com/',
                           is_sandbox=False)
