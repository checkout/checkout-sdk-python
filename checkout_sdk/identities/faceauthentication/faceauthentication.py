from __future__ import absolute_import


class ClientInformation:
    pre_selected_residence_country: str
    pre_selected_language: str


class FaceAuthenticationRequest:
    applicant_id: str
    user_journey_id: str


class FaceAuthenticationAttemptRequest:
    redirect_url: str
    client_information: ClientInformation
