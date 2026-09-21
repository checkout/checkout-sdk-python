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
    # Format: YYYY-MM-DD
    # Example: 1994-10-15
    birth_date: str


class IdDocumentVerificationRequest:
    """Request body for POST /id-document-verifications."""
    # The applicant's unique identifier.
    # [Required]
    applicant_id: str
    # Your configuration ID.
    # [Optional]
    user_journey_id: str
    # The personal details provided by the applicant.
    # [Optional]
    declared_data: DeclaredData


class IdDocumentVerificationAttemptRequest:
    """Request body for POST /id-document-verifications/{id}/attempts."""
    # The front image of the identity document, as a binary upload.
    # [Required]
    # Format: binary
    document_front: str
    # The back image of the identity document, as a binary upload.
    # [Optional]
    # Format: binary
    document_back: str
