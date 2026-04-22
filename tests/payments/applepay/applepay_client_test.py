import pytest

from checkout_sdk.payments.applepay.applepay import UploadCertificateRequest, EnrollDomainRequest, \
    GenerateSigningRequestRequest
from checkout_sdk.payments.applepay.applepay_client import ApplePayClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return ApplePayClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


# tests

class TestApplePayClient:

    def test_should_upload_payment_processing_certificate(self, mocker, client: ApplePayClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.upload_payment_processing_certificate(UploadCertificateRequest()) == 'response'

    def test_should_enroll_domain(self, mocker, client: ApplePayClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.enroll_domain(EnrollDomainRequest()) == 'response'

    def test_should_generate_certificate_signing_request(self, mocker, client: ApplePayClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.generate_certificate_signing_request(GenerateSigningRequestRequest()) == 'response'
