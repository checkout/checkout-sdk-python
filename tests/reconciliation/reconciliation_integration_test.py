from __future__ import absolute_import

import os
from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta

from checkout_sdk import CheckoutSdk
from checkout_sdk.common.common import QueryFilterDateRange
from checkout_sdk.environment import Environment
from checkout_sdk.previous.checkout_api import CheckoutApi
from tests.checkout_test_utils import assert_response


@pytest.fixture(scope='class')
def production_api() -> CheckoutApi:
    return CheckoutSdk \
        .builder() \
        .previous() \
        .environment(Environment.production()) \
        .secret_key(os.environ.get('CHECKOUT_PREVIOUS_SECRET_KEY_PROD')) \
        .build()


def query_filter_date():
    date_range = QueryFilterDateRange()
    now = datetime.now()
    date_range.from_ = now - relativedelta(months=3)
    date_range.to = now
    return date_range


@pytest.mark.skip(reason='only works in production')
def test_should_query_payments_report(production_api):
    response = production_api.reconciliation.query_payments_report(query_filter_date())
    assert_response(response, 'http_metadata')
    assert response.http_metadata.status_code == 200


@pytest.mark.skip(reason='only works in production')
def test_should_get_single_payment_report(production_api):
    response = production_api.reconciliation.single_payment_report('pay_oe5vaxisis4krciobenmrv4xze')
    assert_response(response, 'http_metadata')
    assert response.http_metadata.status_code == 200


@pytest.mark.skip(reason='only works in production')
def test_should_query_statements_report(production_api):
    response = production_api.reconciliation.query_statements_report(query_filter_date())
    assert_response(response, 'http_metadata')
    assert response.http_metadata.status_code == 200


@pytest.mark.skip(reason='only works in production')
def test_should_retrieve_csv_payment_report(production_api):
    response = production_api.reconciliation.retrieve_csv_payment_report(query_filter_date())
    assert_response(response, 'contents', 'http_metadata')
    assert response.http_metadata.status_code == 200


@pytest.mark.skip(reason='only works in production')
def test_should_retrieve_csv_single_statement_report(production_api):
    response = production_api.reconciliation.retrieve_csv_single_statement_report('221222B100981')
    assert_response(response, 'contents', 'http_metadata')
    assert response.http_metadata.status_code == 200


@pytest.mark.skip(reason='only works in production')
def test_should_retrieve_csv_statements_report(production_api):
    response = production_api.reconciliation.retrieve_csv_statements_report(query_filter_date())
    assert_response(response, 'contents', 'http_metadata')
    assert response.http_metadata.status_code == 200
