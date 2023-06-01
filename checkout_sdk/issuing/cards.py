from enum import Enum

from checkout_sdk.common.common import Address, Phone


class CardType(str, Enum):
    PHYSICAL = 'physical'
    VIRTUAL = 'virtual'


class LifetimeUnit(str, Enum):
    MONTHS = 'Months'
    YEARS = 'Years'


class RevokeReason(str, Enum):
    EXPIRED = 'expired'
    REPORTED_LOST = 'reported_lost'
    REPORTED_STOLEN = 'reported_stolen'


class SuspendReason(str, Enum):
    SUSPECTED_LOST = 'suspected_lost'
    SUSPECTED_STOLEN = 'suspected_stolen'


class CardLifetime:
    unit: LifetimeUnit
    value: int


class ShippingInstructions:
    recipient_address: str
    shipping_address: Address
    additional_comment: str


class CardRequest:
    type: CardType
    cardholder_id: str
    lifetime: CardLifetime
    reference: str
    card_product_id: str
    display_name: str
    activate_card: bool

    def __init__(self, type_p: CardType):
        self.type = type_p


class PhysicalCardRequest(CardRequest):
    shipping_instructions: ShippingInstructions

    def __init__(self):
        super().__init__(CardType.PHYSICAL)


class VirtualCardRequest(CardRequest):
    is_single_use: bool

    def __init__(self):
        super().__init__(CardType.VIRTUAL)


class SecurityPair:
    question: str
    answer: str


class ThreeDsEnrollmentRequest:
    locale: str
    phone_number: Phone


class SecurityQuestionEnrollmentRequest(ThreeDsEnrollmentRequest):
    security_pair: SecurityPair


class PasswordEnrollmentRequest(ThreeDsEnrollmentRequest):
    password: str


class UpdateThreeDsEnrollmentRequest:
    security_pair: SecurityPair
    password: str
    locale: str
    phone_number: Phone


class CardCredentialsQuery:
    credentials: str


class RevokeRequest:
    reason: RevokeReason


class SuspendRequest:
    reason: SuspendReason
