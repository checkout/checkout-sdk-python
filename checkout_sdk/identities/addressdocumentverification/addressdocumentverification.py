from __future__ import absolute_import


class DeclaredData:
    name: str


class AddressDocumentVerificationRequest:
    applicant_id: str
    user_journey_id: str
    declared_data: DeclaredData


class AddressDocumentVerificationAttemptRequest:
    document: str
