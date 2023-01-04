from checkout_sdk.common.common import QueryFilterDateRange


class ReconciliationQueryFilter(QueryFilterDateRange):
    limit: int
    reference: str
