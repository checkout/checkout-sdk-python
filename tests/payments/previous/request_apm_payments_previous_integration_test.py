from __future__ import absolute_import

import pytest

from checkout_sdk.common.enums import Country, Currency
from checkout_sdk.payments.payments_previous import PaymentRequest
from checkout_sdk.payments.payments_apm_previous import IntegrationType, \
    RequestBoletoSource, RequestFawrySource, RequestGiropaySource, RequestIdealSource, RequestOxxoSource, \
    RequestPagoFacilSource, RequestRapiPagoSource, RequestSofortSource, FawryProduct, RequestAlipaySource, \
    RequestBenefitPaySource, RequestEpsSource, RequestKnetSource, RequestP24Source, RequestPayPalSource, \
    RequestPoliSource, RequestBancontactSource, RequestQPaySource, RequestMultiBancoSource
from tests.checkout_test_utils import assert_response, retriable, get_payer


@pytest.mark.skip(reason='not available')
def test_should_make_ali_pay_payment(previous_api):
    request_source = RequestAlipaySource()

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 100
    payment_request.currency = Currency.USD

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)

    assert_response(payment_response, 'id')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


@pytest.mark.skip(reason='not available')
def test_should_make_benefit_pay_payment(previous_api):
    request_source = RequestBenefitPaySource()
    request_source.integration_type = 'mobile'

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 100
    payment_request.currency = Currency.USD

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)

    assert_response(payment_response, 'id')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


@pytest.mark.skip(reason='not available')
@pytest.mark.parametrize('integration_type', [IntegrationType.REDIRECT, IntegrationType.DIRECT])
def test_should_request_boleto_payment(previous_api, integration_type: IntegrationType):
    request_source = RequestBoletoSource()
    request_source.country = Country.BR
    request_source.description = 'boleto payment'
    request_source.payer = get_payer()
    request_source.integration_type = integration_type

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 100
    payment_request.currency = Currency.BRL

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


def test_should_make_eps_payment(previous_api):
    request_source = RequestEpsSource()
    request_source.purpose = 'Mens black t-shirt L'

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 100
    payment_request.currency = Currency.EUR

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


def test_should_request_fawry_payment(previous_api):
    product = FawryProduct()
    product.product_id = '0123456789'
    product.description = 'Fawry Demo Product'
    product.price = 1000
    product.quantity = 1

    request_source = RequestFawrySource()
    request_source.description = 'Fawry Demo Payment'
    request_source.customer_email = 'bruce@wayne-enterprises.com'
    request_source.customer_mobile = '01058375055'
    request_source.products = [product]

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 1000
    payment_request.currency = Currency.EGP

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


def test_should_request_giropay_payment(previous_api):
    request_source = RequestGiropaySource()
    request_source.purpose = 'CKO Giropay test'

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 1000
    payment_request.currency = Currency.EUR
    payment_request.capture = True

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


def test_should_request_ideal_payment(previous_api):
    request_source = RequestIdealSource()
    request_source.bic = 'INGBNL2A'
    request_source.description = 'ORD50234E89'
    request_source.language = 'nl'

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 1000
    payment_request.currency = Currency.EUR
    payment_request.capture = True

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


@pytest.mark.skip(reason='not available')
def test_should_request_oxxo_payment(previous_api):
    request_source = RequestOxxoSource()
    request_source.country = Country.MX
    request_source.description = 'description'
    request_source.payer = get_payer()

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 1000
    payment_request.currency = Currency.MXN

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


@pytest.mark.skip(reason='not available')
def test_should_request_pagofacil_payment(previous_api):
    request_source = RequestPagoFacilSource()
    request_source.country = Country.AR
    request_source.description = 'description'
    request_source.payer = get_payer()

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 1000
    payment_request.currency = Currency.ARS

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


@pytest.mark.skip(reason='not available')
def test_should_request_rapipago_payment(previous_api):
    request_source = RequestRapiPagoSource()
    request_source.country = Country.AR
    request_source.description = 'description'
    request_source.payer = get_payer()

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 1000
    payment_request.currency = Currency.ARS

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


def test_should_request_sofort_payment(previous_api):
    payment_request = PaymentRequest()
    payment_request.source = RequestSofortSource()
    payment_request.amount = 10000
    payment_request.currency = Currency.EUR
    payment_request.capture = True

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


def test_should_make_knet_payment(previous_api):
    request_source = RequestKnetSource()
    request_source.language = "en"

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 100
    payment_request.currency = Currency.KWD
    payment_request.capture = True

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


def test_should_make_przelewy24_payment(previous_api):
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

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


def test_should_make_pay_pal_payment(previous_api):
    request_source = RequestPayPalSource()
    request_source.invoice_number = 'CKO00001'
    request_source.logo_url = 'https://www.example.com/logo.jpg'

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 100
    payment_request.currency = Currency.EUR
    payment_request.capture = True

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


def test_should_make_poli_payment(previous_api):
    payment_request = PaymentRequest()
    payment_request.source = RequestPoliSource()
    payment_request.amount = 100
    payment_request.currency = Currency.AUD
    payment_request.capture = True

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


def test_should_make_bancontact_payment(previous_api):
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

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


def test_should_make_qpay_payment(previous_api):
    request_source = RequestQPaySource()
    request_source.description = 'QPay Demo Payment'
    request_source.language = 'en'
    request_source.quantity = 1
    request_source.national_id = '070AYY010BU234M'

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 100
    payment_request.currency = Currency.QAR
    payment_request.capture = True

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


@pytest.mark.skip(reason='not available')
def test_should_make_multi_banco_payment(previous_api):
    request_source = RequestMultiBancoSource()
    request_source.payment_country = Country.PT
    request_source.account_holder_name = 'Bruce Wayne'
    request_source.billing_descriptor = 'Multibanco Demo Payment'

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 100
    payment_request.currency = Currency.QAR
    payment_request.capture = True

    payment_response = retriable(callback=previous_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=previous_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')
