from tests.checkout_test_utils import assert_response, retriable
from tests.payments.payments_test_utils import make_card_payment
from tests.workflows.workflows_test_utils import create_workflow


def test_should_get_action_invocations(default_api):
    workflow = create_workflow(default_api)

    payment_response = make_card_payment(default_api)

    payment_event = retriable(callback=default_api.workflows.get_subject_events,
                              subject_id=payment_response.id)

    assert_response(payment_event, 'data')

    workflow_response = default_api.workflows.get_workflow(workflow.id)

    assert_response(workflow_response, 'actions')

    actions_id = workflow_response.actions[0].id

    action_invocations = default_api.workflows.get_action_invocations(payment_event.data[0].id, actions_id)

    assert_response(action_invocations,
                    'workflow_id',
                    'workflow_action_id',
                    'status',
                    'event_id',
                    'action_type',
                    'action_invocations')

    assert actions_id == action_invocations.workflow_action_id
    assert payment_event.data[0].id == action_invocations.event_id
