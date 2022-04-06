from __future__ import absolute_import

from checkout_sdk.common.enums import Country, Currency
from checkout_sdk.customers.customers_four import CustomerRequest
from checkout_sdk.four.checkout_api import CheckoutApi
from checkout_sdk.payments.payments_four import PaymentRequestCardSource, Identification, IdentificationType, \
    PaymentIndividualSender, PaymentRequest, AuthorizationType, AuthorizationRequest
from tests.checkout_test_utils import new_uuid, assert_response, new_idempotency_key, VisaCard, address, phone, \
    random_email, FIRST_NAME, LAST_NAME


def test_should_increment_payment_authorization(four_api):
    payment_response = make_authorization_estimated_payment(four_api)

    authorization_request = AuthorizationRequest()
    authorization_request.amount = 5
    authorization_request.reference = new_uuid()

    void_response = four_api.payments.increment_payment_authorization(payment_response.id, authorization_request)
    assert_response(void_response,
                    'http_response',
                    'amount',
                    'action_id',
                    'currency',
                    'response_code',
                    'response_summary',
                    'expires_on',
                    'processed_on',
                    'balances',
                    'response_summary',
                    'risk',
                    '_links')


def test_should_increment_payment_authorization_idempotently(four_api):
    payment_response = make_authorization_estimated_payment(four_api)

    authorization_request = AuthorizationRequest()
    authorization_request.amount = 5
    authorization_request.reference = new_uuid()

    idempotency_key = new_idempotency_key()

    increment_response_1 = four_api.payments.increment_payment_authorization(payment_response.id,
                                                                             authorization_request, idempotency_key)
    assert_response(increment_response_1)

    increment_response_2 = four_api.payments.increment_payment_authorization(payment_response.id,
                                                                             authorization_request, idempotency_key)
    assert_response(increment_response_2)

    assert increment_response_1.action_id == increment_response_2.action_id


def make_authorization_estimated_payment(four_api: CheckoutApi):
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
    identification.type = IdentificationType.NATIONAL_ID

    payment_individual_sender = PaymentIndividualSender()
    payment_individual_sender.first_name = FIRST_NAME
    payment_individual_sender.last_name = LAST_NAME
    payment_individual_sender.address = address()
    payment_individual_sender.identification = identification

    payment_request = PaymentRequest()
    payment_request.source = request_card_source

    payment_request.reference = new_uuid()
    payment_request.amount = 10
    payment_request.currency = Currency.EUR
    payment_request.capture = False
    payment_request.reference = new_uuid()
    payment_request.customer = customer_request
    payment_request.sender = payment_individual_sender
    payment_request.authorization_type = AuthorizationType.ESTIMATED

    payment_response = four_api.payments.request_payment(payment_request, None)
    assert_response(payment_response, 'id')
    return payment_response
