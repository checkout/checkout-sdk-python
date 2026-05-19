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
    processing_channel_ids: str
    segment_ids: str


class CompellingEvidenceShippingAddress:
    address: str
    address2: str
    city: str
    state_region: str
    postal_code: str
    country: str


class CompellingEvidenceHistoricalTransaction:
    historical_arn: str
    merchandise_or_service_desc: str


class CompellingEvidence:
    merchandise_or_service: str
    merchandise_or_service_desc: str
    merchandise_or_service_provided_date: datetime
    shipping_delivery_status: str
    tracking_information: str
    user_id: str
    ip_address: str
    device_id: str
    shipping_address: CompellingEvidenceShippingAddress
    historical_transactions: list  # CompellingEvidenceHistoricalTransaction


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
    arbitration_no_review_files: list  # list[str]
    arbitration_no_review_text: str
    arbitration_review_required_files: list  # list[str]
    arbitration_review_required_text: str
    compelling_evidence: CompellingEvidence
