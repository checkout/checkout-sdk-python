from enum import Enum


class DisputeEvidence:
    name: str
    content: str
    description: str


class DisputeReasonChange:
    reason: str
    justification: str


class IssuingDisputeFraudType(str, Enum):
    CARD_LOST = 'card_lost'
    CARD_STOLEN = 'card_stolen'
    CARD_NEVER_RECEIVED = 'card_never_received'
    FRAUDULENT_ACCOUNT = 'fraudulent_account'
    COUNTERFEIT_CARD = 'counterfeit_card'
    ACCOUNT_TAKEOVER = 'account_takeover'
    CARD_NOT_PRESENT_FRAUD = 'card_not_present_fraud'
    MERCHANT_MISREPRESENTATION = 'merchant_misrepresentation'
    CARDHOLDER_MANIPULATION = 'cardholder_manipulation'
    INCORRECT_PROCESSING = 'incorrect_processing'
    OTHER = 'other'


class IssuingDisputeFraudDetails:
    fraud_type: IssuingDisputeFraudType  # required
    description: str


class CreateDisputeRequest:
    transaction_id: str
    reason: str
    evidence: list  # DisputeEvidence
    amount: int
    presentment_message_id: str
    fraud_details: IssuingDisputeFraudDetails
    justification: str


class EscalateDisputeRequest:
    justification: str
    additional_evidence: list  # DisputeEvidence
    amount: int
    reason_change: DisputeReasonChange
    fraud_details: IssuingDisputeFraudDetails


class AmendDisputeRequest:
    reason: str
    amount: int
    evidence: list  # DisputeEvidence
    fraud_details: IssuingDisputeFraudDetails
    reason_change_justification: str  # max 13000
    action_response: str  # max 1000


class SubmitDisputeRequest:
    # Deprecated: the submit endpoint is deprecated in the API swagger. Use CreateDisputeRequest to
    # create and submit in one step, or AmendDisputeRequest when the dispute status is
    # 'action_required'.
    reason: str
    evidence: list  # DisputeEvidence
    amount: int
