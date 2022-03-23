from __future__ import absolute_import

from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.exception import CheckoutAuthorizationException
from checkout_sdk.platform_type import PlatformType
from checkout_sdk.sdk_authorization import SdkAuthorization
from checkout_sdk.sdk_credentials import SdkCredentials


class SessionSecretSdkCredentials(SdkCredentials):

    def __init__(self, secret):
        self.secret = secret

    def get_authorization(self, authorization_type: AuthorizationType):
        if AuthorizationType.CUSTOM == authorization_type:
            if self.secret is None:
                raise CheckoutAuthorizationException.invalid_key(AuthorizationType.CUSTOM)
            return SdkAuthorization(PlatformType.CUSTOM, self.secret)
        raise CheckoutAuthorizationException.invalid_authorization(authorization_type=authorization_type)
