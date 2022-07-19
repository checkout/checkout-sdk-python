from __future__ import absolute_import

from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.exception import CheckoutAuthorizationException
from checkout_sdk.platform_type import PlatformType
from checkout_sdk.sdk_authorization import SdkAuthorization
from checkout_sdk.sdk_credentials import SdkCredentials


class DefaultKeysSdkCredentials(SdkCredentials):

    def __init__(self, secret_key, public_key=None):
        self.secret_key = secret_key
        self.public_key = public_key

    def get_authorization(self, authorization_type: AuthorizationType):

        if authorization_type in (AuthorizationType.SECRET_KEY, AuthorizationType.SECRET_KEY_OR_OAUTH):
            if self.secret_key is None:
                raise CheckoutAuthorizationException.invalid_key(AuthorizationType.SECRET_KEY)
            return SdkAuthorization(PlatformType.DEFAULT, self.secret_key)

        if authorization_type in (AuthorizationType.PUBLIC_KEY, AuthorizationType.PUBLIC_KEY_OR_OAUTH):
            if self.public_key is None:
                raise CheckoutAuthorizationException.invalid_key(AuthorizationType.PUBLIC_KEY)
            return SdkAuthorization(PlatformType.DEFAULT, self.public_key)

        raise CheckoutAuthorizationException.invalid_authorization(authorization_type=authorization_type)
