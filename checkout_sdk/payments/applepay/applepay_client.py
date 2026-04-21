from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.payments.applepay.applepay import UploadCertificateRequest, EnrollDomainRequest, \
    GenerateSigningRequestRequest


class ApplePayClient(Client):
    __CERTIFICATES_PATH = 'applepay/certificates'
    __ENROLLMENTS_PATH = 'applepay/enrollments'
    __SIGNING_REQUESTS_PATH = 'applepay/signing-requests'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def upload_payment_processing_certificate(self, request: UploadCertificateRequest):
        return self._api_client.post(self.__CERTIFICATES_PATH, self._sdk_authorization(), request)

    def enroll_domain(self, request: EnrollDomainRequest):
        return self._api_client.post(self.__ENROLLMENTS_PATH,
                                     self._sdk_authorization(AuthorizationType.OAUTH),
                                     request)

    def generate_certificate_signing_request(self, request: GenerateSigningRequestRequest):
        return self._api_client.post(self.__SIGNING_REQUESTS_PATH, self._sdk_authorization(), request)
