from __future__ import absolute_import

from enum import Enum


class AccountType(str, Enum):
    SAVINGS = 'savings'
    CURRENT = 'current'
    CASH = 'cash'


class AccountHolderType(str, Enum):
    INDIVIDUAL = 'individual'
    CORPORATE = 'corporate'
    INSTRUMENT = 'instrument'


class AccountHolderIdentificationType(str, Enum):
    PASSPORT = 'passport'
    DRIVING_LICENSE = 'driving_licence'
    NATIONAL_ID = 'national_id'
    COMPANY_REGISTRATION = 'company_registration'
    TAX_ID = 'tax_id'
