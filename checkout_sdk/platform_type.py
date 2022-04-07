from __future__ import absolute_import

from enum import Enum


class PlatformType(str, Enum):
    DEFAULT = 'DEFAULT'
    FOUR = 'FOUR'
    FOUR_OAUTH = 'FOUR_OAUTH'
    CUSTOM = 'CUSTOM'
