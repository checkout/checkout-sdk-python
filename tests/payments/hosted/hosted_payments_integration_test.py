from __future__ import absolute_import

import pytest

from checkout_sdk.common.common import CustomerRequest, Product
from checkout_sdk.common.enums import Currency, PaymentSourceType
from checkout_sdk.payments.hosted.hosted_payments import HostedPaymentsSessionRequest
from checkout_sdk.payments.payments import BillingDescriptor, ShippingDetails, ThreeDsRequest, RiskRequest, \
    ProcessingSettings
from checkout_sdk.payments.payments_previous import BillingInformation
from tests.checkout_test_utils import assert_response, phone, address, random_email, get_payment_recipient


@pytest.mark.skip(reason='not available')
def test_should_create_and_get_hosted_payments_page_details(default_api):
    request = create_hosted_payments_request()

    response = default_api.hosted_payments.create_hosted_payments_page_session(request)

    assert_response(response,
                    'http_metadata',
                    'id',
                    'reference',
                    '_links',
                    '_links.self',
                    '_links.redirect')

    hosted_details = default_api.hosted_payments.get_hosted_payments_page_details(response.id)

    assert_response(hosted_details,
                    'http_metadata',
                    'id',
                    'reference',
                    'status',
                    'amount',
                    'billing',
                    'currency',
                    'customer',
                    'description',
                    'failure_url',
                    'success_url',
                    'cancel_url',
                    'products',
                    '_links',
                    '_links.self',
                    '_links.redirect')


def create_hosted_payments_request():
    customer_request = CustomerRequest()
    customer_request.email = random_email()
    customer_request.name = 'Customer'

    billing_information = BillingInformation()
    billing_information.address = address()
    billing_information.phone = phone()

    shipping_details = ShippingDetails()
    shipping_details.address = address()
    shipping_details.phone = phone()

    product = Product()
    product.name = 'Gold Necklace'
    product.quantity = 1
    product.price = 1000

    three_ds_request = ThreeDsRequest()
    three_ds_request.enabled = True
    three_ds_request.attempt_n3d = False

    processing_settings = ProcessingSettings()
    processing_settings.aft = True

    risk_request = RiskRequest()
    risk_request.enabled = True

    billing_descriptor = BillingDescriptor()
    billing_descriptor.city = 'London'
    billing_descriptor.name = 'Awesome name'
    billing_descriptor.reference = 'another reference'

    request = HostedPaymentsSessionRequest()
    request.amount = 1000
    request.reference = 'reference'
    request.currency = Currency.GBP
    request.description = 'Payment for Gold Necklace'
    request.display_name = 'Gold Necklace'
    request.customer = customer_request
    request.shipping = shipping_details
    request.billing = billing_information
    request.recipient = get_payment_recipient()
    request.processing = processing_settings
    request.products = [product]
    request.risk = risk_request
    request.success_url = 'https://example.com/payments/success'
    request.failure_url = 'https://example.com/payments/failure'
    request.cancel_url = 'https://example.com/payments/cancel'
    request.locale = 'en-GB'
    request.three_ds = three_ds_request
    request.capture = True
    request.billing_descriptor = billing_descriptor
    request.allow_payment_methods = [PaymentSourceType.CARD, PaymentSourceType.IDEAL]

    return request
