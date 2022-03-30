from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.risk.risk import PreAuthenticationAssessmentRequest, PreCaptureAssessmentRequest


class RiskClient(Client):
    __PRE_AUTHENTICATION_PATH = 'risk/assessments/pre-authentication'
    __PRE_CAPTURE_PATH = 'risk/assessments/pre-capture'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY)

    def request_pre_authentication_risk_scan(self,
                                             pre_authentication_assessment_request: PreAuthenticationAssessmentRequest):
        return self._api_client.post(self.__PRE_AUTHENTICATION_PATH, self._sdk_authorization(),
                                     pre_authentication_assessment_request)

    def request_pre_capture_risk_scan(self, pre_capture_assessment_request: PreCaptureAssessmentRequest):
        return self._api_client.post(self.__PRE_CAPTURE_PATH, self._sdk_authorization(), pre_capture_assessment_request)
