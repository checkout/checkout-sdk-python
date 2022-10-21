from datetime import datetime


class ReportsQuery:
    created_after: datetime
    created_before: datetime
    entity_id: str
    limit: int
    pagination_token: str
