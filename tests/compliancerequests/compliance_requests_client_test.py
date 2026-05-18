import pytest

from tests._assertions import assert_api_call
from checkout_sdk.compliancerequests.compliance_requests_client import ComplianceRequestsClient
from checkout_sdk.compliancerequests.compliance_requests import ComplianceRequestRespondRequest


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return ComplianceRequestsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestComplianceRequestsClient:

    def test_get_compliance_request(self, mocker, client: ComplianceRequestsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_compliance_request('pay_fun26akvvjjerahhctaq2uzhu4') == 'response'
        assert_api_call(mock, 'compliance-requests/pay_fun26akvvjjerahhctaq2uzhu4')

    def test_get_compliance_request_with_none_payment_id(self, mocker, client: ComplianceRequestsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        with pytest.raises(TypeError, match="sequence item 1: expected str"):
            client.get_compliance_request(None)

    def test_respond_to_compliance_request(self, mocker, client: ComplianceRequestsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = ComplianceRequestRespondRequest()

        assert client.respond_to_compliance_request('pay_fun26akvvjjerahhctaq2uzhu4', body) == 'response'
        assert_api_call(mock, 'compliance-requests/pay_fun26akvvjjerahhctaq2uzhu4', body)

    def test_respond_to_compliance_request_with_none_payment_id(self, mocker, client: ComplianceRequestsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        with pytest.raises(TypeError, match="sequence item 1: expected str"):
            client.respond_to_compliance_request(None, ComplianceRequestRespondRequest())

    def test_respond_to_compliance_request_with_none_request(self, mocker, client: ComplianceRequestsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.respond_to_compliance_request('pay_fun26akvvjjerahhctaq2uzhu4', None) == 'response'
        # Body is None — verify path; helper's body=None skips body identity check.
        assert_api_call(mock, 'compliance-requests/pay_fun26akvvjjerahhctaq2uzhu4')
