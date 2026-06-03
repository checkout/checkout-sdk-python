from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.onboardingsimulator.onboarding_simulator import (
    SimulatorSetRequirementsDueRequest,
    SimulatorSetStatusRequest
)


class OnboardingSimulatorClient(Client):
    __SIMULATE_PATH = 'simulate'
    __ENTITIES_PATH = 'entities'
    __REQUIREMENTS_DUE_PATH = 'requirements-due'
    __SCENARIOS_PATH = 'scenarios'
    __STATUS_PATH = 'status'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.OAUTH)

    def set_requirements_due(self, entity_id: str, request: SimulatorSetRequirementsDueRequest):
        return self._api_client.post(
            self.build_path(self.__SIMULATE_PATH, self.__ENTITIES_PATH, entity_id,
                            self.__REQUIREMENTS_DUE_PATH),
            self._sdk_authorization(), request)

    def run_scenario(self, entity_id: str, scenario_id: str):
        return self._api_client.post(
            self.build_path(self.__SIMULATE_PATH, self.__ENTITIES_PATH, entity_id,
                            self.__SCENARIOS_PATH, scenario_id),
            self._sdk_authorization())

    def set_entity_status(self, entity_id: str, request: SimulatorSetStatusRequest):
        return self._api_client.post(
            self.build_path(self.__SIMULATE_PATH, self.__ENTITIES_PATH, entity_id,
                            self.__STATUS_PATH),
            self._sdk_authorization(), request)

    def list_available_requirements(self):
        return self._api_client.get(
            self.build_path(self.__SIMULATE_PATH, self.__REQUIREMENTS_DUE_PATH),
            self._sdk_authorization())

    def list_scenarios(self):
        return self._api_client.get(
            self.build_path(self.__SIMULATE_PATH, self.__SCENARIOS_PATH),
            self._sdk_authorization())
