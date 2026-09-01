from __future__ import absolute_import

from enum import Enum

from checkout_sdk.common.enums import Currency


# The type of pre-notification being sent to the payer.
class BacsNotificationType(str, Enum):
    ADVANCE_NOTICE = 'advance_notice'


class BacsNotificationRequest:
    r"""Bacs Direct Debit notification request.

    collection_date is a yyyy-MM-dd string. Do not pass a datetime: the serializer emits a full ISO
    timestamp for it, which this field rejects, and a date object raises inside the serializer.

    source_id matches the pattern ^(src)_(\w{26})$. amount is in the currency's minor unit with a
    minimum of 1. currency is min 3 max 3 characters. reference is max 50 and billing_descriptor
    max 25 characters. customer_email and support_email are email addresses, and support_phone is in
    E.164 format. reference and support_phone are the only optional properties.
    """
    source_id: str
    notification_type: BacsNotificationType
    collection_date: str
    amount: int
    currency: Currency
    reference: str
    customer_email: str
    billing_descriptor: str
    support_email: str
    support_phone: str
