import uuid

import pytest

from checkout_sdk.issuing.disputes import CreateDisputeRequest, DisputeEvidence, EscalateDisputeRequest
from tests.checkout_test_utils import assert_response


@pytest.mark.skip("Requires permissions to create disputes and simulate transactions")
class TestDisputesIssuing:
    # tests

    def test_should_create_dispute(self, issuing_checkout_api, transaction):
        request = build_create_dispute_request(transaction.id)
        idempotency_key = str(uuid.uuid4())

        response = issuing_checkout_api.issuing.create_dispute(request, idempotency_key)

        assert_response(response,
                        'id',
                        'transaction_id',
                        'reason',
                        'status')
        assert response.id.startswith('idsp_')
        assert response.transaction_id == request.transaction_id
        assert response.reason == request.reason

    def test_should_get_dispute_details(self, issuing_checkout_api, transaction):
        request = build_create_dispute_request(transaction.id)
        created = issuing_checkout_api.issuing.create_dispute(request, str(uuid.uuid4()))

        response = issuing_checkout_api.issuing.get_dispute_details(created.id)

        assert_response(response,
                        'id',
                        'transaction_id',
                        'reason')
        assert response.id == created.id
        assert response.transaction_id == created.transaction_id

    def test_should_cancel_dispute(self, issuing_checkout_api, transaction):
        request = build_create_dispute_request(transaction.id)
        idempotency_key = str(uuid.uuid4())
        created = issuing_checkout_api.issuing.create_dispute(request, idempotency_key)

        response = issuing_checkout_api.issuing.cancel_dispute(created.id, idempotency_key)

        assert_response(response)
        assert response.http_metadata.status_code == 200

    def test_should_escalate_dispute(self, issuing_checkout_api, transaction):
        request = build_create_dispute_request(transaction.id)
        idempotency_key = str(uuid.uuid4())
        created = issuing_checkout_api.issuing.create_dispute(request, idempotency_key)

        response = issuing_checkout_api.issuing.escalate_dispute(
            created.id, build_escalate_dispute_request(), idempotency_key)

        assert_response(response)
        assert response.http_metadata.status_code == 200


# common methods

def build_create_dispute_request(transaction_id: str) -> CreateDisputeRequest:
    evidence = DisputeEvidence()
    evidence.name = 'receipt.pdf'
    evidence.content = 'SGVsbG8gV29ybGQ='
    evidence.description = 'Transaction receipt showing unauthorized charge'

    request = CreateDisputeRequest()
    request.transaction_id = transaction_id
    request.reason = '4837'
    request.evidence = [evidence]
    request.amount = 1000
    request.justification = 'Customer reports unauthorized transaction'
    return request


def build_escalate_dispute_request() -> EscalateDisputeRequest:
    evidence = DisputeEvidence()
    evidence.name = 'location_evidence.pdf'
    evidence.content = 'TG9jYXRpb24gRXZpZGVuY2U='
    evidence.description = 'GPS data showing customer location during transaction'

    request = EscalateDisputeRequest()
    request.justification = 'Merchant response was insufficient. Escalating to pre-arbitration.'
    request.additional_evidence = [evidence]
    request.amount = 800
    return request
