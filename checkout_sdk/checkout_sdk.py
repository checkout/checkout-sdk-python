from __future__ import absolute_import

from checkout_sdk.default_sdk import DefaultSdk


class CheckoutSdk:

    @staticmethod
    def builder():
        return DefaultSdk()
