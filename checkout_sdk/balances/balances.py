class BalancesQuery:
    query: str
    with_currency_account_id: str
    balances_at: str

    # The /balances/{id} endpoint uses camelCase query params, inconsistent with
    # the rest of the API. Handle the mapping locally so the quirk stays scoped
    # to this class — if the API ever normalizes to snake_case, deleting this
    # method is the entire fix.
    def to_json(self):
        out = {}
        if getattr(self, 'query', None) is not None:
            out['query'] = self.query
        if getattr(self, 'with_currency_account_id', None) is not None:
            out['withCurrencyAccountId'] = self.with_currency_account_id
        if getattr(self, 'balances_at', None) is not None:
            out['balancesAt'] = self.balances_at
        return out
