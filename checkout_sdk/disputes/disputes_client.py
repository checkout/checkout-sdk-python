from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.disputes.disputes import DisputesQueryFilter, DisputeEvidenceRequest
from checkout_sdk.files.files_client import FilesClient


class DisputesClient(FilesClient):
    __DISPUTES_PATH = 'disputes'
    __ACCEPT_PATH = 'accept'
    __EVIDENCE_PATH = 'evidence'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY)

    def query(self, query: DisputesQueryFilter):
        return self._api_client.get(self.__DISPUTES_PATH, self._sdk_authorization(),
                                    query)

    def get_dispute_details(self, dispute_id: str):
        return self._api_client.get(self.build_path(self.__DISPUTES_PATH, dispute_id), self._sdk_authorization())

    def accept(self, dispute_id: str):
        return self._api_client.post(self.build_path(self.__DISPUTES_PATH, dispute_id, self.__ACCEPT_PATH),
                                     self._sdk_authorization())

    def put_evidence(self, dispute_id: str, dispute_evidence_request: DisputeEvidenceRequest):
        return self._api_client.put(self.build_path(self.__DISPUTES_PATH, dispute_id, self.__EVIDENCE_PATH),
                                    self._sdk_authorization(), dispute_evidence_request)

    def get_evidence(self, dispute_id: str):
        return self._api_client.get(self.build_path(self.__DISPUTES_PATH, dispute_id, self.__EVIDENCE_PATH),
                                    self._sdk_authorization())

    def submit_evidence(self, dispute_id: str):
        return self._api_client.post(self.build_path(self.__DISPUTES_PATH, dispute_id, self.__EVIDENCE_PATH),
                                     self._sdk_authorization())
