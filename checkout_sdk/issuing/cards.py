from enum import Enum
from typing import Dict

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


class ReturnCredentials(str, Enum):
    NUMBER = 'number'
    CVC2 = 'cvc2'


class CardLifetime:
    unit: LifetimeUnit
    value: int


class ShippingInstructions:
    # Deprecated: marked deprecated in the Checkout.com API swagger
    # (IssuingShippingInstruction.shipping_recipient). Do not set in new code.
    shipping_recipient: str
    shipping_address: Address
    # Deprecated: marked deprecated in the Checkout.com API swagger
    # (IssuingShippingInstruction.additional_comment). Do not set in new code.
    additional_comment: str


class CardMetadata:
    udf1: str
    udf2: str
    udf3: str
    udf4: str
    udf5: str


class CardRequest:
    type: CardType
    cardholder_id: str
    lifetime: CardLifetime
    reference: str
    card_product_id: str
    display_name: str
    activate_card: bool
    metadata: CardMetadata
    # Date scheduling the card's automatic revocation.
    # [Optional]
    # Format: date (YYYY-MM-DD, time is midnight UTC)
    # Example: 2027-03-12
    revocation_date: str
    # Date scheduling the card's first activation. Only applies to the initial activation of a
    # card. Two formats are supported: date only (YYYY-MM-DD, treated as midnight UTC), or date
    # with round hour (YYYY-MM-DDTHH:mmZ in UTC, or YYYY-MM-DDTHH:mm+HH:mm with offset). Only
    # round hours are allowed when a time is provided (HH:00). The value must be at least the
    # next round hour after the request time.
    # [Optional]
    # Example: 2026-06-01T10:00Z
    scheduled_activation_date: str

    def __init__(self, type_p: CardType):
        self.type = type_p


class PhysicalCardRequest(CardRequest):
    shipping_instructions: ShippingInstructions

    def __init__(self):
        super().__init__(CardType.PHYSICAL)


class VirtualCardRequest(CardRequest):
    is_single_use: bool
    return_credentials: list  # ReturnCredentials
    control_profiles: list  # str (IssuingControlProfileId)
    controls: list  # VirtualCardControlRequest

    def __init__(self):
        super().__init__(CardType.VIRTUAL)


class UpdateCardRequest:
    """Request body for PATCH /issuing/cards/{cardId}."""
    # Your reference.
    # [Optional]
    # max 256 characters
    # Example: X-123456-N11
    reference: str
    # User's metadata.
    # [Optional]
    metadata: CardMetadata
    # The card's expiration month.
    # [Optional]
    # Format: int32
    # min 1, max 12
    # Example: 5
    expiry_month: int
    # The card's expiration year.
    # [Optional]
    # Format: int32
    # min 4 characters, max 4 characters
    # Example: 2025
    expiry_year: int
    # Date scheduling the card's first activation. Only applies to the initial activation of a
    # card. Two formats are supported: date only (YYYY-MM-DD, treated as midnight UTC), or date
    # with round hour (YYYY-MM-DDTHH:mmZ in UTC, or YYYY-MM-DDTHH:mm+HH:mm with offset). Only
    # round hours are allowed when a time is provided (HH:00). The value must be at least the
    # next round hour after the request time.
    # [Optional]
    # Example: 2026-06-01T10:00Z
    scheduled_activation_date: str
    # Date scheduling the card's automatic revocation.
    # [Optional]
    # Format: date (YYYY-MM-DD, time is midnight UTC)
    # Example: 2027-03-12
    revocation_date: str


class CardUpdateHeaders:
    """The optional HTTP headers accepted when updating a card's details.

    Header values are stringified by ApiClient, so declare the boolean header as the string
    "true" rather than a Python bool: str(True) is "True", which is not the value the spec
    shows. All three existing header classes in this SDK use str for the same reason.
    """
    # Set to "true" to retrieve the card's encrypted credentials in the response. Requires an RSA
    # public key to be provided in the Encryption-Key header.
    # [Optional]
    # Maps to HTTP header return-encrypted-cvv.
    # Example: "true"
    return_encrypted_cvv: str
    # The RSA public key used to encrypt returned credentials. Required when the
    # return-encrypted-cvv header is set to "true". Provide the public key with the
    # BEGIN PUBLIC KEY and END PUBLIC KEY headers and any newline characters removed, encoded as
    # Base64.
    # [Optional]
    # Maps to HTTP header Encryption-Key.
    encryption_key: str

    def get_header_mappings(self) -> Dict[str, str]:
        return {
            'return_encrypted_cvv': 'return-encrypted-cvv',
            'encryption_key': 'Encryption-Key'
        }


class RenewCardRequest:
    display_name: str
    reference: str
    metadata: CardMetadata


class PhysicalCardRenewRequest(RenewCardRequest):
    shipping_instructions: ShippingInstructions


class VirtualCardRenewRequest(RenewCardRequest):
    pass


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
