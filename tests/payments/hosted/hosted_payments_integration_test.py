from __future__ import absolute_import

from checkout_sdk.common.common import CustomerRequest, Product
from checkout_sdk.common.enums import Country, Currency, PaymentSourceType
from checkout_sdk.payments.hosted.hosted_payments import HostedPaymentsSessionRequest
from checkout_sdk.payments.payments import BillingInformation, PaymentRecipient, ThreeDsRequest, ProcessingSettings, \
    RiskRequest, ShippingDetails
from tests.checkout_test_utils import assert_response, phone, address, random_email


def test_should_create_and_get_hosted_payments_page_details(default_api):
    request = create_hosted_payments_request()

    response = default_api.hosted_payments.create_hosted_payments_page_session(request)

    assert_response(response,
                    'http_response',
                    'id',
                    'reference',
                    '_links',
                    '_links.self',
                    '_links.redirect')

    hosted_details = default_api.hosted_payments.get_hosted_payments_page_details(response.id)

    assert_response(hosted_details,
                    'http_response',
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

    request = HostedPaymentsSessionRequest()
    request.amount = 1000
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
    request.success_url = 'https://example.com/payments/success'
    request.failure_url = 'https://example.com/payments/failure'
    request.cancel_url = 'https://example.com/payments/cancel'
    request.locale = 'en-GB'
    request.three_ds = three_ds_request
    request.capture = True
    request.allow_payment_methods = [PaymentSourceType.CARD, PaymentSourceType.KLARNA]

    return request
