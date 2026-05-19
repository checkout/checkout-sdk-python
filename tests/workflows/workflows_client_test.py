import pytest

from tests._assertions import assert_api_call
from checkout_sdk.workflows.workflows import CreateWorkflowRequest, UpdateWorkflowRequest, \
    WebhookWorkflowActionRequest, EventWorkflowConditionRequest, ReflowRequest, EventTypesRequest
from checkout_sdk.workflows.workflows_client import WorkflowsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return WorkflowsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestWorkflowsClient:

    def test_get_workflows(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_workflows() == 'response'
        assert_api_call(mock, 'workflows')

    def test_create_workflow(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = CreateWorkflowRequest()

        assert client.create_workflow(body) == 'response'
        assert_api_call(mock, 'workflows', body)

    def test_get_workflow(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_workflow('workflow_id') == 'response'
        assert_api_call(mock, 'workflows/workflow_id')

    def test_remove_workflow(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')

        assert client.remove_workflow('workflow_id') == 'response'
        assert_api_call(mock, 'workflows/workflow_id')

    def test_update_workflow(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        body = UpdateWorkflowRequest()

        assert client.update_workflow('workflow_id', body) == 'response'
        assert_api_call(mock, 'workflows/workflow_id', body)

    def test_add_workflow_action(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = WebhookWorkflowActionRequest()

        assert client.add_workflow_action('workflow_id', body) == 'response'
        assert_api_call(mock, 'workflows/workflow_id/actions', body)

    def test_update_workflow_action(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        body = WebhookWorkflowActionRequest()

        assert client.update_workflow_action('workflow_id', 'action_id', body) == 'response'
        assert_api_call(mock, 'workflows/workflow_id/actions/action_id', body)

    def test_remove_workflow_action(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')

        assert client.remove_workflow_action('workflow_id', 'action_id') == 'response'
        assert_api_call(mock, 'workflows/workflow_id/actions/action_id')

    def test_add_workflow_condition(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = EventWorkflowConditionRequest()

        assert client.add_workflow_condition('workflow_id', body) == 'response'
        assert_api_call(mock, 'workflows/workflow_id/conditions', body)

    def test_update_workflow_condition(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        body = EventWorkflowConditionRequest()

        assert client.update_workflow_condition('workflow_id', 'condition_id', body) == 'response'
        assert_api_call(mock, 'workflows/workflow_id/conditions/condition_id', body)

    def test_remove_workflow_condition(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')

        assert client.remove_workflow_condition('workflow_id', 'condition_id') == 'response'
        assert_api_call(mock, 'workflows/workflow_id/conditions/condition_id')

    def test_test_workflow(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = EventTypesRequest()

        assert client.test_workflow('workflow_id', body) == 'response'
        assert_api_call(mock, 'workflows/workflow_id/test', body)

    def test_get_event_types(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_event_types() == 'response'
        assert_api_call(mock, 'workflows/event-types')

    def test_get_event(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_event('event_id') == 'response'
        assert_api_call(mock, 'workflows/events/event_id')

    def test_should_get_action_invocations(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_action_invocations('event_id', 'action_id') == 'response'
        assert_api_call(mock, 'workflows/events/event_id/actions/action_id')

    def test_reflow_by_event(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.reflow_by_event('event_id') == 'response'
        assert_api_call(mock, 'workflows/events/event_id/reflow')

    def test_reflow_by_event_and_workflow(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.reflow_by_event_and_workflow('event_id', 'workflow_id') == 'response'
        assert_api_call(mock, 'workflows/events/event_id/workflow/workflow_id/reflow')

    def test_reflow(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = ReflowRequest()

        assert client.reflow(body) == 'response'
        assert_api_call(mock, 'workflows/events/reflow', body)

    def test_get_subject_events(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_subject_events('subject_id') == 'response'
        assert_api_call(mock, 'workflows/events/subject/subject_id')

    def test_reflow_by_subject(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.reflow_by_subject('subject_id') == 'response'
        assert_api_call(mock, 'workflows/events/subject/subject_id/reflow')

    def test_reflow_by_subject_and_workflow(self, mocker, client: WorkflowsClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')

        assert client.reflow_by_subject_and_workflow('subject_id', 'workflow_id') == 'response'
        assert_api_call(mock, 'workflows/events/subject/subject_id/workflow/workflow_id/reflow')
