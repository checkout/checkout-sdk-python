from __future__ import absolute_import

from datetime import datetime

from checkout_sdk.previous.checkout_api import CheckoutApi
from checkout_sdk.common.common import CustomerRequest
from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.payments_previous import RequestCardSource, PaymentRequest, RequestTokenSource
from checkout_sdk.payments.payments import ThreeDsRequest
from checkout_sdk.tokens.tokens import CardTokenRequest
from tests.checkout_test_utils import VisaCard, address, phone, assert_response, random_email, new_uuid


def make_card_payment(previous_api: CheckoutApi, amount: int = 10, capture_on: datetime = None,
                      idempotency_key: str = None, capture=False):
    request_card_source = RequestCardSource()
    request_card_source.number = VisaCard.number
    request_card_source.expiry_month = VisaCard.expiry_month
    request_card_source.expiry_year = VisaCard.expiry_year
    request_card_source.cvv = VisaCard.cvv
    request_card_source.name = VisaCard.name
    request_card_source.billing_address = address()
    request_card_source.phone = phone()

    payment_request = PaymentRequest()
    payment_request.source = request_card_source

    payment_request.reference = new_uuid()
    payment_request.amount = amount
    payment_request.currency = Currency.GBP
    payment_request.capture = capture

    if capture_on is not None:
        payment_request.capture = True
        payment_request.capture_on = capture_on

    payment_response = previous_api.payments.request_payment(payment_request, idempotency_key)
    # assert_response(payment_response, 'id')
    return payment_response


def make_token_payment(previous_api: CheckoutApi):
    card_token_request = CardTokenRequest()
    card_token_request.name = VisaCard.name
    card_token_request.number = VisaCard.number
    card_token_request.expiry_year = VisaCard.expiry_year
    card_token_request.expiry_month = VisaCard.expiry_month
    card_token_request.cvv = VisaCard.cvv
    card_token_request.billing_address = address()
    card_token_request.phone = phone()

    card_token_response = previous_api.tokens.request_card_token(card_token_request)
    assert card_token_response is not None

    request_token_source = RequestTokenSource()
    request_token_source.token = card_token_response.token

    customer_request = CustomerRequest()
    customer_request.email = random_email()

    payment_request = PaymentRequest()
    payment_request.source = request_token_source
    payment_request.capture = True
    payment_request.reference = new_uuid()
    payment_request.amount = 10
    payment_request.currency = Currency.USD
    payment_request.customer = customer_request

    payment_response = previous_api.payments.request_payment(payment_request)
    assert_response(payment_response, 'id')
    return payment_response


def make_3ds_card_payment(previous_api: CheckoutApi, attempt_n3d: bool = False):
    request_card_source = RequestCardSource()
    request_card_source.number = VisaCard.number
    request_card_source.expiry_month = VisaCard.expiry_month
    request_card_source.expiry_year = VisaCard.expiry_year
    request_card_source.cvv = VisaCard.cvv
    request_card_source.name = VisaCard.name
    request_card_source.billing_address = address()
    request_card_source.phone = phone()

    customer_request = CustomerRequest()
    customer_request.email = random_email()

    three_ds_request = ThreeDsRequest()
    three_ds_request.enabled = True
    three_ds_request.attempt_n3d = attempt_n3d
    three_ds_request.eci = '05' if attempt_n3d else ''
    three_ds_request.cryptogram = 'AgAAAAAAAIR8CQrXcIhbQAAAAAA' if attempt_n3d else ''
    three_ds_request.xid = 'MDAwMDAwMDAwMDAwMDAwMzIyNzY' if attempt_n3d else ''
    three_ds_request.version = '2.0.1'

    payment_request = PaymentRequest()
    payment_request.source = request_card_source
    payment_request.reference = new_uuid()
    payment_request.amount = 10
    payment_request.currency = Currency.GBP
    payment_request.customer = customer_request
    payment_request.three_ds = three_ds_request

    payment_response = previous_api.payments.request_payment(payment_request)
    assert_response(payment_response, 'id')
    return payment_response
