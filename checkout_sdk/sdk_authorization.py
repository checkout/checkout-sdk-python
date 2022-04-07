from __future__ import absolute_import

from checkout_sdk.exception import CheckoutAuthorizationException
from checkout_sdk.platform_type import PlatformType


class SdkAuthorization:

    def __init__(self, platform_type, credential):
        self.platform_type = platform_type
        self.credential = credential

    def get_authorization_header(self):
        if self.platform_type in (PlatformType.DEFAULT, PlatformType.CUSTOM):
            return self.credential
        if self.platform_type in (PlatformType.FOUR, PlatformType.FOUR_OAUTH):
            return 'Bearer ' + self.credential
        raise CheckoutAuthorizationException('Invalid platform type')
