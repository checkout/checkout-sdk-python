class DisputeEvidence:
    name: str
    content: str
    description: str


class DisputeReasonChange:
    reason: str
    justification: str


class CreateDisputeRequest:
    transaction_id: str
    reason: str
    evidence: list  # DisputeEvidence
    amount: int
    presentment_message_id: str
    justification: str


class EscalateDisputeRequest:
    justification: str
    additional_evidence: list  # DisputeEvidence
    amount: int
    reason_change: DisputeReasonChange
