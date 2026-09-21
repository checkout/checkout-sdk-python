from __future__ import absolute_import


class AttemptsQueryFilter:
    """Pagination for the list-attempts endpoints."""
    # The number of attempts to skip.
    # [Optional]
    # Default: 0
    skip: int
    # The maximum number of attempts to return.
    # [Optional]
    # Default: 10
    limit: int


class AttemptAssetsQueryFilter:
    """Pagination for the attempt-assets endpoints."""
    # The number of assets to skip.
    # [Optional]
    # Default: 0
    skip: int
    # The maximum number of assets to return.
    # [Optional]
    # Default: 10
    limit: int


class PhoneNumber:
    """The applicant's mobile phone number, if sharing the attempt URL via SMS."""
    # The international phone country code. This is a dialling prefix, not an ISO country code.
    # [Required]
    # ^\+(\d+)$
    # Example: +33
    country_code: str
    # The applicant's mobile number, without the country code.
    # [Required]
    # ^\d{1,14}$
    # Example: 5555550102
    number: str


class IdvAddress:
    """The applicant's address."""
    # The first line of the address.
    # [Optional]
    # max 250 characters
    # Example: 123 Main Street
    address_line1: str
    # The second line of the address.
    # [Optional]
    # max 250 characters
    # Example: Apt 4B
    address_line2: str
    # The city or town.
    # [Optional]
    # max 50 characters
    # Example: London
    city: str
    # The state, county, or province.
    # [Optional]
    # max 50 characters
    # Example: Greater London
    state: str
    # The postal or ZIP code.
    # [Optional]
    # max 50 characters
    # Example: SW1A 1AA
    zip: str
    # The two-letter ISO country code of the address.
    # [Optional]
    # Standard: ISO 3166-1 alpha-2 country code
    # max 2 characters
    # Example: GB
    country: str
