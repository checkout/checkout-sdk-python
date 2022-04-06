from __future__ import absolute_import

from datetime import datetime, timezone

from checkout_sdk.common.enums import Currency
from checkout_sdk.customers.customers_four import CustomerRequest
from checkout_sdk.four.checkout_api import CheckoutApi
from checkout_sdk.instruments.instruments_four import InstrumentAccountHolder, CreateTokenInstrumentRequest
from checkout_sdk.risk.risk import CardSourcePrism, CustomerSourcePrism, IdSourcePrism, RiskRequestTokenSource, \
    RiskPaymentRequestSource, PreAuthenticationAssessmentRequest, AuthenticationResult, AuthorizationResult, \
    PreCaptureAssessmentRequest, RiskShippingDetails, Device, Location, RiskPayment
from checkout_sdk.tokens.tokens import CardTokenRequest
from tests.checkout_test_utils import assert_response, VisaCard, address, common_customer_request, random_email, phone


def test_should_pre_capture_and_authenticate_card(four_api):
    card_source = CardSourcePrism()
    card_source.billing_address = address()
    card_source.number = VisaCard.number
    card_source.expiry_month = VisaCard.expiry_month
    card_source.expiry_year = VisaCard.expiry_year
    card_source.name = VisaCard.name

    authentication_assessment_request(four_api, card_source)
    pre_capture_assessment_request(four_api, card_source)


def test_should_pre_capture_and_authenticate_customer(four_api):
    customer = CustomerRequest()
    customer.email = random_email()
    customer.name = 'Customer'
    customer.phone = phone()

    customer_response = four_api.customers.create(customer)

    source_prism = CustomerSourcePrism()
    source_prism.id = customer_response.id

    authentication_assessment_request(four_api, source_prism)
    pre_capture_assessment_request(four_api, source_prism)


def test_should_pre_capture_and_authenticate_id(four_api):
    card_token_request = CardTokenRequest()
    card_token_request.number = VisaCard.number
    card_token_request.expiry_month = VisaCard.expiry_month
    card_token_request.expiry_year = VisaCard.expiry_year
    card_token_request.cvv = VisaCard.cvv
    card_token_request.name = VisaCard.name
    card_token_request.billing_address = address()
    card_token_request.phone = phone()

    card_token_response = four_api.tokens.request_card_token(card_token_request)

    account_holder = InstrumentAccountHolder()
    account_holder.billing_address = address()
    account_holder.phone = phone()

    instrument_request = CreateTokenInstrumentRequest()
    instrument_request.token = card_token_response.token
    instrument_request.account_holder = account_holder

    instrument_response = four_api.instruments.create(instrument_request)

    source_prism = IdSourcePrism()
    source_prism.id = instrument_response.id
    source_prism.cvv = VisaCard.cvv

    authentication_assessment_request(four_api, source_prism)
    pre_capture_assessment_request(four_api, source_prism)


def test_should_pre_capture_and_authenticate_token(four_api):
    card_token_request = CardTokenRequest()
    card_token_request.number = VisaCard.number
    card_token_request.expiry_month = VisaCard.expiry_month
    card_token_request.expiry_year = VisaCard.expiry_year
    card_token_request.cvv = VisaCard.cvv
    card_token_request.name = VisaCard.name
    card_token_request.billing_address = address()
    card_token_request.phone = phone()

    card_token_response = four_api.tokens.request_card_token(card_token_request)

    token_source = RiskRequestTokenSource()
    token_source.token = card_token_response.token
    token_source.phone = phone()
    token_source.billing_address = address()

    authentication_assessment_request(four_api, token_source)
    pre_capture_assessment_request(four_api, token_source)


def authentication_assessment_request(api_client: CheckoutApi, request_source: RiskPaymentRequestSource):
    request = PreAuthenticationAssessmentRequest()
    request.date = datetime.now(timezone.utc)
    request.source = request_source
    request.customer = common_customer_request()
    request.payment = get_risk_payment()
    request.shipping = get_risk_shipping_details()
    request.reference = 'ORD-1011-87AH'
    request.description = 'Set of 3 masks'
    request.amount = 6540
    request.currency = Currency.GBP
    request.device = get_device()
    request.metadata = {
        'VoucherCode': 'loyalty_10',
        'discountApplied': '10',
        'customer_id': '2190EF321'}

    response = api_client.risk.request_pre_authentication_risk_scan(request)

    assert_response(response,
                    'http_response',
                    'assessment_id',
                    'result',
                    'result.decision',
                    'result.details',
                    '_links')


def pre_capture_assessment_request(api_client: CheckoutApi, request_source: RiskPaymentRequestSource):
    authentication_result = AuthenticationResult()
    authentication_result.attempted = True
    authentication_result.challenged = True
    authentication_result.liability_shifted = True
    authentication_result.method = '3ds'
    authentication_result.succeeded = True
    authentication_result.version = '2.0'

    authorization_result = AuthorizationResult()
    authorization_result.avs_code = 'Y'
    authorization_result.cvv_result = 'N'

    request = PreCaptureAssessmentRequest()
    request.date = datetime.now(timezone.utc)
    request.source = request_source
    request.customer = common_customer_request()
    request.payment = get_risk_payment()
    request.shipping = get_risk_shipping_details()
    request.amount = 6540
    request.currency = Currency.GBP
    request.device = get_device()
    request.metadata = {
        'VoucherCode': 'loyalty_10',
        'discountApplied': '10',
        'customer_id': '2190EF321'}
    request.authentication_result = authentication_result
    request.authorization_result = authorization_result

    response = api_client.risk.request_pre_capture_risk_scan(request)

    assert_response(response,
                    'http_response',
                    'assessment_id',
                    'result',
                    'result.decision',
                    'result.details',
                    '_links')


def get_risk_shipping_details() -> RiskShippingDetails:
    shipping_details = RiskShippingDetails()
    shipping_details.address = address()
    return shipping_details


def get_device() -> Device:
    location = Location()
    location.longitude = '0.1313'
    location.latitude = '51.5107'

    device = Device()
    device.location = location
    device.type = 'Phone'
    device.os = 'ISO'
    device.model = 'iPhone X'
    device.date = datetime.now(timezone.utc)
    device.user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, ' \
                        'like Gecko) Version/11.0 Mobile/15A372 Safari/604.1 '
    device.fingerprint = '34304a9e3fg09302'
    return device


def get_risk_payment() -> RiskPayment:
    risk_payment = RiskPayment()
    risk_payment.psp = 'CheckoutSdk.com'
    risk_payment.id = '78453878'
    return risk_payment
