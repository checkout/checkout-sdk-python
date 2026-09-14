from collections import Counter

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

    def test_should_expose_documented_values_for_scopes_added_in_spec_sync(self):
        """The scopes added when this enum was synced against the spec.

        None of these four are declared in clientCredentials.scopes: they appear only in the
        per-operation security requirements of GET/POST /compliance-requests/{payment_id} and
        GET /tokens/{tokenId}/metadata. An enum built from the declared map alone would miss them.
        """
        assert OAuthScopes.COMPLIANCE_REQUESTS.value == 'compliance-requests'
        assert OAuthScopes.COMPLIANCE_REQUESTS_READ.value == 'compliance-requests:read'
        assert OAuthScopes.COMPLIANCE_REQUESTS_RESPOND.value == 'compliance-requests:respond'
        assert OAuthScopes.VAULT_TOKENS_METADATA.value == 'vault:tokens-metadata'

    def test_should_retain_the_legacy_scopes_the_spec_omits(self):
        """These five appear nowhere in the spec, so a spec-driven sweep would delete them.

        They are kept deliberately: the authorization server still grants them and callers still
        request them. marketplace is the proof -- the sandbox payouts client is provisioned for it
        and answers a request for accounts with invalid_scope.
        """
        assert OAuthScopes.ISSUING_CARD_MGMT.value == 'issuing:card-mgmt'
        assert OAuthScopes.ISSUING_CLIENT.value == 'issuing:client'
        assert OAuthScopes.MARKETPLACE.value == 'marketplace'
        assert OAuthScopes.MIDDLEWARE_GATEWAY.value == 'middleware:gateway'
        assert OAuthScopes.MIDDLEWARE_PAYMENT_CONTEXT.value == 'middleware:payment-context'

    def test_should_distinguish_the_two_payment_context_scopes(self):
        """PAYMENT_CONTEXT and GATEWAY_PAYMENT_CONTEXTS read alike but are unrelated scopes.

        The spec requires the former for GET /payment-contexts/{id} and the latter for
        POST /payment-contexts. 'Payment Context' is the only scope whose value contains a space and
        a capital letter, which is almost certainly a spec authoring defect -- asserted verbatim
        because that is the value the authorization server is documented to accept.
        """
        assert OAuthScopes.PAYMENT_CONTEXT.value == 'Payment Context'
        assert OAuthScopes.GATEWAY_PAYMENT_CONTEXTS.value == 'gateway:payment-contexts'

    def test_should_expose_a_non_blank_wire_value_for_every_member(self):
        """A blank value is not caught by the assertions above, which only read members they name.

        oauth_credentials.py joins the requested scopes with a space, so a blank member would be
        sent as an empty entry and the token endpoint would reject the whole request, costing the
        caller every other scope it asked for.
        """
        blank = [scope.name for scope in OAuthScopes if not scope.value.strip()]
        assert blank == []

    def test_should_not_reuse_a_wire_value_across_members(self):
        """A duplicate wire value means one of the two members is a copy-paste error.

        Python's Enum hides this far better than the other SDKs' constructs do: the second member
        to declare a value becomes an *alias* of the first rather than a member of its own, so
        `OAuthScopes.VAULT_TOKENS_METADATA is OAuthScopes.VAULT_TOKENIZATION` would simply be True
        and the scope the aliased name was meant to carry would be unreachable, with nothing
        failing loudly.

        This must iterate __members__, not the enum: iteration *skips* aliases, so counting values
        that way can never see a duplicate and the assertion would hold vacuously.
        """
        duplicates = [value for value, count in
                      Counter(scope.value for scope in OAuthScopes.__members__.values()).items()
                      if count > 1]
        assert duplicates == []

    def test_should_declare_members_in_alphabetical_order(self):
        """Members are kept alphabetical so the next spec sync produces a readable diff.

        Underscores are ignored when comparing, which is what puts PAYMENT_CONTEXT,
        PAYMENT_SESSIONS and PAYMENTS_SEARCH in that order, matching the other Checkout SDKs.
        """
        declared = [scope.name.replace('_', '').lower() for scope in OAuthScopes]
        assert declared == sorted(declared)
