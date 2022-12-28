from __future__ import absolute_import

import os
from datetime import datetime, timezone

import pytest
from dateutil.relativedelta import relativedelta

from checkout_sdk.disputes.disputes import DisputesQueryFilter, DisputeEvidenceRequest
from checkout_sdk.files.files import FileRequest
from tests.checkout_test_utils import assert_response, get_project_root, retriable
from tests.payments.previous.payments_previous_test_utils import make_card_payment


def test_should_query_disputes(default_api):
    query = DisputesQueryFilter()
    now = datetime.now(timezone.utc)
    query.from_ = now - relativedelta(months=6)
    query.to = now

    response = default_api.disputes.query(query)
    assert_response(response,
                    'http_metadata',
                    'limit',
                    'total_count',
                    'from',
                    'to')
    if response.data:
        assert_response(response.data[0],
                        'id',
                        'category',
                        'status',
                        'amount',
                        'currency',
                        'reason_code',
                        'payment_id')


def test_should_upload_file(default_api):
    request = FileRequest()
    request.file = os.path.join(get_project_root(), 'tests', 'resources', 'checkout.jpeg')
    request.purpose = 'dispute_evidence'
    response = default_api.disputes.upload_file(request)
    assert_response(response, 'id', '_links')

    file_details = default_api.disputes.get_file_details(response.id)
    assert_response(file_details,
                    'http_metadata',
                    'id',
                    'filename',
                    'purpose',
                    'size',
                    'uploaded_on',
                    '_links')


@pytest.mark.skip(reason='due the time to takes to capture a dispute')
def test_should_test_full_disputes_workflow(default_api):
    payment = make_card_payment(default_api, amount=1040, capture=True)

    query = DisputesQueryFilter()
    query.payment_id = payment.id

    query_response = retriable(callback=default_api.disputes.query,
                               predicate=there_are_disputes,
                               query=query)
    assert_response(query_response, 'data')
    assert payment.id == query_response.data[0].payment_id

    request = FileRequest()
    request.file = os.path.join(get_project_root(), 'tests', 'resources', 'checkout_sdk.jpeg')
    request.purpose = 'dispute_evidence'

    upload_file_response = default_api.disputes.upload_file(request)
    assert_response(upload_file_response, 'id', '_links')

    evidence_request = DisputeEvidenceRequest()
    evidence_request.proof_of_delivery_or_service_file = upload_file_response.id
    evidence_request.proof_of_delivery_or_service_text = 'proof of delivery or service text'
    evidence_request.invoice_or_receipt_file = upload_file_response.id
    evidence_request.invoice_or_receipt_text = 'Copy of the invoice'
    evidence_request.customer_communication_file = upload_file_response.id
    evidence_request.customer_communication_text = 'Copy of an email exchange with the cardholder'
    evidence_request.additional_evidence_file = upload_file_response.id
    evidence_request.additional_evidence_text = 'Scanned document'

    dispute_id = query_response.data[0].id

    default_api.disputes.put_evidence(dispute_id, evidence_request)

    evidence = default_api.disputes.get_evidence(dispute_id)
    assert_response(evidence,
                    'http_metadata',
                    'proof_of_delivery_or_service_file',
                    'proof_of_delivery_or_service_text',
                    'invoice_or_receipt_file',
                    'invoice_or_receipt_text',
                    'customer_communication_file',
                    'customer_communication_text',
                    'additional_evidence_file',
                    'additional_evidence_text')


def there_are_disputes(response) -> bool:
    return response.total_count is not None and response.total_count > 0


def test_should_disputes_scheme_files(default_api):
    disputes_query_filter = DisputesQueryFilter()
    disputes_query_filter.limit = 5

    query_response = default_api.disputes.query(disputes_query_filter)

    if query_response.data:
        for dispute in query_response.data:
            scheme_files = default_api.disputes.get_dispute_scheme_files(dispute.id)
            assert_response(scheme_files,
                            'id',
                            'files')
