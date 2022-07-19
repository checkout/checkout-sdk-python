from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.apm.ideal_client import IdealClient
from checkout_sdk.checkout_configuration import CheckoutConfiguration


class CheckoutApmApi:

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        self.ideal = IdealClient(api_client=api_client, configuration=configuration)
