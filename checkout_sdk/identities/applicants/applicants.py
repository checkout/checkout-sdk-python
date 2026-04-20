from __future__ import absolute_import


class CreateApplicantRequest:
    external_applicant_id: str
    email: str
    external_applicant_name: str


class UpdateApplicantRequest:
    email: str
    external_applicant_name: str
