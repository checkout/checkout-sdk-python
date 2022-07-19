from __future__ import absolute_import

from enum import Enum


class PlatformType(str, Enum):
    PREVIOUS = 'PREVIOUS'
    DEFAULT = 'DEFAULT'
    OAUTH = 'OAUTH'
    CUSTOM = 'CUSTOM'
