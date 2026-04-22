from __future__ import absolute_import

from typing import List


class ComplianceRespondedField:
    name: str
    value: str
    not_available: bool


class ComplianceRespondedFields:
    sender: List[ComplianceRespondedField]
    recipient: List[ComplianceRespondedField]


class ComplianceRequestRespondRequest:
    fields: ComplianceRespondedFields
    comments: str
