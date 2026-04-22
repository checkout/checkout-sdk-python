from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.payments.googlepay.googlepay import GooglePayEnrollmentRequest, GooglePayRegisterDomainRequest


class GooglePayClient(Client):
    __GOOGLEPAY_ENROLLMENTS_PATH = 'googlepay/enrollments'
    __DOMAIN_PATH = 'domain'
    __DOMAINS_PATH = 'domains'
    __STATE_PATH = 'state'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.OAUTH)

    def create_enrollment(self, request: GooglePayEnrollmentRequest):
        return self._api_client.post(self.__GOOGLEPAY_ENROLLMENTS_PATH, self._sdk_authorization(), request)

    def register_domain(self, entity_id: str, request: GooglePayRegisterDomainRequest):
        return self._api_client.post(
            self.build_path(self.__GOOGLEPAY_ENROLLMENTS_PATH, entity_id, self.__DOMAIN_PATH),
            self._sdk_authorization(),
            request)

    def get_registered_domains(self, entity_id: str):
        return self._api_client.get(
            self.build_path(self.__GOOGLEPAY_ENROLLMENTS_PATH, entity_id, self.__DOMAINS_PATH),
            self._sdk_authorization())

    def get_enrollment_state(self, entity_id: str):
        return self._api_client.get(
            self.build_path(self.__GOOGLEPAY_ENROLLMENTS_PATH, entity_id, self.__STATE_PATH),
            self._sdk_authorization())
