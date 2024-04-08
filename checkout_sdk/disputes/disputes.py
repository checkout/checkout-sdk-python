from datetime import datetime


class DisputesQueryFilter:
    limit: int
    skip: int
    from_: datetime
    to: datetime
    id: str
    statuses: str
    payment_id: str
    payment_reference: str
    payment_arn: str
    this_channel_only: bool  # Only available for CS2
    entity_ids: str
    sub_entity_ids: str
    payment_mcc: str


class DisputeEvidenceRequest:
    proof_of_delivery_or_service_file: str
    proof_of_delivery_or_service_text: str
    invoice_or_receipt_file: str
    invoice_or_receipt_text: str
    invoice_showing_distinct_transactions_file: str
    invoice_showing_distinct_transactions_text: str
    customer_communication_file: str
    customer_communication_text: str
    refund_or_cancellation_policy_file: str
    refund_or_cancellation_policy_text: str
    recurring_transaction_agreement_file: str
    recurring_transaction_agreement_text: str
    additional_evidence_file: str
    additional_evidence_text: str
    proof_of_delivery_or_service_date_file: str
    proof_of_delivery_or_service_date_text: str
