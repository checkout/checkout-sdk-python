from __future__ import absolute_import

import os

import pytest

import checkout_sdk
from checkout_sdk.accounts.accounts import UpdateScheduleRequest, ScheduleFrequencyWeeklyRequest, DaySchedule, \
    ScheduleFrequencyDailyRequest, ScheduleFrequencyMonthlyRequest
from checkout_sdk.common.enums import Currency
from checkout_sdk.four.oauth_scopes import OAuthScopes
from tests.checkout_test_utils import assert_response


@pytest.fixture(scope='class')
def payout_schedules_api():
    return checkout_sdk.OAuthSdk() \
        .client_credentials(client_id=os.environ.get('CHECKOUT_FOUR_OAUTH_PAYOUT_SCHEDULE_CLIENT_ID'),
                            client_secret=os.environ.get('CHECKOUT_FOUR_OAUTH_PAYOUT_SCHEDULE_CLIENT_SECRET')) \
        .scopes([OAuthScopes.MARKETPLACE]) \
        .build()


def test_should_update_and_retrieve_weekly_payout_schedules(payout_schedules_api):
    weekly_request = ScheduleFrequencyWeeklyRequest()
    weekly_request.by_day = [DaySchedule.TUESDAY]

    schedule_request = UpdateScheduleRequest()
    schedule_request.enabled = True
    schedule_request.threshold = 1000
    schedule_request.recurrence = weekly_request

    payout_schedule = payout_schedules_api.accounts.update_payout_schedule(
        'ent_sdioy6bajpzxyl3utftdp7legq', Currency.USD, schedule_request)

    assert_response(payout_schedule, 'http_metadata')
    assert payout_schedule.http_metadata.status_code == 200

    retrieve_payout_schedule = payout_schedules_api.accounts.retrieve_payout_schedule(
        'ent_sdioy6bajpzxyl3utftdp7legq')

    assert_response(retrieve_payout_schedule, 'http_metadata',
                    'USD',
                    'USD.enabled',
                    'USD.recurrence',
                    'USD.recurrence.frequency',
                    'USD.recurrence.by_day')


def test_should_update_and_retrieve_daily_payout_schedules(payout_schedules_api):
    daily_request = ScheduleFrequencyDailyRequest()

    schedule_request = UpdateScheduleRequest()
    schedule_request.enabled = True
    schedule_request.threshold = 1000
    schedule_request.recurrence = daily_request

    payout_schedule = payout_schedules_api.accounts.update_payout_schedule(
        'ent_sdioy6bajpzxyl3utftdp7legq', Currency.USD, schedule_request)

    assert_response(payout_schedule, 'http_metadata')
    assert payout_schedule.http_metadata.status_code == 200

    retrieve_payout_schedule = payout_schedules_api.accounts.retrieve_payout_schedule(
        'ent_sdioy6bajpzxyl3utftdp7legq')

    assert_response(retrieve_payout_schedule, 'http_metadata',
                    'USD',
                    'USD.enabled',
                    'USD.recurrence',
                    'USD.recurrence.frequency')


def test_should_update_and_retrieve_monthly_payout_schedules(payout_schedules_api):
    montly_request = ScheduleFrequencyMonthlyRequest()
    montly_request.by_month_day = [5]

    schedule_request = UpdateScheduleRequest()
    schedule_request.enabled = True
    schedule_request.threshold = 1000
    schedule_request.recurrence = montly_request

    payout_schedule = payout_schedules_api.accounts.update_payout_schedule(
        'ent_sdioy6bajpzxyl3utftdp7legq', Currency.USD, schedule_request)

    assert_response(payout_schedule, 'http_metadata')
    assert payout_schedule.http_metadata.status_code == 200

    retrieve_payout_schedule = payout_schedules_api.accounts.retrieve_payout_schedule(
        'ent_sdioy6bajpzxyl3utftdp7legq')

    assert_response(retrieve_payout_schedule, 'http_metadata',
                    'USD',
                    'USD.enabled',
                    'USD.recurrence',
                    'USD.recurrence.frequency',
                    'USD.recurrence.by_month_day')
