import pytest

from checkout_sdk.events.events import RetrieveEventsRequest
from tests.checkout_test_utils import assert_response, retriable
from tests.payments.previous.payments_previous_test_utils import make_card_payment
from tests.webhooks.webhooks_integration_test import register_webhook

__PAYMENT_EVENT_TYPES = ['payment_approved',
                         'payment_canceled',
                         'payment_capture_declined',
                         'payment_capture_pending',
                         'payment_captured',
                         'payment_chargeback',
                         'payment_declined',
                         'payment_expired',
                         'payment_paid',
                         'payment_pending',
                         'payment_refund_declined',
                         'payment_refund_pending',
                         'payment_refunded',
                         'payment_retrieval',
                         'payment_void_declined',
                         'payment_voided']


def test_should_retrieve_event_types(previous_api):
    all_event_types = previous_api.events.retrieve_all_event_types()
    assert_response(all_event_types, 'items')
    assert all_event_types.items.__len__() == 2

    version_one_items = previous_api.events.retrieve_all_event_types(all_event_types.items[0].version)
    assert_response(version_one_items, 'items')
    assert version_one_items.items.__len__() == 1
    assert all_event_types.items[0].version == version_one_items.items[0].version

    version_two_items = previous_api.events.retrieve_all_event_types(all_event_types.items[1].version)
    assert_response(version_one_items, 'items')
    assert version_two_items.items.__len__() == 1
    assert all_event_types.items[1].version == version_two_items.items[0].version


@pytest.mark.skip(reason='unstable')
def test_should_retrieve_events_by_payment_id_and_retrieve_event_by_id_and_get_notification(previous_api):
    webhook = register_webhook(previous_api, 'https://checkout.python.com/webhooks')

    payment = make_card_payment(previous_api)

    retrieve_events_request = RetrieveEventsRequest()
    retrieve_events_request.payment_id = payment.id

    events = retriable(callback=previous_api.events.retrieve_events,
                       events_request=retrieve_events_request,
                       predicate=__events_has_data)

    assert_response(events, 'data')
    assert_response(events.data[0], 'created_on', 'id', 'type')

    retrieve_event = previous_api.events.retrieve_event(events.data[0].id)

    assert_response(retrieve_event, 'id', 'notifications', 'data', 'type', 'version')

    event_notification = previous_api.events.retrieve_event_notification(retrieve_event.id,
                                                                         retrieve_event.notifications[0].id)

    assert_response(event_notification, 'id', 'success', 'url', 'content_type')

    retry_webhook = previous_api.events.retry_webhook(events.data[0].id, webhook.id)

    assert_response(retry_webhook, 'http_metadata')

    retry_all_webhooks = previous_api.events.retry_all_webhooks(events.data[0].id)

    assert_response(retry_all_webhooks, 'http_metadata')


def __events_has_data(response) -> bool:
    return hasattr(response, 'data') and response.data.__len__() == 1
