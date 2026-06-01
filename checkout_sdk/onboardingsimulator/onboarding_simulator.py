from __future__ import absolute_import

from enum import Enum


class SimulatorEntityStatus(str, Enum):
    DRAFT = 'draft'
    REQUIREMENTS_DUE = 'requirements_due'
    PENDING = 'pending'
    ACTIVE = 'active'
    RESTRICTED = 'restricted'
    REJECTED = 'rejected'
    INACTIVE = 'inactive'


class SimulatorSetRequirementsDueRequest:
    fields: list  # list of str


class SimulatorSetStatusRequest:
    status: SimulatorEntityStatus
