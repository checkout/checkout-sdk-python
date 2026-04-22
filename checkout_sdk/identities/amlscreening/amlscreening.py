from __future__ import absolute_import


class SearchParameters:
    configuration_identifier: str


class AmlScreeningRequest:
    applicant_id: str
    search_parameters: SearchParameters
    monitored: bool
