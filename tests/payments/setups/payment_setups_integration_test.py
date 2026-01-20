from __future__ import absolute_import

import os
import pytest

from checkout_sdk.common.common import Address, Phone
from checkout_sdk.common.enums import Currency, Country
from checkout_sdk.payments.payments import PaymentType
from checkout_sdk.payments.setups.setups import (
    PaymentSetupsRequest, Settings, Customer, CustomerEmail, CustomerDevice,
    PaymentMethods, Klarna, KlarnaAccountHolder, PaymentMethodInitialization
)
from tests.checkout_test_utils import assert_response, new_uuid


def test_should_create_payment_setup(default_api):
    """Test creating a payment setup"""
    # Arrange
    request = create_payment_setups_request()

    # Act
    response = default_api.setups.create_payment_setup(request)

    # Assert
    assert_response(response,
                    'http_metadata',
                    'id',
                    'processing_channel_id',
                    'amount',
                    'currency',
                    'payment_type',
                    'reference',
                    'description')

    assert response.processing_channel_id == request.processing_channel_id
    assert response.amount == request.amount
    assert response.currency == request.currency
    assert response.payment_type == request.payment_type
    assert response.reference == request.reference
    assert response.description == request.description


def test_should_update_payment_setup(default_api):
    """Test updating a payment setup"""
    # Arrange
    create_request = create_payment_setups_request()
    create_response = default_api.setups.create_payment_setup(create_request)

    assert_response(create_response, 'id')

    # Create update request
    update_request = create_payment_setups_request()
    update_request.description = "Updated description"

    # Act
    update_response = default_api.setups.update_payment_setup(create_response.id, update_request)

    # Assert
    assert_response(update_response,
                    'http_metadata',
                    'id',
                    'description')

    assert update_response.id == create_response.id
    assert update_response.description == "Updated description"


def test_should_get_payment_setup(default_api):
    """Test retrieving a payment setup"""
    # Arrange
    create_request = create_payment_setups_request()
    create_response = default_api.setups.create_payment_setup(create_request)

    # Act
    response = default_api.setups.get_payment_setup(create_response.id)

    # Assert
    assert_response(response,
                    'http_metadata',
                    'id',
                    'processing_channel_id',
                    'amount',
                    'currency',
                    'payment_type',
                    'reference',
                    'description')

    assert response.id == create_response.id
    assert response.processing_channel_id == create_request.processing_channel_id
    assert response.amount == create_request.amount
    assert response.currency == create_request.currency
    assert response.payment_type == create_request.payment_type
    assert response.reference == create_request.reference
    assert response.description == create_request.description


@pytest.mark.skip(reason="Integration test - requires valid payment method option")
def test_should_confirm_payment_setup(default_api):
    """Test confirming a payment setup"""
    # Arrange
    create_request = create_payment_setups_request()
    create_response = default_api.setups.create_payment_setup(create_request)

    payment_method_option_id = "opt_test_12345"

    # Act
    response = default_api.setups.confirm_payment_setup(
        create_response.id,
        payment_method_option_id
    )

    # Assert
    assert_response(response,
                    'id',
                    'action_id',
                    'amount',
                    'currency',
                    'processed_on')

    assert response.amount == create_request.amount
    assert response.currency == create_request.currency


def create_payment_setups_request() -> PaymentSetupsRequest:
    """Create a payment setup request for testing"""
    request = PaymentSetupsRequest()

    request.processing_channel_id = os.getenv('CHECKOUT_PROCESSING_CHANNEL_ID')
    request.amount = 1000
    request.currency = Currency.GBP
    request.payment_type = PaymentType.REGULAR
    request.reference = f"TEST-REF-{new_uuid()[:6]}"
    request.description = "Integration test payment setup"

    # Settings
    settings = Settings()
    settings.success_url = "https://example.com/success"
    settings.failure_url = "https://example.com/failure"
    request.settings = settings

    # Customer
    customer = Customer()
    customer.name = "John Smith"

    email = CustomerEmail()
    email.address = f"john.smith+{new_uuid()[:6]}@example.com"
    email.verified = True
    customer.email = email

    phone = Phone()
    phone.country_code = "+44"
    phone.number = "207 946 0000"
    customer.phone = phone

    device = CustomerDevice()
    device.locale = "en_GB"
    customer.device = device

    request.customer = customer

    # Payment methods - Klarna example
    payment_methods = PaymentMethods()

    klarna = Klarna()
    klarna.initialization = PaymentMethodInitialization.DISABLED

    account_holder = KlarnaAccountHolder()
    billing_address = Address()
    billing_address.address_line1 = "123 High Street"
    billing_address.city = "London"
    billing_address.zip = "SW1A 1AA"
    billing_address.country = Country.GB
    account_holder.billing_address = billing_address
    klarna.account_holder = account_holder

    payment_methods.klarna = klarna
    request.payment_methods = payment_methods

    return request
