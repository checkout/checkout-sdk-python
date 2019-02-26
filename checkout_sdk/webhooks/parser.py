import json

from checkout_sdk.common import Event
from checkout_sdk.webhooks.utils import verify_signature, _to_string


def parse(body, webhook_secret, signature_header):
    verify_signature(body, webhook_secret, signature_header)

    event_data = json.loads(_to_string(body))
    return Event(event_data)
