from __future__ import absolute_import

from datetime import datetime

from checkout_sdk.common.common import CustomerRequest
from checkout_sdk.common.enums import Currency, Country
from checkout_sdk.four.checkout_api import CheckoutApi
from checkout_sdk.payments.payments import RequestTokenSource, ThreeDsRequest
from checkout_sdk.payments.payments_four import PaymentRequestCardSource, PaymentRequest, Identification, \
    IdentificationType, PaymentIndividualSender, PaymentInstrumentSender, PaymentCorporateSender
from checkout_sdk.tokens.tokens import CardTokenRequest
from tests.checkout_test_utils import VisaCard, address, phone, assert_response, random_email, new_uuid, FIRST_NAME, \
    LAST_NAME, NAME, SUCCESS_URL, FAILURE_URL


def make_card_payment(four_api: CheckoutApi, amount: int = 10, capture_on: datetime = None,
                      idempotency_key: str = None, capture=False):
    request_card_source = PaymentRequestCardSource()
    request_card_source.number = VisaCard.number
    request_card_source.expiry_month = VisaCard.expiry_month
    request_card_source.expiry_year = VisaCard.expiry_year
    request_card_source.cvv = VisaCard.cvv
    request_card_source.name = VisaCard.name
    request_card_source.billing_address = address()
    request_card_source.phone = phone()

    customer_request = CustomerRequest()
    customer_request.email = random_email()
    customer_request.name = 'Customer'

    identification = Identification()
    identification.issuing_country = Country.GT
    identification.number = '1234'
    identification.type = IdentificationType.DRIVING_LICENSE

    payment_individual_sender = PaymentIndividualSender()
    payment_individual_sender.first_name = FIRST_NAME
    payment_individual_sender.last_name = LAST_NAME
    payment_individual_sender.address = address()
    payment_individual_sender.identification = identification

    payment_request = PaymentRequest()
    payment_request.source = request_card_source

    payment_request.reference = new_uuid()
    payment_request.amount = amount
    payment_request.currency = Currency.USD
    payment_request.capture = capture
    payment_request.reference = new_uuid()
    payment_request.customer = customer_request
    payment_request.sender = payment_individual_sender

    if capture_on is not None:
        payment_request.capture = True
        payment_request.capture_on = capture_on

    payment_response = four_api.payments.request_payment(payment_request, idempotency_key)
    assert_response(payment_response, 'id')
    return payment_response


def make_token_payment(four_api: CheckoutApi):
    card_token_request = CardTokenRequest()
    card_token_request.name = VisaCard.name
    card_token_request.number = VisaCard.number
    card_token_request.expiry_year = VisaCard.expiry_year
    card_token_request.expiry_month = VisaCard.expiry_month
    card_token_request.cvv = VisaCard.cvv
    card_token_request.billing_address = address()
    card_token_request.phone = phone()

    card_token_response = four_api.tokens.request_card_token(card_token_request)
    assert card_token_response is not None

    request_token_source = RequestTokenSource()
    request_token_source.token = card_token_response.token

    customer_request = CustomerRequest()
    customer_request.email = random_email()

    payment_instrument_sender = PaymentInstrumentSender()

    payment_request = PaymentRequest()
    payment_request.source = request_token_source
    payment_request.capture = True
    payment_request.reference = new_uuid()
    payment_request.amount = 10
    payment_request.currency = Currency.USD
    payment_request.customer = customer_request
    payment_request.sender = payment_instrument_sender

    payment_response = four_api.payments.request_payment(payment_request)
    assert_response(payment_response, 'id')
    return payment_response


def make_3ds_card_payment(four_api: CheckoutApi, attempt_n3d: bool = False):
    request_card_source = PaymentRequestCardSource()
    request_card_source.number = VisaCard.number
    request_card_source.expiry_month = VisaCard.expiry_month
    request_card_source.expiry_year = VisaCard.expiry_year
    request_card_source.cvv = VisaCard.cvv
    request_card_source.name = VisaCard.name
    request_card_source.billing_address = address()
    request_card_source.phone = phone()

    customer_request = CustomerRequest()
    customer_request.email = random_email()
    customer_request.name = NAME

    three_ds_request = ThreeDsRequest()
    three_ds_request.enabled = True
    three_ds_request.attempt_n3d = attempt_n3d
    three_ds_request.eci = '05' if attempt_n3d else ''
    three_ds_request.cryptogram = 'AgAAAAAAAIR8CQrXcIhbQAAAAAA' if attempt_n3d else ''
    three_ds_request.xid = 'MDAwMDAwMDAwMDAwMDAwMzIyNzY' if attempt_n3d else ''
    three_ds_request.version = '2.0.1'

    payment_corporate_sender = PaymentCorporateSender()
    payment_corporate_sender.company_name = 'Testing Inc.'
    payment_corporate_sender.address = address()

    payment_request = PaymentRequest()
    payment_request.source = request_card_source
    payment_request.reference = new_uuid()
    payment_request.amount = 10
    payment_request.currency = Currency.GBP
    payment_request.customer = customer_request
    payment_request.three_ds = three_ds_request
    payment_request.success_url = SUCCESS_URL
    payment_request.failure_url = FAILURE_URL

    payment_response = four_api.payments.request_payment(payment_request)
    assert_response(payment_response, 'id')
    return payment_response
