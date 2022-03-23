from __future__ import absolute_import

import json
from abc import ABCMeta
from datetime import datetime, timedelta

import urllib3
from requests import HTTPError, Session, ConnectionError

from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.exception import CheckoutAuthorizationException
from checkout_sdk.four.oauth_access_token import OAuthAccessToken
from checkout_sdk.platform_type import PlatformType
from checkout_sdk.sdk_authorization import SdkAuthorization
from checkout_sdk.sdk_credentials import SdkCredentials


class FourOAuthSdkCredentials(SdkCredentials, metaclass=ABCMeta):
    __access_token: OAuthAccessToken = None
    __http_client: Session
    __scopes: list

    def __init__(self, http_client: Session, client_id, client_secret, authorization_uri, scopes: list):
        self.__http_client = http_client
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__authorization_uri = authorization_uri
        self.__scopes = scopes

    @staticmethod
    def init(http_client: Session, client_id, client_secret, authorization_uri, scopes: list):
        credentials = FourOAuthSdkCredentials(http_client, client_id, client_secret, authorization_uri, scopes)
        credentials.get_access_token()
        return credentials

    def get_authorization(self, authorization_type: AuthorizationType):
        if AuthorizationType.SECRET_KEY_OR_OAUTH == authorization_type or \
                AuthorizationType.PUBLIC_KEY_OR_OAUTH == authorization_type or \
                AuthorizationType.OAUTH == authorization_type:
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
            message = 'OAuth client_credentials authentication failed with error: ({})'.format(errors["error"])
            raise CheckoutAuthorizationException(message)
        except ConnectionError:
            raise CheckoutAuthorizationException(
                'Unable to establish connection to host: ({})'.format(self.__authorization_uri))

        response_json = response.json()
        self.__access_token = OAuthAccessToken(token=response_json['access_token'],
                                               expiration_date=datetime.now() + timedelta(
                                                   seconds=response_json['expires_in']))
        return self.__access_token
