from __future__ import absolute_import

import pytest

from checkout_sdk.common.common import CustomerRequest, Product
from checkout_sdk.common.enums import Country, Currency, PaymentSourceType
from checkout_sdk.payments.links.payments_links import PaymentLinkRequest
from checkout_sdk.payments.payments import BillingInformation, PaymentRecipient, ThreeDsRequest, ProcessingSettings, \
    RiskRequest, ShippingDetails
from tests.checkout_test_utils import assert_response, phone, address, random_email


@pytest.mark.skip(reason='not available')
def test_should_create_and_get_payment_link(four_api):
    request = create_payment_link_request()

    response = four_api.payments_links.create_payment_link(request)

    assert_response(response,
                    'http_metadata',
                    'id',
                    'reference',
                    'expires_on',
                    '_links',
                    '_links.self',
                    '_links.redirect',
                    'warnings')

    for warning in response.warnings:
        assert_response(warning,
                        'http_metadata',
                        'code',
                        'value',
                        'description')

    hosted_details = four_api.payments_links.get_payment_link(response.id)

    assert_response(hosted_details,
                    'http_metadata',
                    'id',
                    'reference',
                    'status',
                    'amount',
                    'billing',
                    'currency',
                    'billing',
                    'customer',
                    'created_on',
                    'expires_on',
                    'description',
                    'products',
                    '_links',
                    '_links.self',
                    '_links.redirect', )


def create_payment_link_request():
    customer_request = CustomerRequest()
    customer_request.email = random_email()
    customer_request.name = 'Customer'

    billing_information = BillingInformation()
    billing_information.address = address()
    billing_information.phone = phone()

    shipping_details = ShippingDetails()
    shipping_details.address = address()
    shipping_details.phone = phone()

    recipient = PaymentRecipient()
    recipient.account_number = '123456789'
    recipient.country = Country.ES
    recipient.dob = '1985-05-18'
    recipient.first_name = 'It'
    recipient.last_name = 'Testing'
    recipient.zip = '12345'

    product = Product()
    product.name = 'Gold Necklace'
    product.quantity = 1
    product.price = 10

    three_ds_request = ThreeDsRequest()
    three_ds_request.enabled = True
    three_ds_request.attempt_n3d = False

    processing_settings = ProcessingSettings()
    processing_settings.aft = True

    risk_request = RiskRequest()
    risk_request.enabled = True

    request = PaymentLinkRequest()
    request.amount = 200
    request.reference = 'reference'
    request.currency = Currency.GBP
    request.description = 'Payment for Gold Necklace'
    request.customer = customer_request
    request.shipping = shipping_details
    request.billing = billing_information
    request.recipient = recipient
    request.processing = processing_settings
    request.products = [product]
    request.risk = risk_request
    request.return_url = 'https://example.com/payments/return'
    request.locale = 'en-GB'
    request.three_ds = three_ds_request
    request.expires_in = 6400
    request.capture = True
    request.allow_payment_methods = [PaymentSourceType.CARD, PaymentSourceType.IDEAL]

    return request
