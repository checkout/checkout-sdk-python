from __future__ import absolute_import

import pytest

from checkout_sdk.apm.bacs import BacsNotificationRequest, BacsNotificationType
from checkout_sdk.common.enums import Currency
from tests.checkout_test_utils import assert_response


@pytest.mark.skip(reason='Requires a merchant enabled for Bacs Direct Debit and an existing Bacs instrument')
def test_should_send_bacs_notification(default_api):
    request = BacsNotificationRequest()
    request.source_id = 'src_wmlfc3zyhqzehihu7giusaaawu'
    request.notification_type = BacsNotificationType.ADVANCE_NOTICE
    request.collection_date = '2026-07-15'
    request.amount = 4999
    request.currency = Currency.GBP
    request.customer_email = 'customer@example.com'
    request.billing_descriptor = 'CHECKOUT'
    request.support_email = 'support@test.com'

    response = default_api.bacs.send_notification(request)

    assert_response(response, 'event_id')
