import pytest

from checkout_sdk.identities.applicants.applicants import CreateApplicantRequest, UpdateApplicantRequest
from checkout_sdk.identities.applicants.applicants_client import ApplicantsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return ApplicantsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


# tests

class TestApplicantsClient:

    def test_should_create_applicant(self, mocker, client: ApplicantsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_applicant(CreateApplicantRequest()) == 'response'

    def test_should_get_applicant(self, mocker, client: ApplicantsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_applicant('aplt_7hr7swleu6guzjqesyxmyodnya') == 'response'

    def test_should_update_applicant(self, mocker, client: ApplicantsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        assert client.update_applicant('aplt_7hr7swleu6guzjqesyxmyodnya', UpdateApplicantRequest()) == 'response'

    def test_should_anonymize_applicant(self, mocker, client: ApplicantsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.anonymize_applicant('aplt_7hr7swleu6guzjqesyxmyodnya') == 'response'
