from __future__ import absolute_import

from enum import Enum


class AuthorizationType(Enum):
    PUBLIC_KEY = 'PUBLIC_KEY'
    SECRET_KEY = 'SECRET_KEY'
    PUBLIC_KEY_OR_OAUTH = 'PUBLIC_KEY_OR_OAUTH'
    SECRET_KEY_OR_OAUTH = 'SECRET_KEY_OR_OAUTH'
    OAUTH = 'OAUTH'
    CUSTOM = 'CUSTOM'
