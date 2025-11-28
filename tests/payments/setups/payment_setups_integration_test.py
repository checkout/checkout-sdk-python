from __future__ import absolute_import

from checkout_sdk.common.enums import Currency, Country
from checkout_sdk.payments.payments import PaymentType
from checkout_sdk.payments.setups.setups import (
    PaymentSetupsRequest, Settings, Customer, CustomerEmail, CustomerDevice, MerchantAccount,
    Order, OrderSubMerchant, PaymentMethods, Klarna, KlarnaAccountHolder,
    PaymentMethodOptions, PaymentMethodOption, PaymentMethodAction,
    PaymentMethodInitialization
)
from tests.checkout_test_utils import assert_response, new_uuid, address, phone


def test_should_create_and_get_payment_setup_details(default_api):
    request = create_payment_setups_request()

    response = default_api.setups.create_payment_setup(request)

    assert_response(response,
                    'http_metadata',
                    'id',
                    'processing_channel_id',
                    'amount',
                    'currency')

    payment_setup_details = default_api.setups.get_payment_setup(response.id)

    assert_response(payment_setup_details,
                    'http_metadata',
                    'id',
                    'processing_channel_id',
                    'amount',
                    'currency',
                    'payment_type',
                    'reference',
                    'description')


def test_should_update_payment_setup(default_api):
    # Create initial setup
    request = create_payment_setups_request()
    create_response = default_api.setups.create_payment_setup(request)

    assert_response(create_response, 'id')

    # Update the setup
    update_request = create_payment_setups_request()
    update_request.description = "Updated description"
    update_request.amount = 15000

    update_response = default_api.setups.update_payment_setup(create_response.id, update_request)

    assert_response(update_response,
                    'http_metadata',
                    'id',
                    'amount',
                    'description')


def create_payment_setups_request() -> PaymentSetupsRequest:
    # Create customer
    email = CustomerEmail()
    email.address = "johnsmith@example.com"
    email.verified = True

    customer_phone = phone()

    device = CustomerDevice()
    device.locale = "en_GB"

    merchant_account = MerchantAccount()
    merchant_account.id = "1234"
    merchant_account.returning_customer = True
    merchant_account.total_order_count = 6
    merchant_account.last_payment_amount = 5599  # Using int instead of float

    customer = Customer()
    customer.email = email
    customer.name = "John Smith"
    customer.phone = customer_phone
    customer.device = device
    customer.merchant_account = merchant_account

    # Create settings
    settings = Settings()
    settings.success_url = "http://example.com/payments/success"
    settings.failure_url = "http://example.com/payments/fail"

    # Create order
    order = Order()
    order.discount_amount = 10

    # Create Klarna payment method
    account_holder = KlarnaAccountHolder()
    account_holder.billing_address = address()

    sdk_action = PaymentMethodAction()
    sdk_action.type = "sdk"
    sdk_action.client_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ewogICJzZXNzaW9uX2lkIiA6ICIw"
    sdk_action.session_id = "0b1d9815-165e-42e2-8867-35bc03789e00"

    sdk_option = PaymentMethodOption()
    sdk_option.id = "opt_drzstxerxrku3apsepshbslssu"
    sdk_option.action = sdk_action

    klarna_options = PaymentMethodOptions()
    klarna_options.sdk = sdk_option

    klarna_method = Klarna()
    klarna_method.status = "available"
    klarna_method.flags = ["string"]
    klarna_method.initialization = PaymentMethodInitialization.DISABLED
    klarna_method.account_holder = account_holder
    klarna_method.payment_method_options = klarna_options

    payment_methods = PaymentMethods()
    payment_methods.klarna = klarna_method

    # Create main request
    request = PaymentSetupsRequest()
    request.processing_channel_id = "pc_q4dbxom5jbgudnjzjpz7j2z6uq"
    request.amount = 10000
    request.currency = Currency.GBP
    request.payment_type = PaymentType.REGULAR
    request.reference = new_uuid()
    request.description = "Set of three t-shirts."
    request.payment_methods = payment_methods
    request.settings = settings
    request.customer = customer
    request.order = order

    return request