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
             idempotency_key: str = None,
             headers=None):
        return self.invoke(method='POST', path=path, authorization=authorization, body=request,
                           idempotency_key=idempotency_key, headers=headers)

    def put(self,
            path,
            authorization: SdkAuthorization,
            request=None,
            headers=None):
        return self.invoke(method='PUT', path=path, authorization=authorization, body=request, headers=headers)

    def patch(self,
              path,
              authorization: SdkAuthorization,
              request=None,
              headers=None):
        return self.invoke(method='PATCH', path=path, authorization=authorization, body=request, headers=headers)

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
               multipart_file=None,
               headers=None):

        request_headers = {
            'User-Agent': 'checkout-sdk-python/' + VERSION,
            'Accept': 'application/json',
            'Authorization': authorization.get_authorization_header(),
            'Content-Type': 'application/json'}

        if idempotency_key is not None:
            request_headers['Cko-Idempotency-Key'] = idempotency_key

        if headers is not None:
            custom_headers = self._process_custom_headers(headers)
            request_headers.update(custom_headers)

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
                request_headers.pop('Content-Type')
                files, json_body = get_file_request(file_request, multipart_file)

            self._logger.info(method + ' ' + path)

            response = self._http_client.request(method=method,
                                                 url=base_uri,
                                                 headers=request_headers,
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
            if response.headers.get('Content-Type').startswith('application/json'):
                contents = response.json()
            else:
                contents = response.text
            return ResponseWrapper(http_metadata, contents)
        else:
            return ResponseWrapper(http_metadata)
        
    def _process_custom_headers(self, custom_headers):        
        # Trivial case
        if custom_headers is None:
            return None
        
        # Get custom mappings if the class defines them, otherwise use empty dict
        headers = {}
        custom_mappings = {}
        if hasattr(custom_headers, 'get_header_mappings'):
            custom_mappings = custom_headers.get_header_mappings()
        
        # Iterate through all attributes
        for attr_name in dir(custom_headers):
            # Skip private attributes and methods
            if attr_name.startswith('_') or callable(getattr(custom_headers, attr_name)):
                continue
                
            value = getattr(custom_headers, attr_name)
            if value is not None and value != '':
                # Use custom mapping if available, otherwise convert using default logic
                header_name = custom_mappings.get(attr_name, self._convert_property_to_header(attr_name))
                headers[header_name] = str(value)
        
        return headers
    
    def _convert_property_to_header(self, property_name):
        # Convert snake_case to Title-Case (e.g., 'api_version' -> 'Api-Version')
        return '-'.join(word.capitalize() for word in property_name.split('_'))

