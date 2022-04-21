from __future__ import absolute_import

import pytest

from checkout_sdk.checkout_api import CheckoutApi
from checkout_sdk.webhooks.webhooks import WebhookRequest, WebhookContentType
from tests.checkout_test_utils import assert_response, retriable

__GATEWAY_EVENT_TYPES = ['payment_approved',
                         'payment_pending',
                         'payment_declined',
                         'payment_expired',
                         'payment_canceled',
                         'payment_voided',
                         'payment_void_declined',
                         'payment_captured',
                         'payment_capture_declined',
                         'payment_capture_pending',
                         'payment_refunded',
                         'payment_refund_declined',
                         'payment_refund_pending']


@pytest.fixture(autouse=True)
def clean_webhooks(default_api):
    webhooks = default_api.webhooks.retrieve_webhooks()
    if hasattr(webhooks, 'items'):
        for webhook in webhooks.items:
            default_api.webhooks.remove_webhook(webhook.id)
    yield


def test_full_webhook_operations(default_api):
    webhook_url = 'https://checkout.python.com/webhooks'
    # Create webhook
    webhook = register_webhook(default_api, webhook_url)
    assert_response(webhook,
                    'id',
                    'active',
                    'content_type',
                    'event_types',
                    'headers',
                    'url')
    assert webhook_url == webhook.url
    assert bool(set(__GATEWAY_EVENT_TYPES).intersection(webhook.event_types))

    # Retrieve webhook
    retrieve_webhook = retriable(callback=default_api.webhooks.retrieve_webhook,
                                 webhook_id=webhook.id)

    assert webhook_url == retrieve_webhook.url
    assert bool(set(__GATEWAY_EVENT_TYPES).intersection(retrieve_webhook.event_types))

    # Update webhook
    update_request = WebhookRequest()
    update_request.url = 'https://checkout.python.com/failed'
    update_request.headers = retrieve_webhook.headers
    update_request.event_types = ["source_updated"]
    update_request.active = True
    update_request.content_type = WebhookContentType.JSON

    updated_webhook = retriable(callback=default_api.webhooks.update_webhook,
                                webhook_id=webhook.id,
                                webhook_request=update_request)

    assert_response(updated_webhook,
                    'id',
                    'active',
                    'content_type',
                    'event_types',
                    'headers',
                    'url')

    assert update_request.url == updated_webhook.url
    assert bool(set(update_request.event_types).intersection(updated_webhook.event_types))

    # Delete webhook
    remove_webhook = default_api.webhooks.remove_webhook(webhook.id)
    assert_response(remove_webhook, 'http_response')
    assert 200 == remove_webhook.http_response.status_code


def register_webhook(default_api: CheckoutApi, url: str):
    request = WebhookRequest()
    request.url = url
    request.event_types = __GATEWAY_EVENT_TYPES

    return default_api.webhooks.register_webhook(request)
