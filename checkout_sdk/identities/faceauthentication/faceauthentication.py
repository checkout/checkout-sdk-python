from __future__ import absolute_import

from checkout_sdk.identities.entities import PhoneNumber


class ClientInformation:
    """The applicant's details for a face authentication attempt.

    Maps FavClientInformation. Deliberately smaller than the identity verification copy in
    checkout_sdk.identities.identityverification: the face authentication attempt schema does not
    declare pre_selected_document_issuing_country or pre_selected_document_type, so sending them
    here would be a request the API rejects.
    """
    # The applicant's residence country.
    # [Optional]
    # Standard: ISO 3166-1 alpha-2 country code
    # ^[A-Z]{2}
    # Example: FR
    pre_selected_residence_country: str
    # The language you want to use for the user interface.
    # [Optional]
    # Format: IETF BCP 47 language tag
    # Example: en-US
    pre_selected_language: str


class FaceAuthenticationRequest:
    """Request body for POST /face-authentications."""
    # The applicant's unique identifier.
    # [Required]
    applicant_id: str
    # Your configuration ID.
    # [Optional]
    user_journey_id: str


class FaceAuthenticationAttemptRequest:
    """Request body for POST /face-authentications/{id}/attempts."""
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
