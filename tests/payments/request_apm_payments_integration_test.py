from __future__ import absolute_import

import pytest

from checkout_sdk.common.enums import Country, Currency
from checkout_sdk.payments.payments import PaymentRequest
from checkout_sdk.payments.payments_apm import RequestBalotoSource, BalotoPayer, Payer, IntegrationType, \
    RequestBoletoSource, RequestFawrySource, RequestGiropaySource, RequestIdealSource, RequestOxxoSource, \
    RequestPagoFacilSource, RequestRapiPagoSource, RequestSofortSource, FawryProduct
from tests.checkout_test_utils import assert_response, random_email, NAME, retriable


@pytest.mark.skip(reason='not available')
def test_should_request_baloto_payment(default_api):
    payer = BalotoPayer()
    payer.email = random_email()
    payer.name = NAME

    request_source = RequestBalotoSource()
    request_source.country = Country.CO
    request_source.description = 'simulate Via Baloto Demo Payment'
    request_source.payer = payer

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 100000
    payment_request.currency = Currency.COP

    payment_response = retriable(callback=default_api.payments.request_payment,
                                 payment_request=payment_request)

    assert_response(payment_response, 'id')

    payment_details = retriable(callback=default_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


@pytest.mark.skip(reason='not available')
@pytest.mark.parametrize('integration_type', [IntegrationType.REDIRECT, IntegrationType.DIRECT])
def test_should_request_boleto_payment(default_api, integration_type: IntegrationType):
    payer = Payer()
    payer.email = random_email()
    payer.name = NAME
    payer.document = '53033315550'

    request_source = RequestBoletoSource()
    request_source.country = Country.BR
    request_source.description = 'boleto payment'
    request_source.payer = payer
    request_source.integration_type = integration_type

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 100
    payment_request.currency = Currency.BRL

    payment_response = retriable(callback=default_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=default_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


def test_should_request_fawry_payment(default_api):
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

    payment_response = retriable(callback=default_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=default_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


def test_should_request_giropay_payment(default_api):
    request_source = RequestGiropaySource()
    request_source.purpose = 'CKO Giropay test'

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 1000
    payment_request.currency = Currency.EUR
    payment_request.capture = True

    payment_response = retriable(callback=default_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=default_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


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

    payment_response = retriable(callback=default_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=default_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


@pytest.mark.skip(reason='not available')
def test_should_request_oxxo_payment(default_api):
    payer = Payer()
    payer.email = random_email()
    payer.name = NAME

    request_source = RequestOxxoSource()
    request_source.country = Country.MX
    request_source.description = 'description'
    request_source.payer = payer

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 1000
    payment_request.currency = Currency.MXN

    payment_response = retriable(callback=default_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=default_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


@pytest.mark.skip(reason='not available')
def test_should_request_pagofacil_payment(default_api):
    payer = Payer()
    payer.email = random_email()
    payer.name = NAME

    request_source = RequestPagoFacilSource()
    request_source.country = Country.AR
    request_source.description = 'description'
    request_source.payer = payer

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 1000
    payment_request.currency = Currency.ARS

    payment_response = retriable(callback=default_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=default_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


@pytest.mark.skip(reason='not available')
def test_should_request_rapipago_payment(default_api):
    payer = Payer()
    payer.email = random_email()
    payer.name = NAME

    request_source = RequestRapiPagoSource()
    request_source.country = Country.AR
    request_source.description = 'description'
    request_source.payer = payer

    payment_request = PaymentRequest()
    payment_request.source = request_source
    payment_request.amount = 1000
    payment_request.currency = Currency.ARS

    payment_response = retriable(callback=default_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=default_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')


@pytest.mark.skip(reason='not available')
def test_should_request_sofort_payment(default_api):
    payment_request = PaymentRequest()
    payment_request.source = RequestSofortSource()
    payment_request.amount = 100000
    payment_request.currency = Currency.ARS
    payment_request.capture = True

    payment_response = retriable(callback=default_api.payments.request_payment,
                                 payment_request=payment_request)
    assert_response(payment_response,
                    'id',
                    '_links')

    payment_details = retriable(callback=default_api.payments.get_payment_details,
                                payment_id=payment_response.id)
    assert_response(payment_details,
                    'id',
                    'source',
                    'amount',
                    '_links')
