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


class CardStatusUpdate(str, Enum):
    # Set on UpdateCardRequest.status to reactivate an inactive or suspended card.
    # Mutually exclusive with UpdateCardRequest.scheduled_activation_date.
    ACTIVE = 'active'


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
    """User's metadata."""
    # User defined field 1
    # [Optional]
    # Pattern: ^.{0,255}$
    # Example: metadata1
    udf1: str
    # User defined field 2
    # [Optional]
    # Pattern: ^.{0,255}$
    # Example: metadata2
    udf2: str
    # User defined field 3
    # [Optional]
    # Pattern: ^.{0,255}$
    # Example: metadata3
    udf3: str
    # User defined field 4
    # [Optional]
    # Pattern: ^.{0,255}$
    # Example: metadata4
    udf4: str
    # User defined field 5
    # [Optional]
    # Pattern: ^.{0,255}$
    # Example: metadata5
    udf5: str


class CardRequest:
    """Shared base for the card creation requests. The concrete type is chosen by the subclass,
    which sets the discriminator in its constructor."""
    # The card type.
    # [Required]
    # Enum: "virtual" "physical"
    # Example: virtual
    type: CardType
    # The cardholder's unique identifier.
    # [Required]
    # ^crh_[a-z0-9]{26}$
    # min 30 characters, max 30 characters
    # Example: crh_d3ozhf43pcq2xbldn2g45qnb44
    cardholder_id: str
    # The duration of time during which the card will accept incoming authorizations. The unit
    # and value combination determines the card's expiry date.
    # [Optional]
    lifetime: CardLifetime
    # Your reference.
    # [Optional]
    # max 256 characters
    # Example: X-123456-N11
    reference: str
    # The card product's unique identifier. Required if more than one card product is associated
    # with the entity.
    # [Required]
    card_product_id: str
    # The name to display on the card.
    # [Optional]
    # ^[0-9a-zA-Z.\- ]{2,26}$
    # min 2 characters, max 26 characters
    # Example: JOHN KENNEDY
    display_name: str
    # Sets whether to activate the newly created card upon creation. If false, the cardholder
    # cannot process transactions until you activate the card.
    # [Optional]
    # Default: true
    activate_card: bool
    # User's metadata.
    # [Optional]
    metadata: CardMetadata
    # Deprecated: use scheduled_revocation_date instead. If both are provided,
    # scheduled_revocation_date overrides this value.
    # [Optional]
    # Format: yyyy-MM-dd (time is midnight UTC)
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
    # The card will be revoked at midnight UTC on the date specified.
    # [Optional]
    # Format: date (YYYY-MM-DD)
    # Example: 2027-03-12
    scheduled_revocation_date: str

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
    # Set the card's status to active to activate an inactive or suspended card. If you submit
    # this field, you cannot specify a scheduled_activation_date. If you do, you receive a
    # scheduled_activation_date_conflicts_with_activation error.
    # [Optional]
    # Enum: active
    # Example: active
    status: CardStatusUpdate
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
    # Deprecated: use scheduled_revocation_date instead. If both are provided,
    # scheduled_revocation_date overrides this value.
    # [Optional]
    # Format: yyyy-MM-dd (time is midnight UTC)
    # Example: 2027-03-12
    revocation_date: str
    # The card will be revoked at midnight UTC on the date specified.
    # [Optional]
    # Format: date (YYYY-MM-DD)
    # Example: 2027-03-12
    scheduled_revocation_date: str


class CardUpdateHeaders:
    """The optional HTTP headers accepted when updating a card's details.

    Deprecated: The API no longer documents these headers; use the method without headers.
    Will be removed in the next major version. When set, they are still sent unchanged.

    Header values are stringified by ApiClient, so declare the boolean header as the string
    "true" rather than a Python bool: str(True) is "True", which is not the value the spec
    shows. All three existing header classes in this SDK use str for the same reason.
    """
    # Deprecated: no longer documented by the API. Still sent when set.
    # [Optional]
    # Maps to HTTP header return-encrypted-cvv.
    # Example: "true"
    return_encrypted_cvv: str
    # Deprecated: no longer documented by the API. Still sent when set.
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
    """Optional request body for POST /issuing/cards/{cardId}/revoke."""
    # The reason why the card is being revoked.
    # [Optional]
    # Enum: expired, reported_lost, reported_stolen
    reason: RevokeReason


class SuspendRequest:
    """Optional request body for POST /issuing/cards/{cardId}/suspend."""
    # The reason why the card is being suspended.
    # [Optional]
    # Enum: suspected_lost, suspected_stolen
    reason: SuspendReason
