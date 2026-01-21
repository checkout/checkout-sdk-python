import re
from urllib.parse import urlparse, urlunparse

from checkout_sdk.environment import Environment


class EnvironmentSubdomain:
    def __init__(self, environment: Environment, subdomain: str):
        self.base_uri = self.create_url_with_subdomain(environment.base_uri, subdomain)
        self.authorization_uri = self.create_url_with_subdomain(environment.authorization_uri, subdomain)

    @staticmethod
    def create_url_with_subdomain(original_url: str, subdomain: str):
        """
        Applies subdomain transformation to any given URL.
        If the subdomain is valid (alphanumeric pattern), prepends it to the host.
        Otherwise, returns the original URL unchanged.
        
        Args:
            original_url: the original URL to transform
            subdomain: the subdomain to prepend
            
        Returns:
            the transformed URL with subdomain, or original URL if subdomain is invalid
        """
        new_environment = original_url

        regex = r'^[0-9a-z]+$'
        if re.match(regex, subdomain):
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

            new_environment = urlunparse(new_url_parts)

        return new_environment

    def base_uri(self) -> str:
        return self.base_uri
