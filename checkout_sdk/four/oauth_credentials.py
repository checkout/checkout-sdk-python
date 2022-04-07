from __future__ import absolute_import

import json
from abc import ABCMeta
from datetime import datetime, timedelta

import urllib3
from requests import HTTPError, Session, ConnectionError

from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.environment import Environment
from checkout_sdk.exception import CheckoutAuthorizationException, CheckoutArgumentException
from checkout_sdk.four.oauth_access_token import OAuthAccessToken
from checkout_sdk.platform_type import PlatformType
from checkout_sdk.sdk_authorization import SdkAuthorization
from checkout_sdk.sdk_credentials import SdkCredentials


class FourOAuthSdkCredentials(SdkCredentials, metaclass=ABCMeta):
    __access_token: OAuthAccessToken = None
    __http_client: Session
    __scopes: list

    def __init__(self,
                 http_client: Session,
                 environment: Environment,
                 client_id: str,
                 client_secret: str,
                 authorization_uri: str,
                 scopes: list):
        self.validate_arguments(environment, client_id, client_secret, authorization_uri)
        self.__http_client = http_client
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__authorization_uri = authorization_uri if authorization_uri else environment.authorization_uri
        self.__scopes = scopes

    @staticmethod
    def validate_arguments(environment: Environment, client_id: str, client_secret: str, authorization_uri: str):
        if not client_id or not client_secret:
            raise CheckoutArgumentException(
                "Invalid OAuth 'client_id' or 'client_secret'")
        if not environment and not authorization_uri:
            raise CheckoutArgumentException(
                "Invalid configuration. Please specify an 'environment' or a specific OAuth 'authorization_uri'")

    @staticmethod
    def init(http_client: Session, environment: Environment, client_id, client_secret, authorization_uri, scopes: list):
        credentials = FourOAuthSdkCredentials(http_client, environment, client_id, client_secret, authorization_uri,
                                              scopes)
        credentials.get_access_token()
        return credentials

    def get_authorization(self, authorization_type: AuthorizationType):
        if authorization_type in (
                AuthorizationType.SECRET_KEY_OR_OAUTH, AuthorizationType.PUBLIC_KEY_OR_OAUTH, AuthorizationType.OAUTH):
            return SdkAuthorization(PlatformType.FOUR_OAUTH, self.get_access_token().token)

        raise CheckoutAuthorizationException.invalid_authorization(authorization_type=authorization_type)

    def get_access_token(self):
        if self.__access_token is not None and self.__access_token.is_valid():
            return self.__access_token

        data = {
            'grant_type': 'client_credentials',
            'scope': str.join(' ', self.__scopes)
        }

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        try:
            response = self.__http_client.request(method='POST', url=self.__authorization_uri,
                                                  data=data, verify=False, allow_redirects=False,
                                                  auth=(self.__client_id, self.__client_secret))
            response.raise_for_status()
        except HTTPError as err:
            errors = json.loads(err.response.text)
            message = 'OAuth client_credentials authentication failed with error: ({})'.format(errors['error'])
            raise CheckoutAuthorizationException(message) from err
        except ConnectionError as err:
            raise CheckoutAuthorizationException(
                'Unable to establish connection to host: ({})'.format(self.__authorization_uri)) from err

        response_json = response.json()
        self.__access_token = OAuthAccessToken(token=response_json['access_token'],
                                               expiration_date=datetime.now() + timedelta(
                                                   seconds=response_json['expires_in']))
        return self.__access_token
