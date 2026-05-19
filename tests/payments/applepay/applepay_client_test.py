import pytest

from tests._assertions import assert_api_call
from checkout_sdk.payments.applepay.applepay import UploadCertificateRequest, EnrollDomainRequest, \
    GenerateSigningRequestRequest
from checkout_sdk.payments.applepay.applepay_client import ApplePayClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return ApplePayClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestApplePayClient:

    def test_should_upload_payment_processing_certificate(self, mocker, client: ApplePayClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = UploadCertificateRequest()

        assert client.upload_payment_processing_certificate(body) == 'response'
        assert_api_call(mock, 'applepay/certificates', body)

    def test_should_enroll_domain(self, mocker, client: ApplePayClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = EnrollDomainRequest()

        assert client.enroll_domain(body) == 'response'
        assert_api_call(mock, 'applepay/enrollments', body)

    def test_should_generate_certificate_signing_request(self, mocker, client: ApplePayClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = GenerateSigningRequestRequest()

        assert client.generate_certificate_signing_request(body) == 'response'
        assert_api_call(mock, 'applepay/signing-requests', body)
