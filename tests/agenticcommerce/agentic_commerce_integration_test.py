from __future__ import absolute_import

import pytest

from datetime import datetime, timezone, timedelta
from checkout_sdk.agenticcommerce.agentic_commerce import (
    DelegatedPaymentRequest, DelegatedPaymentHeaders, DelegatedPaymentMethodCard,
    DelegatedPaymentAllowance, DelegatedPaymentBillingAddress, DelegatedPaymentRiskSignal,
    DelegatedCardNumberType, DelegatedPaymentAllowanceReason
)
from checkout_sdk.common.enums import Currency, Country
from checkout_sdk.exception import CheckoutApiException
from tests.checkout_test_utils import assert_response


@pytest.mark.skip(reason="Requires a valid HMAC signing key and merchant enabled for agentic commerce")
def test_should_create_delegated_payment_token(default_api):
    request = build_valid_delegated_payment_request()
    headers = build_valid_delegated_payment_headers()

    response = default_api.agentic_commerce.create_delegated_payment_token(request, headers)

    assert_delegated_payment_token_response(response)
    assert_response(response,
                    'id',
                    'created',
                    'metadata')


@pytest.mark.skip(reason="Requires a valid HMAC signing key and merchant enabled for agentic commerce")
def test_should_create_delegated_payment_token_with_billing_address(default_api):
    request = build_valid_delegated_payment_request_with_billing_address()
    headers = build_valid_delegated_payment_headers()

    response = default_api.agentic_commerce.create_delegated_payment_token(request, headers)

    assert_delegated_payment_token_response(response)
    assert_response(response,
                    'id',
                    'created',
                    'metadata')


@pytest.mark.skip(reason="Requires a valid HMAC signing key and merchant enabled for agentic commerce")
def test_should_create_delegated_payment_token_with_network_token(default_api):
    request = build_valid_delegated_payment_request_with_network_token()
    headers = build_valid_delegated_payment_headers()

    response = default_api.agentic_commerce.create_delegated_payment_token(request, headers)

    assert_delegated_payment_token_response(response)
    assert_response(response,
                    'id',
                    'created',
                    'metadata')


def test_should_fail_create_delegated_payment_token_with_invalid_request(default_api):
    from checkout_sdk.agenticcommerce.agentic_commerce import DelegatedPaymentRequest
    invalid_request = DelegatedPaymentRequest()
    headers = build_valid_delegated_payment_headers()

    with pytest.raises(CheckoutApiException) as exc_info:
        default_api.agentic_commerce.create_delegated_payment_token(invalid_request, headers)

    assert exc_info.value.http_metadata.status_code in [400, 422]


def test_should_fail_create_delegated_payment_token_with_invalid_signature(default_api):
    request = build_valid_delegated_payment_request()

    from checkout_sdk.agenticcommerce.agentic_commerce import DelegatedPaymentHeaders
    invalid_headers = DelegatedPaymentHeaders()
    invalid_headers.signature = "invalid-signature"
    invalid_headers.timestamp = "2026-03-11T10:30:00Z"

    with pytest.raises(CheckoutApiException) as exc_info:
        default_api.agentic_commerce.create_delegated_payment_token(request, invalid_headers)

    assert exc_info.value.http_metadata.status_code in [401, 403]


# Common methods
def build_valid_delegated_payment_request():
    payment_method = DelegatedPaymentMethodCard()
    payment_method.card_number_type = DelegatedCardNumberType.FPAN
    payment_method.number = "4242424242424242"
    payment_method.exp_month = "11"
    payment_method.exp_year = "2026"
    payment_method.metadata = {"issuing_bank": "test"}

    allowance = DelegatedPaymentAllowance()
    allowance.reason = DelegatedPaymentAllowanceReason.ONE_TIME
    allowance.max_amount = 10000
    allowance.currency = Currency.USD
    allowance.merchant_id = "cli_vkuhvk4vjn2edkps7dfsq6emqm"
    allowance.checkout_session_id = "1PQrsT"
    allowance.expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

    risk_signal = DelegatedPaymentRiskSignal()
    risk_signal.type = "card_testing"
    risk_signal.score = 10
    risk_signal.action = "blocked"

    request = DelegatedPaymentRequest()
    request.payment_method = payment_method
    request.allowance = allowance
    request.risk_signals = [risk_signal]
    request.metadata = {"campaign": "q4"}

    return request


def build_valid_delegated_payment_request_with_billing_address():
    request = build_valid_delegated_payment_request()

    billing_address = DelegatedPaymentBillingAddress()
    billing_address.name = "John Doe"
    billing_address.line_one = "123 Test Street"
    billing_address.city = "London"
    billing_address.postal_code = "SW1A 1AA"
    billing_address.country = Country.GB

    request.billing_address = billing_address

    return request


def build_valid_delegated_payment_request_with_network_token():
    request = build_valid_delegated_payment_request()

    request.payment_method.card_number_type = DelegatedCardNumberType.NETWORK_TOKEN
    request.payment_method.number = "4111111111111111"

    return request


def build_valid_delegated_payment_headers():
    headers = DelegatedPaymentHeaders()
    headers.signature = "eyJtZX..."
    headers.timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    headers.api_version = "2026-01-01"
    return headers


def build_delegated_payment_response_mock():
    return {
        'id': 'vt_abc123def456ghi789',
        'created': '2026-03-11T10:30:00Z',
        'metadata': {'psp': 'checkout.com'}
    }


def assert_delegated_payment_response(response):
    assert_response(response,
                    'id',
                    'created',
                    'metadata')


def assert_delegated_payment_token_response(response):
    assert response is not None
    assert hasattr(response, 'id')
    assert response['id'] is not None
    assert response['id'].startswith('vt_')
    assert hasattr(response, 'created')
    assert response['created'] is not None
    assert hasattr(response, 'metadata')
    assert response['metadata'] is not None
