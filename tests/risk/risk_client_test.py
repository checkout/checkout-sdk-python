import pytest

from checkout_sdk.risk.risk import PreAuthenticationAssessmentRequest, PreCaptureAssessmentRequest
from checkout_sdk.risk.risk_client import RiskClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return RiskClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestRiskClient:

    def test_should_request_pre_authentication_risk_scan(self, mocker, client: RiskClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.request_pre_authentication_risk_scan(PreAuthenticationAssessmentRequest()) == 'response'

    def test_should_request_pre_capture_risk_scan(self, mocker, client: RiskClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.request_pre_capture_risk_scan(PreCaptureAssessmentRequest()) == 'response'
