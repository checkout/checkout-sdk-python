from __future__ import absolute_import


class DeclaredData:
    name: str


class ClientInformation:
    pre_selected_residence_country: str
    pre_selected_language: str


class IdentityVerificationRequest:
    applicant_id: str
    declared_data: DeclaredData
    user_journey_id: str


class IdentityVerificationAndAttemptRequest:
    declared_data: DeclaredData
    redirect_url: str
    user_journey_id: str
    applicant_id: str


class IdentityVerificationAttemptRequest:
    redirect_url: str
    client_information: ClientInformation
