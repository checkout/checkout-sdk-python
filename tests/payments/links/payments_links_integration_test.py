from __future__ import absolute_import

from checkout_sdk.common.common import CustomerRequest, Product, Commission, AmountAllocations
from checkout_sdk.common.enums import Currency, PaymentSourceType
from checkout_sdk.payments.links.payments_links import PaymentLinkRequest
from checkout_sdk.payments.payments import ShippingDetails, ThreeDsRequest, RiskRequest, ProcessingSettings
from checkout_sdk.payments.payments_previous import BillingInformation
from tests.checkout_test_utils import assert_response, phone, address, random_email, new_uuid, get_payment_recipient


def test_should_create_and_get_payment_link(default_api):
    commission = Commission()
    commission.amount = 1
    commission.percentage = 0.1

    amount_allocations = AmountAllocations()
    amount_allocations.id = 'ent_sdioy6bajpzxyl3utftdp7legq'
    amount_allocations.reference = new_uuid()
    amount_allocations.commission = commission
    amount_allocations.amount = 100

    request = create_payment_link_request()
    request.amount_allocations = [amount_allocations]

    response = default_api.payments_links.create_payment_link(request)

    assert_response(response,
                    'http_metadata',
                    'id',
                    'reference',
                    'expires_on',
                    'warnings')

    for warning in response.warnings:
        assert_response(warning,
                        'code',
                        'value',
                        'description')

    hosted_details = default_api.payments_links.get_payment_link(response.id)

    assert_response(hosted_details,
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
                    '_links.redirect')


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

    product = Product()
    product.name = 'Gold Necklace'
    product.quantity = 1
    product.price = 200

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
    request.recipient = get_payment_recipient()
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
