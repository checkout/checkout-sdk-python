import pytest

from checkout_sdk.apm.bacs import BacsNotificationRequest
from checkout_sdk.apm.bacs_client import BacsClient
from tests._assertions import assert_api_call


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return BacsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestBacsClient:

    def test_should_send_notification(self, mocker, client: BacsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        request = BacsNotificationRequest()

        assert client.send_notification(request) == 'response'
        assert_api_call(mock, 'apms/bacs/notifications', body=request)
