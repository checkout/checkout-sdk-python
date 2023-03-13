class RetrieveEventsRequest:
    payment_id: str
    charge_id: str
    track_id: str
    reference: str
    skip: int
    limit: int
