from __future__ import absolute_import

import os

import pytest

from checkout_sdk.checkout_sdk import CheckoutSdk
from checkout_sdk.common.common import Address, CustomerRequest, Phone, Product, AccountHolder
from checkout_sdk.common.enums import Currency, Country
from checkout_sdk.exception import CheckoutApiException
from checkout_sdk.payments.payment_apm import RequestIdealSource, RequestTamaraSource, \
    PaymentRequestWeChatPaySource, RequestAlipayPlusSource, RequestP24Source, RequestKnetSource, \
    RequestBancontactSource, RequestMultiBancoSource, RequestPostFinanceSource, RequestStcPaySource, RequestAlmaSource, \
    RequestKlarnaSource, RequestFawrySource
from checkout_sdk.payments.payments import PaymentRequest, ProcessingSettings, FawryProduct, PaymentCustomerRequest
from checkout_sdk.payments.payments_apm_previous import RequestSofortSource
from tests.checkout_test_utils import assert_response, SUCCESS_URL, FAILURE_URL, retriable, address, FIRST_NAME, \
    LAST_NAME, phone, check_error_item, PAYEE_NOT_ONBOARDED, APM_SERVICE_UNAVAILABLE, random_email, new_uuid


def test_should_request_ideal_payment(default_api):
    request_source = RequestIdealSource()
    request_source.bic = 'INGBNL2A'
    request_source.description = 'ORD50234E89'
    request_source.language = 'nl'

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 1000
    payment_request.currency = Currency.EUR
    payment_request.capture = True
    payment_request.success_url = SUCCESS_URL
    payment_request.failure_url = FAILURE_URL

    payment_response = retriable(callback=default_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'http_metadata',
                    'id',
                    'status',
                    '_links',
                    '_links.self')

    payment_details = retriable(callback=default_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'http_metadata',
                    'id',
                    'requested_on',
                    'source',
                    'amount',
                    'currency',
                    'payment_type',
                    'status')


def test_should_request_sofort_payment(default_api):
    payment_request = PaymentRequest()
    payment_request.source = RequestSofortSource()
    payment_request.amount = 100
    payment_request.currency = Currency.EUR
    payment_request.capture = True
    payment_request.success_url = SUCCESS_URL
    payment_request.failure_url = FAILURE_URL

    payment_response = retriable(callback=default_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'http_metadata',
                    'id',
                    'status',
                    '_links',
                    '_links.self',
                    '_links.redirect')

    payment_details = retriable(callback=default_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'http_metadata',
                    'id',
                    'requested_on',
                    'source',
                    'amount',
                    'currency',
                    'payment_type',
                    'status')


@pytest.mark.skip(reason='preview')
def test_should_request_tamara_payment():
    address = Address()
    address.address_line1 = 'Cecilia Chapman'
    address.address_line2 = '711-2880 Nulla St.'
    address.city = 'Mankato'
    address.state = 'Mississippi'
    address.zip = '96522'
    address.country = Country.SA

    payment_request_source = RequestTamaraSource()
    payment_request_source.billing_address = address

    processing_settings = ProcessingSettings()
    processing_settings.aft = True
    processing_settings.tax_amount = 500
    processing_settings.shipping_amount = 1000

    phone = Phone()
    phone.number = '113 496 0000'
    phone.country_code = '+966'

    customer_request = CustomerRequest()
    customer_request.name = 'Cecilia Chapman'
    customer_request.email = 'c.chapman@example.com'
    customer_request.phone = phone

    product = Product()
    product.name = 'Item name'
    product.quantity = 3
    product.unit_price = 100
    product.total_amount = 100
    product.tax_amount = 19
    product.discount_amount = 2
    product.reference = 'some description about item'
    product.image_url = 'https://some_s3bucket.com'
    product.url = 'https://some.website.com/item'
    product.sku = '123687000111'

    payment_request = PaymentRequest()
    payment_request.source = payment_request_source
    payment_request.amount = 10000
    payment_request.currency = Currency.SAR
    payment_request.capture = True
    payment_request.success_url = SUCCESS_URL
    payment_request.failure_url = FAILURE_URL
    payment_request.processing = processing_settings
    payment_request.processing_channel_id = 'pc_zs5fqhybzc2e3jmq3efvybybpq'
    payment_request.customer = customer_request
    payment_request.reference = 'ORD-5023-4E89'
    payment_request.items = [product]

    preview_api = CheckoutSdk \
        .builder() \
        .oauth() \
        .client_credentials(client_id=os.environ.get('CHECKOUT_PREVIEW_OAUTH_CLIENT_ID'),
                            client_secret=os.environ.get('CHECKOUT_PREVIEW_OAUTH_CLIENT_SECRET')) \
        .build()

    payment_response = retriable(callback=preview_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    'reference',
                    'status',
                    '_links',
                    'customer',
                    'customer.id',
                    'customer.name',
                    'customer.email',
                    'customer.phone')


def test_should_request_we_chat_pay_payment(default_api):
    payment_request = PaymentRequest()
    payment_request.source = PaymentRequestWeChatPaySource()
    payment_request.amount = 100
    payment_request.currency = Currency.EUR
    payment_request.capture = True
    payment_request.success_url = SUCCESS_URL
    payment_request.failure_url = FAILURE_URL

    check_error_item(callback=default_api.payments.request_payment,
                     error_item=PAYEE_NOT_ONBOARDED,
                     payment_request=payment_request)


def test_should_request_alipay_plus_payment(default_api):
    source = RequestAlipayPlusSource.request_alipay_plus_cn_source()

    payment_request = PaymentRequest()
    payment_request.source = source
    payment_request.amount = 100
    payment_request.currency = Currency.EUR
    payment_request.capture = True
    payment_request.success_url = SUCCESS_URL
    payment_request.failure_url = FAILURE_URL

    try:
        default_api.payments.request_payment(payment_request)
        pytest.fail()
    except CheckoutApiException as err:
        assert err.args[0] == 'The API response status code (422) does not indicate success.'


def test_should_make_przelewy24_payment(default_api):
    request_source = RequestP24Source()
    request_source.payment_country = Country.PL
    request_source.account_holder_name = 'Bruce Wayne'
    request_source.account_holder_email = 'ruce@wayne-enterprises.com'
    request_source.billing_descriptor = 'P24 Demo Payment'

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 100
    payment_request.currency = Currency.PLN
    payment_request.capture = True
    payment_request.success_url = SUCCESS_URL
    payment_request.failure_url = FAILURE_URL

    check_error_item(callback=default_api.payments.request_payment,
                     error_item=PAYEE_NOT_ONBOARDED,
                     payment_request=payment_request)


def test_should_make_knet_payment(default_api):
    request_source = RequestKnetSource()
    request_source.language = "en"

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 100
    payment_request.currency = Currency.KWD
    payment_request.capture = True
    payment_request.success_url = SUCCESS_URL
    payment_request.failure_url = FAILURE_URL

    check_error_item(callback=default_api.payments.request_payment,
                     error_item=PAYEE_NOT_ONBOARDED,
                     payment_request=payment_request)


def test_should_make_bancontact_payment(default_api):
    request_source = RequestBancontactSource()
    request_source.payment_country = Country.BE
    request_source.account_holder_name = 'Bruce Wayne'
    request_source.account_holder_email = 'ruce@wayne-enterprises.com'
    request_source.billing_descriptor = 'bancontact Demo Payment'

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 100
    payment_request.currency = Currency.EUR
    payment_request.capture = True
    payment_request.success_url = SUCCESS_URL
    payment_request.failure_url = FAILURE_URL

    check_error_item(callback=default_api.payments.request_payment,
                     error_item=PAYEE_NOT_ONBOARDED,
                     payment_request=payment_request)


def test_should_make_multi_banco_payment(default_api):
    request_source = RequestMultiBancoSource()
    request_source.payment_country = Country.PT
    request_source.account_holder_name = 'Bruce Wayne'
    request_source.billing_descriptor = 'Multibanco Demo Payment'

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 100
    payment_request.currency = Currency.EUR
    payment_request.capture = True
    payment_request.success_url = SUCCESS_URL
    payment_request.failure_url = FAILURE_URL

    check_error_item(callback=default_api.payments.request_payment,
                     error_item=PAYEE_NOT_ONBOARDED,
                     payment_request=payment_request)


def test_should_make_post_finance_payment(default_api):
    request_source = RequestPostFinanceSource()
    request_source.payment_country = Country.CH
    request_source.account_holder_name = 'Bruce Wayne'
    request_source.billing_descriptor = 'Multibanco Demo Payment'

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 100
    payment_request.currency = Currency.EUR
    payment_request.capture = True
    payment_request.success_url = SUCCESS_URL
    payment_request.failure_url = FAILURE_URL

    check_error_item(callback=default_api.payments.request_payment,
                     error_item=PAYEE_NOT_ONBOARDED,
                     payment_request=payment_request)


def test_should_make_stc_pay_payment(default_api):
    customer_request = PaymentCustomerRequest()
    customer_request.email = random_email()
    customer_request.name = "Louis Smith"
    customer_request.phone = phone()

    payment_request = PaymentRequest()
    payment_request.source = RequestStcPaySource()
    payment_request.amount = 100
    payment_request.currency = Currency.SAR
    payment_request.capture = True
    payment_request.success_url = SUCCESS_URL
    payment_request.failure_url = FAILURE_URL
    payment_request.reference = new_uuid()
    payment_request.customer = customer_request

    check_error_item(callback=default_api.payments.request_payment,
                     error_item=APM_SERVICE_UNAVAILABLE,
                     payment_request=payment_request)


def test_should_make_alma_payment(default_api):
    request_source = RequestAlmaSource()
    request_source.billing_address = address()

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 100
    payment_request.currency = Currency.EUR
    payment_request.capture = True
    payment_request.success_url = SUCCESS_URL
    payment_request.failure_url = FAILURE_URL

    check_error_item(callback=default_api.payments.request_payment,
                     error_item=PAYEE_NOT_ONBOARDED,
                     payment_request=payment_request)


def test_should_make_klarna_payment(default_api):
    account_holder = AccountHolder()
    account_holder.first_name = FIRST_NAME
    account_holder.last_name = LAST_NAME
    account_holder.phone = phone()
    account_holder.billing_address = address()

    request_source = RequestKlarnaSource()
    request_source.account_holder = account_holder

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 100
    payment_request.currency = Currency.EUR
    payment_request.capture = True
    payment_request.success_url = SUCCESS_URL
    payment_request.failure_url = FAILURE_URL

    check_error_item(callback=default_api.payments.request_payment,
                     error_item=APM_SERVICE_UNAVAILABLE,
                     payment_request=payment_request)


def test_should_request_fawry_payment(default_api):
    product = FawryProduct()
    product.product_id = '0123456789'
    product.description = 'Fawry Demo Product'
    product.price = 10
    product.quantity = 1

    request_source = RequestFawrySource()
    request_source.description = 'Fawry Demo Payment'
    request_source.customer_email = 'bruce@wayne-enterprises.com'
    request_source.customer_mobile = '01058375055'
    request_source.products = [product]

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 10
    payment_request.currency = Currency.EGP
    payment_request.success_url = SUCCESS_URL
    payment_request.failure_url = FAILURE_URL

    check_error_item(callback=default_api.payments.request_payment,
                     error_item=PAYEE_NOT_ONBOARDED,
                     payment_request=payment_request)
