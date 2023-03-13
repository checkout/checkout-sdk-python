from checkout_sdk.workflows.workflows import UpdateWorkflowRequest, WebhookWorkflowActionRequest, WebhookSignature, \
    EventWorkflowConditionRequest
from tests.checkout_test_utils import assert_response
from tests.workflows.workflows_test_utils import create_workflow, clean_workflows, add_action


def test__should_create_and_get_workflows(default_api):
    workflow = create_workflow(default_api)

    workflow_response = default_api.workflows.get_workflow(workflow.id)

    assert_response(workflow_response,
                    'http_metadata',
                    'id',
                    'name',
                    'active',
                    'actions',
                    'conditions')

    for action in workflow_response.actions:
        assert_response(action, 'id',
                        'type',
                        'url',
                        'headers',
                        'signature')

    for condition in workflow_response.conditions:
        assert_response(condition, 'id', 'type')
        if condition.type == 'event':
            assert hasattr(condition, 'events') and vars(condition.events).__len__() > 0
        if condition.type == 'entity':
            assert hasattr(condition, 'entities') and condition.entities.__len__() > 0
        if condition.type == 'processing_channel':
            assert hasattr(condition, 'processing_channels') and condition.processing_channels.__len__() > 0

    workflows = default_api.workflows.get_workflows()

    for workflow in workflows.data:
        assert_response(workflow, 'id',
                        'name',
                        'active',
                        '_links')

    clean_workflows(default_api)


def test__should_create_and_update_workflow(default_api):
    workflow = create_workflow(default_api)

    update_workflow_request = UpdateWorkflowRequest()
    update_workflow_request.name = 'python_testing_2'
    update_workflow_request.active = False

    update_workflow_response = default_api.workflows.update_workflow(workflow.id, update_workflow_request)

    assert_response(update_workflow_response,
                    'http_metadata',
                    'name',
                    'active')

    assert update_workflow_request.name == update_workflow_response.name
    assert update_workflow_request.active == update_workflow_response.active

    clean_workflows(default_api)


def test__should_add_workflow_action(default_api):
    workflow = create_workflow(default_api)

    workflow_response = default_api.workflows.get_workflow(workflow.id)

    assert_response(workflow_response,
                    'http_metadata',
                    'id',
                    'name',
                    'active',
                    'actions',
                    'conditions')

    signature = WebhookSignature()
    signature.key = '8V8x0dLK%AyD*DNS8JJr'
    signature.method = 'HMACSHA256'

    action_request = WebhookWorkflowActionRequest()
    action_request.url = 'https://google.com/fail/new-action'
    action_request.signature = signature

    response = default_api.workflows.add_workflow_action(workflow.id, action_request)

    assert_response(response,
                    'http_metadata',
                    'id')

    updated_workflow = default_api.workflows.get_workflow(workflow.id)

    assert_response(workflow_response,
                    'http_metadata',
                    'id',
                    'name',
                    'active',
                    'actions',
                    'conditions')

    assert updated_workflow.actions.__len__() > workflow_response.actions.__len__()

    clean_workflows(default_api)


def test__should_update_workflow_action(default_api):
    workflow = create_workflow(default_api)

    workflow_response = default_api.workflows.get_workflow(workflow.id)

    assert_response(workflow_response,
                    'http_metadata',
                    'id',
                    'name',
                    'active',
                    'actions',
                    'conditions')

    action_id = workflow_response.actions[0].id

    signature = WebhookSignature()
    signature.key = '8V8x0dLK%AyD*DNS8JJr'
    signature.method = 'HMACSHA256'

    action_request = WebhookWorkflowActionRequest()
    action_request.url = 'https://google.com/fail/fake'
    action_request.signature = signature

    default_api.workflows.update_workflow_action(workflow_response.id, action_id, action_request)

    workflow_updated = default_api.workflows.get_workflow(workflow_response.id)
    assert_response(workflow_updated, 'actions')
    action = workflow_updated.actions[0]
    assert action_id == action.id
    assert action_request.url == action.url

    clean_workflows(default_api)


def test__should_remove_workflow_action(default_api):
    workflow = create_workflow(default_api)
    action = add_action(default_api, workflow.id)

    response = default_api.workflows.remove_workflow_action(workflow.id, action.id)

    assert_response(response)


def test__should_update_workflow_condition(default_api):
    workflow = create_workflow(default_api)

    workflow_response = default_api.workflows.get_workflow(workflow.id)

    assert_response(workflow_response,
                    'http_metadata',
                    'id',
                    'name',
                    'active',
                    'actions',
                    'conditions')

    condition_event = next((condition for condition in workflow_response.conditions if condition.type == 'event'),
                           None)

    assert condition_event is not None

    condition_request = EventWorkflowConditionRequest()
    condition_request.events = {'gateway': ['card_verified',
                                            'card_verification_declined',
                                            'payment_approved',
                                            'payment_pending',
                                            'payment_declined',
                                            'payment_voided',
                                            'payment_captured',
                                            'payment_refunded'],
                                'dispute': ['dispute_canceled',
                                            'dispute_evidence_required',
                                            'dispute_expired',
                                            'dispute_lost',
                                            'dispute_resolved',
                                            'dispute_won']}

    default_api.workflows.update_workflow_condition(workflow.id, condition_event.id, condition_request)

    workflow_updated = default_api.workflows.get_workflow(workflow.id)

    assert_response(workflow_updated, 'conditions')

    assert workflow_updated.conditions.__len__() == 3

    condition_event_updated = next(
        (condition for condition in workflow_updated.conditions if condition.type == 'event'), None)

    assert condition_event_updated is not None

    clean_workflows(default_api)
