from datetime import datetime


class BalancesQuery:
    """Query filter for GET /balances/{id}.

    The swagger declares withCurrencyAccountId and balancesAt in camelCase. The mapping to those
    wire names is handled centrally by JsonSerializer._KEYS_TRANSFORMATIONS, so the attributes
    stay snake_case here.
    """
    # A query to filter the balances, for example "currency:GBP".
    # [Optional]
    query: str
    # Specifies if the response should include the sub-account ID that corresponds to each set of
    # balances.
    # [Optional]
    # Default: False
    with_currency_account_id: bool
    # A UTC datetime to retrieve historical balances at a specific point in time. Must be in the
    # past. If omitted, the response returns live balances.
    # [Optional]
    # Format: date-time (RFC 3339)
    balances_at: datetime
