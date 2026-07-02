from enum import Enum

from checkout_sdk.common.common import Phone, Address


class CardholderType(str, Enum):
    INDIVIDUAL = 'individual'


class CardholderRequest:
    type: CardholderType
    reference: str
    entity_id: str
    first_name: str
    middle_name: str
    last_name: str
    email: str
    phone_number: Phone
    date_of_birth: str
    billing_address: Address
    residency_address: Address
