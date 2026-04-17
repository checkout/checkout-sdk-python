from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.compliancerequests.compliance_requests import ComplianceRequestRespondRequest


class ComplianceRequestsClient(Client):
    __COMPLIANCE_REQUESTS_PATH = 'compliance-requests'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def get_compliance_request(self, payment_id: str):
        return self._api_client.get(self.build_path(self.__COMPLIANCE_REQUESTS_PATH, payment_id), 
                                  self._sdk_authorization())

    def respond_to_compliance_request(self, payment_id: str, request: ComplianceRequestRespondRequest):
        return self._api_client.post(self.build_path(self.__COMPLIANCE_REQUESTS_PATH, payment_id),
                                   self._sdk_authorization(), request)