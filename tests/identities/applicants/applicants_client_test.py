import pytest

from tests._assertions import assert_api_call
from checkout_sdk.identities.applicants.applicants import CreateApplicantRequest, UpdateApplicantRequest
from checkout_sdk.identities.applicants.applicants_client import ApplicantsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return ApplicantsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestApplicantsClient:

    def test_should_create_applicant(self, mocker, client: ApplicantsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = CreateApplicantRequest()

        assert client.create_applicant(body) == 'response'
        assert_api_call(mock, 'applicants', body)

    def test_should_get_applicant(self, mocker, client: ApplicantsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_applicant('aplt_7hr7swleu6guzjqesyxmyodnya') == 'response'
        assert_api_call(mock, 'applicants/aplt_7hr7swleu6guzjqesyxmyodnya')

    def test_should_update_applicant(self, mocker, client: ApplicantsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        body = UpdateApplicantRequest()

        assert client.update_applicant('aplt_7hr7swleu6guzjqesyxmyodnya', body) == 'response'
        assert_api_call(mock, 'applicants/aplt_7hr7swleu6guzjqesyxmyodnya', body)

    def test_should_anonymize_applicant(self, mocker, client: ApplicantsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.anonymize_applicant('aplt_7hr7swleu6guzjqesyxmyodnya') == 'response'
        assert_api_call(mock, 'applicants/aplt_7hr7swleu6guzjqesyxmyodnya/anonymize')
