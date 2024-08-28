import re
from urllib.parse import urlparse, urlunparse

from checkout_sdk.environment import Environment


class EnvironmentSubdomain:
    def __init__(self, environment: Environment, subdomain: str):
        self.base_uri = self.add_subdomain_to_api_url_environment(environment, subdomain)

    @staticmethod
    def add_subdomain_to_api_url_environment(environment: Environment, subdomain: str):
        api_url = environment.base_uri
        new_environment = api_url

        regex = r'^[0-9a-z]+$'
        if re.match(regex, subdomain):
            url_parts = urlparse(api_url)
            if url_parts.port:
                new_host = subdomain + '.' + url_parts.hostname + ':' + url_parts.port
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
