from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.identities.applicants.applicants import CreateApplicantRequest, UpdateApplicantRequest


class ApplicantsClient(Client):
    __APPLICANTS_PATH = 'applicants'
    __ANONYMIZE_PATH = 'anonymize'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def create_applicant(self, request: CreateApplicantRequest):
        return self._api_client.post(self.__APPLICANTS_PATH,
                                     self._sdk_authorization(),
                                     request)

    def get_applicant(self, applicant_id: str):
        return self._api_client.get(self.build_path(self.__APPLICANTS_PATH, applicant_id),
                                    self._sdk_authorization())

    def update_applicant(self, applicant_id: str, request: UpdateApplicantRequest):
        return self._api_client.patch(self.build_path(self.__APPLICANTS_PATH, applicant_id),
                                      self._sdk_authorization(),
                                      request)

    def anonymize_applicant(self, applicant_id: str):
        return self._api_client.post(
            self.build_path(self.__APPLICANTS_PATH, applicant_id, self.__ANONYMIZE_PATH),
            self._sdk_authorization())
