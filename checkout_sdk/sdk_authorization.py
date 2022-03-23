from __future__ import absolute_import

from checkout_sdk.exception import CheckoutAuthorizationException
from checkout_sdk.platform_type import PlatformType


class SdkAuthorization:

    def __init__(self, platform_type, credential):
        self.platform_type = platform_type
        self.credential = credential

    def get_authorization_header(self):
        if PlatformType.DEFAULT == self.platform_type or \
                PlatformType.CUSTOM == self.platform_type:
            return self.credential
        if PlatformType.FOUR == self.platform_type or \
                PlatformType.FOUR_OAUTH == self.platform_type:
            return 'Bearer ' + self.credential
        raise CheckoutAuthorizationException("Invalid platform type")
