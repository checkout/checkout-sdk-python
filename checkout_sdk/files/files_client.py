from __future__ import absolute_import

from checkout_sdk.client import Client
from checkout_sdk.files.files import FileRequest


class FilesClient(Client):
    __FILES_PATH = 'files'

    def upload_file(self, file_request: FileRequest):
        return self._api_client.submit_file(self.__FILES_PATH, self._sdk_authorization(), file_request)

    def get_file_details(self, file_id: str):
        return self._api_client.get(self.build_path(self.__FILES_PATH, file_id), self._sdk_authorization())
