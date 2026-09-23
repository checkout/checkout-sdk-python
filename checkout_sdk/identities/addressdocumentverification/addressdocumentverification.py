from __future__ import absolute_import


class DeclaredData:
    """The personal details provided by the applicant.

    Maps IdvDeclaredData. The identity verification requests take the larger
    IdvIdentityDeclaredData shape and keep their own copy of this class.
    """
    # The applicant's name.
    # [Required]
    # min 2 characters, max 255 characters
    # Example: Hannah Bret
    name: str
    # The applicant's birth date.
    # [Optional]
    # Format: yyyy-MM-dd
    # Example: 1994-10-15
    birth_date: str


class AddressDocumentVerificationRequest:
    """Request body for POST /address-document-verifications."""
    # The applicant's unique identifier.
    # [Required]
    # ^aplt_\w+$
    applicant_id: str
    # Your configuration ID.
    # [Required]
    # ^usj_[a-z2-7]{26}$
    user_journey_id: str
    # The personal details provided by the applicant.
    # [Optional]
    declared_data: DeclaredData


class AddressDocumentVerificationAttemptRequest:
    """Request body for POST /address-document-verifications/{id}/attempts."""
    # The address document image to verify, as a binary upload.
    # [Required]
    # Format: binary
    document: str
