from enum import Enum


class WebhookContentType(str, Enum):
    JSON = 'json'


class WebhookRequest:
    url: str
    active: bool
    headers: dict
    content_type: WebhookContentType
    event_types: list
