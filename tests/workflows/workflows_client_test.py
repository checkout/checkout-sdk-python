import pytest

from checkout_sdk.workflows.workflows import CreateWorkflowRequest, UpdateWorkflowRequest, WebhookWorkflowActionRequest, \
    EventWorkflowConditionRequest, ReflowRequest
from checkout_sdk.workflows.workflows_client import WorkflowsClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return WorkflowsClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestWorkflowsClient:

    def test_create_workflow(self, mocker, client: WorkflowsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_workflow(CreateWorkflowRequest()) == 'response'

    def test_get_workflows(self, mocker, client: WorkflowsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_workflows() == 'response'

    def test_get_workflow(self, mocker, client: WorkflowsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_workflow('workflow_id') == 'response'

    def test_update_workflow(self, mocker, client: WorkflowsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        assert client.update_workflow('workflow_id', UpdateWorkflowRequest()) == 'response'

    def test_remove_workflow(self, mocker, client: WorkflowsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.delete')
        client.remove_workflow('workflow_id')

    def test_update_workflow_action(self, mocker, client: WorkflowsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        client.update_workflow_action('workflow_id', 'action_id', WebhookWorkflowActionRequest())

    def test_update_workflow_condition(self, mocker, client: WorkflowsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        client.update_workflow_condition('workflow_id', 'condition_id', EventWorkflowConditionRequest())

    def test_get_event_types(self, mocker, client: WorkflowsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_event_types() == 'response'

    def test_get_subject_events(self, mocker, client: WorkflowsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_subject_events('subject_id') == 'response'

    def test_get_event(self, mocker, client: WorkflowsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_event('event_id') == 'response'

    def test_reflow_by_event(self, mocker, client: WorkflowsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        client.reflow_by_event('event_id')

    def test_reflow_by_subject(self, mocker, client: WorkflowsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        client.reflow_by_subject('subject_id')

    def test_reflow_by_event_and_workflow(self, mocker, client: WorkflowsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        client.reflow_by_event_and_workflow('event_id', 'workflow_id')

    def test_reflow_by_subject_and_workflow(self, mocker, client: WorkflowsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        client.reflow_by_subject_and_workflow('subject_id', 'workflow_id')

    def test_reflow(self, mocker, client: WorkflowsClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        client.reflow(ReflowRequest())
