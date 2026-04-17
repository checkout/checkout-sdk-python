import pytest

from checkout_sdk.compliancerequests.compliance_requests_client import ComplianceRequestsClient
from checkout_sdk.compliancerequests.compliance_requests import ComplianceRequestRespondRequest


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return ComplianceRequestsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestComplianceRequestsClient:

    def test_get_compliance_request(self, mocker, client: ComplianceRequestsClient):
        mock_get = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        payment_id = "pay_fun26akvvjjerahhctaq2uzhu4"
        
        response = client.get_compliance_request(payment_id)
        
        assert response == 'response'
        # Verify the correct endpoint path was called
        mock_get.assert_called_once()
        args = mock_get.call_args[0]
        assert f'compliance-requests/{payment_id}' in args[0]  # Path argument

    def test_get_compliance_request_with_none_payment_id(self, mocker, client: ComplianceRequestsClient):
        mock_get = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        
        with pytest.raises(TypeError, match="sequence item 1: expected str instance, NoneType found"):
            client.get_compliance_request(None)

    def test_respond_to_compliance_request(self, mocker, client: ComplianceRequestsClient):
        mock_post = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        payment_id = "pay_fun26akvvjjerahhctaq2uzhu4"
        request = ComplianceRequestRespondRequest()
        
        response = client.respond_to_compliance_request(payment_id, request)
        
        assert response == 'response'
        # Verify the correct endpoint path was called
        mock_post.assert_called_once()
        args = mock_post.call_args[0]
        assert f'compliance-requests/{payment_id}' in args[0]  # Path argument
        assert args[2] == request  # Request parameter

    def test_respond_to_compliance_request_with_none_payment_id(self, mocker, client: ComplianceRequestsClient):
        mock_post = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        request = ComplianceRequestRespondRequest()
        
        with pytest.raises(TypeError, match="sequence item 1: expected str instance, NoneType found"):
            client.respond_to_compliance_request(None, request)

    def test_respond_to_compliance_request_with_none_request(self, mocker, client: ComplianceRequestsClient):
        mock_post = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        payment_id = "pay_fun26akvvjjerahhctaq2uzhu4"
        
        response = client.respond_to_compliance_request(payment_id, None)
        
        assert response == 'response'
        # Verify None was passed as the request parameter
        mock_post.assert_called_once()
        args = mock_post.call_args[0]
        assert args[2] is None  # Request parameter