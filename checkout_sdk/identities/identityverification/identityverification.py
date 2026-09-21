from __future__ import absolute_import

from checkout_sdk.identities.entities import IdvAddress, PhoneNumber


class DeclaredData:
    """The personal details provided by the applicant for an identity verification.

    Maps IdvIdentityDeclaredData, which is the shape the identity verification requests accept.
    The address document and ID document verification requests take the smaller IdvDeclaredData
    shape instead, and keep their own copies of this class.
    """
    # The applicant's name.
    # [Required]
    # min 2 characters, max 255 characters
    # Example: Hannah Bret
    name: str
    # The applicant's birth date.
    # [Optional]
    # Format: YYYY-MM-DD
    # Example: 1994-10-15
    birth_date: str
    # The applicant's mobile phone number, if sharing the attempt URL via SMS.
    # [Optional]
    phone_number: PhoneNumber
    # The applicant's email address. Explicitly nullable in the spec, so the API may return null
    # for it rather than omitting it.
    # [Optional]
    # Format: email
    # Nullable: true
    # Example: hannah.bret@example.com
    email: str
    # The applicant's address.
    # [Optional]
    address: IdvAddress


class ClientInformation:
    """The applicant's details for an identity verification attempt.

    Maps IdvClientInformation. The face authentication attempt takes the smaller
    FavClientInformation shape and keeps its own copy of this class, so the two document fields
    below cannot leak onto a face authentication request.
    """
    # The applicant's residence country.
    # [Optional]
    # Standard: ISO 3166-1 alpha-2 country code
    # ^[A-Z]{2}
    # Example: FR
    pre_selected_residence_country: str
    # The country that issued the applicant's identity document.
    # [Optional]
    # Standard: ISO 3166-1 alpha-2 country code
    # ^[A-Z]{2}
    # Example: FR
    pre_selected_document_issuing_country: str
    # The type of identity document the applicant uses for the attempt.
    # [Optional]
    # Enum: "Driving licence" "ID" "Other" "Passport" "Residence Permit" "Travel Document" "Visa"
    pre_selected_document_type: str
    # The language you want to use for the user interface.
    # [Optional]
    # Format: IETF BCP 47 language tag
    # Example: en-US
    pre_selected_language: str


class IdentityVerificationRequest:
    """Request body for POST /identity-verifications."""
    # The applicant's unique identifier.
    # [Required]
    applicant_id: str
    # The personal details provided by the applicant.
    # [Required]
    declared_data: DeclaredData
    # Your configuration ID.
    # [Optional]
    user_journey_id: str


class IdentityVerificationAndAttemptRequest:
    """Request body for POST /create-and-open-idv."""
    # The personal details provided by the applicant.
    # [Required]
    declared_data: DeclaredData
    # The URL to redirect the applicant to after the attempt.
    # [Required]
    # Format: uri
    redirect_url: str
    # Your configuration ID.
    # [Optional]
    user_journey_id: str
    # The applicant's unique identifier.
    # [Optional]
    applicant_id: str


class IdentityVerificationAttemptRequest:
    """Request body for POST /identity-verifications/{id}/attempts."""
    # The URL to redirect the applicant to after the attempt.
    # [Required]
    # Format: uri
    redirect_url: str
    # The applicant's mobile phone number, if sharing the attempt URL via SMS.
    # [Optional]
    phone_number: PhoneNumber
    # The applicant's details.
    # [Optional]
    client_information: ClientInformation
