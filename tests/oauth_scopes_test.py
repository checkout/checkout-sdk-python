from checkout_sdk.oauth_scopes import OAuthScopes


class TestOAuthScopes:
    """The enum members are the only place the wire value of a scope is written down.

    A typo would only surface at the token endpoint, which rejects an undefined scope for the
    whole request, so an OAuth-configured caller would lose every scope it asked for alongside
    the bad one.

    Values come from components.securitySchemes.OAuth.flows.clientCredentials.scopes in
    shared/swagger-latest.json.
    """

    def test_should_expose_documented_balances_scope_values(self):
        assert OAuthScopes.BALANCES.value == 'balances'
        assert OAuthScopes.BALANCES_VIEW.value == 'balances:view'
        assert OAuthScopes.BALANCES_TOP_UP_INSTRUCTIONS.value == 'balances:top-up-instructions'
