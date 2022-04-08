from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.workflows.workflows import CreateWorkflowRequest, UpdateWorkflowRequest, WorkflowActionRequest, \
    WorkflowConditionRequest, ReflowRequest


class WorkflowsClient(Client):
    __WORKFLOWS_PATH = 'workflows'
    __ACTIONS_PATH = 'actions'
    __CONDITIONS_PATH = 'conditions'
    __EVENT_TYPES_PATH = 'event-types'
    __EVENTS_PATH = 'events'
    __SUBJECT_PATH = 'subject'
    __REFLOW_PATH = 'reflow'
    __WORKFLOW_PATH = 'workflow'

    def __init__(self, api_client: ApiClient, configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def create_workflow(self, create_workflow_request: CreateWorkflowRequest):
        return self._api_client.post(self.__WORKFLOWS_PATH,
                                     self._sdk_authorization(),
                                     create_workflow_request)

    def get_workflows(self):
        return self._api_client.get(self.__WORKFLOWS_PATH,
                                    self._sdk_authorization())

    def get_workflow(self, workflow_id: str):
        return self._api_client.get(self.build_path(self.__WORKFLOWS_PATH, workflow_id),
                                    self._sdk_authorization())

    def update_workflow(self, workflow_id: str, update_workflow_request: UpdateWorkflowRequest):
        return self._api_client.patch(self.build_path(self.__WORKFLOWS_PATH, workflow_id),
                                      self._sdk_authorization(),
                                      update_workflow_request)

    def remove_workflow(self, workflow_id: str):
        return self._api_client.delete(self.build_path(self.__WORKFLOWS_PATH, workflow_id),
                                       self._sdk_authorization())

    def update_workflow_action(self, workflow_id: str, action_id: str, workflow_action_request: WorkflowActionRequest):
        return self._api_client.put(self.build_path(self.__WORKFLOWS_PATH, workflow_id, self.__ACTIONS_PATH, action_id),
                                    self._sdk_authorization(),
                                    workflow_action_request)

    def update_workflow_condition(self, workflow_id: str, condition_id: str,
                                  workflow_condition_request: WorkflowConditionRequest):
        return self._api_client.put(
            self.build_path(self.__WORKFLOWS_PATH, workflow_id, self.__CONDITIONS_PATH, condition_id),
            self._sdk_authorization(),
            workflow_condition_request)

    def get_event_types(self):
        return self._api_client.get(self.build_path(self.__WORKFLOWS_PATH, self.__EVENT_TYPES_PATH),
                                    self._sdk_authorization())

    def get_subject_events(self, subject_id: str):
        return self._api_client.get(
            self.build_path(self.__WORKFLOWS_PATH, self.__EVENTS_PATH, self.__SUBJECT_PATH, subject_id),
            self._sdk_authorization())

    def get_event(self, event_id: str):
        return self._api_client.get(
            self.build_path(self.__WORKFLOWS_PATH, self.__EVENTS_PATH, event_id),
            self._sdk_authorization())

    def reflow_by_event(self, event_id: str):
        return self._api_client.post(
            self.build_path(self.__WORKFLOWS_PATH, self.__EVENTS_PATH, event_id, self.__REFLOW_PATH),
            self._sdk_authorization())

    def reflow_by_subject(self, subject_id: str):
        return self._api_client.post(
            self.build_path(self.__WORKFLOWS_PATH, self.__EVENTS_PATH, self.__SUBJECT_PATH, subject_id,
                            self.__REFLOW_PATH),
            self._sdk_authorization())

    def reflow_by_event_and_workflow(self, event_id: str, workflow_id: str):
        return self._api_client.post(
            self.build_path(self.__WORKFLOWS_PATH, self.__EVENTS_PATH, event_id, self.__WORKFLOW_PATH, workflow_id,
                            self.__REFLOW_PATH),
            self._sdk_authorization())

    def reflow_by_subject_and_workflow(self, subject_id: str, workflow_id: str):
        return self._api_client.post(
            self.build_path(self.__WORKFLOWS_PATH, self.__EVENTS_PATH, self.__SUBJECT_PATH, subject_id,
                            self.__WORKFLOW_PATH, workflow_id, self.__REFLOW_PATH),
            self._sdk_authorization())

    def reflow(self, reflow_request: ReflowRequest):
        return self._api_client.post(self.build_path(self.__WORKFLOWS_PATH, self.__EVENTS_PATH, self.__REFLOW_PATH),
                                     self._sdk_authorization(),
                                     reflow_request)

    def get_action_invocations(self, event_id: str, action_id: str):
        return self._api_client.get(
            self.build_path(self.__WORKFLOWS_PATH, self.__EVENTS_PATH, event_id, self.__ACTIONS_PATH, action_id),
            self._sdk_authorization())
