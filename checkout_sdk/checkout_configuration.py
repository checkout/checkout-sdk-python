from __future__ import absolute_import

from typing import Optional

from requests import Session

from checkout_sdk.environment import Environment
from checkout_sdk.environment_subdomain import EnvironmentSubdomain
from checkout_sdk.sdk_credentials import SdkCredentials


class CheckoutConfiguration:

    def __init__(self,
                 credentials: SdkCredentials,
                 environment: Environment,
                 http_client: Session,
                 environment_subdomain: Optional[EnvironmentSubdomain] = None):
        self.credentials = credentials
        self.environment = environment
        self.http_client = http_client
        self.environment_subdomain = environment_subdomain
