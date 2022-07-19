from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.apm.ideal_client import IdealClient
from checkout_sdk.apm.klarna_client import KlarnaClient
from checkout_sdk.apm.sepa_client import SepaClient
from checkout_sdk.checkout_configuration import CheckoutConfiguration


class CheckoutApmApi:

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        self.ideal = IdealClient(api_client=api_client, configuration=configuration)
        self.klarna = KlarnaClient(api_client=api_client, configuration=configuration)
        self.sepa = SepaClient(api_client=api_client, configuration=configuration)
