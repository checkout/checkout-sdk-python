import pytest

from tests._assertions import assert_api_call
from checkout_sdk.onboardingsimulator.onboarding_simulator import (
    SimulatorSetRequirementsDueRequest,
    SimulatorSetStatusRequest
)
from checkout_sdk.onboardingsimulator.onboarding_simulator_client import OnboardingSimulatorClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return OnboardingSimulatorClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestOnboardingSimulatorClient:

    def test_should_set_requirements_due(self, mocker, client: OnboardingSimulatorClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = SimulatorSetRequirementsDueRequest()

        assert client.set_requirements_due('entity_id', body) == 'response'
        assert_api_call(mock, 'simulate/entities/entity_id/requirements-due', body)

    def test_should_run_scenario(self, mocker, client: OnboardingSimulatorClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.run_scenario('entity_id', 'scenario_id') == 'response'
        assert_api_call(mock, 'simulate/entities/entity_id/scenarios/scenario_id')

    def test_should_set_entity_status(self, mocker, client: OnboardingSimulatorClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = SimulatorSetStatusRequest()

        assert client.set_entity_status('entity_id', body) == 'response'
        assert_api_call(mock, 'simulate/entities/entity_id/status', body)

    def test_should_list_available_requirements(self, mocker, client: OnboardingSimulatorClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.list_available_requirements() == 'response'
        assert_api_call(mock, 'simulate/requirements-due')

    def test_should_list_scenarios(self, mocker, client: OnboardingSimulatorClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.list_scenarios() == 'response'
        assert_api_call(mock, 'simulate/scenarios')
