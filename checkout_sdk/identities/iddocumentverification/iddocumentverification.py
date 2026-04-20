from __future__ import absolute_import


class DeclaredData:
    name: str


class IdDocumentVerificationRequest:
    applicant_id: str
    user_journey_id: str
    declared_data: DeclaredData


class IdDocumentVerificationAttemptRequest:
    document_front: str
    document_back: str
