import re
from urllib.parse import urlparse, urlunparse

from checkout_sdk.environment import Environment
from checkout_sdk.exception import CheckoutArgumentException


class EnvironmentSubdomain:
    def __init__(self, environment: Environment, subdomain: str):
        self.base_uri = self.create_url_with_subdomain(environment.base_uri, subdomain)
        self.authorization_uri = self.create_url_with_subdomain(environment.authorization_uri, subdomain)

    @staticmethod
    def create_url_with_subdomain(original_url: str, subdomain: str):
        """
        Applies subdomain transformation to any given URL, prepending the subdomain to the host.

        Args:
            original_url: the original URL to transform
            subdomain: the subdomain to prepend

        Returns:
            the transformed URL with subdomain

        Raises:
            CheckoutArgumentException: if the subdomain is not a valid merchant-specific subdomain
        """
        regex = r'(?:pl-)?[a-z0-9]+'
        if subdomain is None or not re.fullmatch(regex, subdomain):
            raise CheckoutArgumentException(
                'invalid environment subdomain - provide your merchant-specific subdomain, '
                'typically your client ID excluding the cli_ prefix (see '
                'https://api-reference.checkout.com/#section/Base-URLs)')

        url_parts = urlparse(original_url)
        if url_parts.port:
            new_host = subdomain + '.' + url_parts.hostname + ':' + str(url_parts.port)
        else:
            new_host = subdomain + '.' + url_parts.hostname

        new_url_parts = (
            url_parts.scheme,
            new_host,
            url_parts.path,
            url_parts.params,
            url_parts.query,
            url_parts.fragment
        )

        return urlunparse(new_url_parts)
