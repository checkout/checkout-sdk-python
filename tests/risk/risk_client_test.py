import pytest

from tests._assertions import assert_api_call
from checkout_sdk.risk.risk import PreAuthenticationAssessmentRequest, PreCaptureAssessmentRequest
from checkout_sdk.risk.risk_client import RiskClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return RiskClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestRiskClient:

    def test_should_request_pre_authentication_risk_scan(self, mocker, client: RiskClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = PreAuthenticationAssessmentRequest()

        assert client.request_pre_authentication_risk_scan(body) == 'response'
        assert_api_call(mock, 'risk/assessments/pre-authentication', body)

    def test_should_request_pre_capture_risk_scan(self, mocker, client: RiskClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = PreCaptureAssessmentRequest()

        assert client.request_pre_capture_risk_scan(body) == 'response'
        assert_api_call(mock, 'risk/assessments/pre-capture', body)
