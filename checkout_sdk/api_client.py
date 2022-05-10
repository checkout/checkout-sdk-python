from __future__ import absolute_import

import json
import logging
import mimetypes
from pathlib import Path

from requests.exceptions import HTTPError

from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.checkout_response import ResponseWrapper
from checkout_sdk.exception import CheckoutApiException, CheckoutException
from checkout_sdk.files.files import FileRequest
from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.properties import VERSION
from checkout_sdk.sdk_authorization import SdkAuthorization
from checkout_sdk.utils import map_to_http_metadata


def get_file_request(file_request: FileRequest, multipart_file=None):
    key_file = 'file' if multipart_file is None else multipart_file
    file_name = Path(file_request.file).name
    mime_type = mimetypes.MimeTypes().guess_type(file_name)[0]
    files = {key_file: (file_name, open(file_request.file, 'rb'), mime_type)}
    json_body = [('purpose', file_request.purpose)]
    return files, json_body


class ApiClient:
    _logger = logging.getLogger('checkout')

    def __init__(self, configuration: CheckoutConfiguration, base_uri: str):
        self._http_client = configuration.http_client
        self._base_uri = base_uri

    def get(self,
            path,
            authorization: SdkAuthorization,
            params=None):
        return self.invoke(method='GET', path=path, authorization=authorization, params=params)

    def post(self,
             path,
             authorization: SdkAuthorization,
             request=None,
             idempotency_key: str = None):
        return self.invoke(method='POST', path=path, authorization=authorization, body=request,
                           idempotency_key=idempotency_key)

    def put(self,
            path,
            authorization: SdkAuthorization,
            request=None):
        return self.invoke(method='PUT', path=path, authorization=authorization, body=request)

    def patch(self,
              path,
              authorization: SdkAuthorization,
              request=None):
        return self.invoke(method='PATCH', path=path, authorization=authorization, body=request)

    def delete(self,
               path,
               authorization: SdkAuthorization):
        return self.invoke(method='DELETE', path=path, authorization=authorization)

    def submit_file(self,
                    path,
                    authorization: SdkAuthorization,
                    file_request: FileRequest,
                    multipart_file=None):
        return self.invoke(method='POST', path=path, authorization=authorization, file_request=file_request,
                           multipart_file=multipart_file)

    def invoke(self,
               method: str,
               path: str,
               authorization: SdkAuthorization,
               body=None,
               idempotency_key: str = None,
               params=None,
               file_request: FileRequest = None,
               multipart_file=None):

        headers = {
            'User-Agent': 'checkout-sdk-python/' + VERSION,
            'Accept': 'application/json',
            'Authorization': authorization.get_authorization_header(),
            'Content-Type': 'application/json'}

        if idempotency_key is not None:
            headers['Cko-Idempotency-Key'] = idempotency_key

        base_uri = self._base_uri + path

        try:
            json_body = None
            params_dict = None
            files = None

            if body is not None:
                json_body = json.dumps(body, cls=JsonSerializer)
            elif params is not None:
                params_dict = json.loads(json.dumps(params, cls=JsonSerializer))
            elif file_request is not None:
                headers.pop('Content-Type')
                files, json_body = get_file_request(file_request, multipart_file)

            self._logger.info(method + ' ' + path)

            response = self._http_client.request(method=method,
                                                 url=base_uri,
                                                 headers=headers,
                                                 params=params_dict,
                                                 data=json_body,
                                                 files=files)

            response.raise_for_status()
        except HTTPError as err:
            self._logger.error(err)
            raise CheckoutApiException(err.response) from err
        except OSError as err:
            error = err.strerror
            raise CheckoutException(error) from err

        http_metadata = map_to_http_metadata(response)
        if response.text:
            return ResponseWrapper(http_metadata, response.json())
        else:
            return ResponseWrapper(http_metadata)
