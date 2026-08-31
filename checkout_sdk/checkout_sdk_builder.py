from __future__ import absolute_import

import warnings
from typing import Optional

from checkout_sdk.default_http_client import DefaultHttpClientBuilder
from checkout_sdk.environment import Environment
from checkout_sdk.environment_subdomain import EnvironmentSubdomain
from checkout_sdk.exception import CheckoutArgumentException
from checkout_sdk.http_client_interface import HttpClientBuilderInterface


class CheckoutSdkBuilder:

    def __init__(self):
        self._environment = Environment.sandbox()
        self._subdomain = None
        self._use_legacy_domain = False
        self._http_client = DefaultHttpClientBuilder().get_client()

    def environment(self, environment: Environment):
        self._environment = environment
        return self

    def environment_subdomain(self, subdomain: Optional[str]):
        self._subdomain = subdomain
        return self

    def use_legacy_domain(self):
        """
        Opts out of the merchant-specific subdomain, sending every request to the shared hosts
        instead (api.checkout.com and access.checkout.com, or their sandbox equivalents).

        Deprecated: this is an emergency fallback for the rare case where the merchant-specific
        subdomain cannot be used, and will be removed in a future release. Call
        environment_subdomain() instead.
        See https://api-reference.checkout.com/#section/Base-URLs
        """
        warnings.warn(
            'use_legacy_domain() is deprecated and will be removed in a future release. It is '
            'intended only as an emergency fallback when the merchant-specific subdomain cannot '
            'be used. Call environment_subdomain() instead. See '
            'https://api-reference.checkout.com/#section/Base-URLs',
            DeprecationWarning,
            stacklevel=2)
        self._use_legacy_domain = True
        return self

    def http_client_builder(self, http_client_builder: HttpClientBuilderInterface):
        self._http_client = http_client_builder.get_client()
        return self

    @property
    def _environment_subdomain(self) -> Optional[EnvironmentSubdomain]:
        if self._subdomain is None:
            return None
        return EnvironmentSubdomain(self._environment, self._subdomain)

    def _requires_environment_subdomain(self) -> bool:
        """
        Whether this builder requires the merchant-specific subdomain to be configured. The
        Previous (ABC) platform predates merchant-specific subdomains, so it overrides this to
        False.
        """
        return True

    def _validate_environment_settings(self):
        if self._subdomain is not None and self._use_legacy_domain:
            raise CheckoutArgumentException(
                'environment_subdomain and use_legacy_domain cannot both be set - provide only '
                'your merchant-specific subdomain')
        if self._subdomain is None and not self._use_legacy_domain and self._requires_environment_subdomain():
            raise CheckoutArgumentException(
                'environment_subdomain is required - provide your merchant-specific subdomain '
                '(typically your client ID excluding the cli_ prefix, see '
                'https://api-reference.checkout.com/#section/Base-URLs), or call '
                'use_legacy_domain() to opt out only if merchant specific sub domains are '
                'causing issues')

    def build(self):
        raise NotImplementedError()
