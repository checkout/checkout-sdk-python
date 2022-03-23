from __future__ import absolute_import

from abc import abstractmethod

from checkout_sdk.authorization_type import AuthorizationType


class SdkCredentials:

    @abstractmethod
    def get_authorization(self, authorization_type: AuthorizationType):
        pass
