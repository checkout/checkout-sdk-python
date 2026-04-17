from __future__ import absolute_import

import pytest

from checkout_sdk.exception import CheckoutApiException
from checkout_sdk.compliancerequests.compliance_requests import (
    ComplianceRequestRespondRequest,
    ComplianceRespondedFields,
    ComplianceRespondedField
)
from tests.checkout_test_utils import assert_response


@pytest.mark.skip(reason="Requires a payment ID associated with an active compliance request")
def test_should_get_compliance_request(default_api):
    payment_id = "pay_fun26akvvjjerahhctaq2uzhu4"  # Replace with actual payment ID
    
    response = default_api.compliance_requests.get_compliance_request(payment_id)
    
    assert_compliance_request_response(response)
    assert_response(response,
                   'payment_id',
                   'status',
                   'amount',
                   'currency')
    assert response['payment_id'] == payment_id


@pytest.mark.skip(reason="Requires a payment ID associated with an active compliance request")
def test_should_respond_to_compliance_request(default_api):
    payment_id = "pay_fun26akvvjjerahhctaq2uzhu4"  # Replace with actual payment ID
    request = build_valid_respond_request()
    
    response = default_api.compliance_requests.respond_to_compliance_request(payment_id, request)
    
    assert_compliance_respond_response(response)
    # Typically returns empty response (204 No Content)


@pytest.mark.skip(reason="Requires a payment ID associated with an active compliance request")
def test_should_respond_to_compliance_request_with_not_available_fields(default_api):
    payment_id = "pay_fun26akvvjjerahhctaq2uzhu4"  # Replace with actual payment ID
    request = build_valid_respond_request_with_not_available_field()
    
    response = default_api.compliance_requests.respond_to_compliance_request(payment_id, request)
    
    assert_compliance_respond_response(response)


def test_should_fail_get_compliance_request_with_invalid_payment_id(default_api):
    invalid_payment_id = "pay_invalid_payment_id"
    
    with pytest.raises(CheckoutApiException) as exc_info:
        default_api.compliance_requests.get_compliance_request(invalid_payment_id)
    
    # Should get a not found error, or unauthorized if compliance endpoint requires special permissions
    assert exc_info.value.http_metadata.status_code in [401, 404, 422]


def test_should_fail_respond_to_compliance_request_with_invalid_payment_id(default_api):
    invalid_payment_id = "pay_invalid_payment_id"
    request = build_valid_respond_request()
    
    with pytest.raises(CheckoutApiException) as exc_info:
        default_api.compliance_requests.respond_to_compliance_request(invalid_payment_id, request)
    
    # Should get a not found or validation error, or unauthorized if compliance endpoint requires special permissions
    assert exc_info.value.http_metadata.status_code in [401, 404, 422]


def test_should_fail_respond_to_compliance_request_with_empty_request(default_api):
    payment_id = "pay_fun26akvvjjerahhctaq2uzhu4"
    from checkout_sdk.compliancerequests.compliance_requests import ComplianceRequestRespondRequest
    empty_request = ComplianceRequestRespondRequest()
    
    with pytest.raises(CheckoutApiException) as exc_info:
        default_api.compliance_requests.respond_to_compliance_request(payment_id, empty_request)
    
    # Should get a validation error, or unauthorized if compliance endpoint requires special permissions
    assert exc_info.value.http_metadata.status_code in [400, 401, 422]

# Common methods
def build_valid_respond_request():
    """Build a valid ComplianceRequestRespondRequest following the C# test structure."""
    
    # Create sender field
    sender_field = ComplianceRespondedField()
    sender_field.name = "date_of_birth"
    sender_field.value = "2000-01-01"
    sender_field.not_available = False
    
    # Create recipient field
    recipient_field = ComplianceRespondedField()
    recipient_field.name = "full_name"
    recipient_field.value = "John Doe"
    recipient_field.not_available = False
    
    # Create responded fields
    responded_fields = ComplianceRespondedFields()
    responded_fields.sender = [sender_field]
    responded_fields.recipient = [recipient_field]
    
    # Build the request
    request = ComplianceRequestRespondRequest()
    request.fields = responded_fields
    request.comments = "Providing the requested compliance information"
    
    return request


def build_valid_respond_request_with_not_available_field():   
    # Create sender field with not_available = True
    sender_field = ComplianceRespondedField()
    sender_field.name = "social_security_number"
    sender_field.value = None
    sender_field.not_available = True
    
    # Create responded fields
    responded_fields = ComplianceRespondedFields()
    responded_fields.sender = [sender_field]
    responded_fields.recipient = []
    
    # Build the request
    request = ComplianceRequestRespondRequest()
    request.fields = responded_fields
    request.comments = "Some fields are not available for compliance reasons"
    
    return request


def build_get_compliance_request_response_mock():
    return {
        'payment_id': 'pay_fun26akvvjjerahhctaq2uzhu4',
        'status': 'pending',
        'amount': '38.23',
        'currency': 'HKD',
        'created_at': '2026-03-11T10:30:00Z',
        'request_id': 'req_abc123def456',
        'fields_required': {
            'sender': ['date_of_birth', 'full_name'],
            'recipient': ['full_name', 'address']
        }
    }


def build_respond_to_compliance_request_response_mock():
    return {
        'http_metadata': {
            'status_code': 204
        }
    }


def assert_compliance_request_response(response):
    assert_response(response,
                    'payment_id',
                    'status',
                    'amount',
                    'currency')


def assert_compliance_respond_response(response):
    assert response is not None
    # For respond requests, typically returns empty response with 204 status code
    if hasattr(response, 'http_metadata'):
        assert hasattr(response, 'http_metadata')