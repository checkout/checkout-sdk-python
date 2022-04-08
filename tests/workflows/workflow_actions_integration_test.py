from tests.checkout_test_utils import assert_response, retriable
from tests.payments.four.payments_four_test_utils import make_card_payment
from tests.workflows.workflows_test_utils import create_workflow


def test_should_get_action_invocations(four_api):
    workflow = create_workflow(four_api)

    payment_response = make_card_payment(four_api)

    payment_event = retriable(callback=four_api.workflows.get_subject_events,
                              subject_id=payment_response.id)

    assert_response(payment_event, 'data')

    workflow_response = four_api.workflows.get_workflow(workflow.id)

    assert_response(workflow_response, 'actions')

    actions_id = workflow_response.actions[0].id

    action_invocations = four_api.workflows.get_action_invocations(payment_event.data[0].id, actions_id)

    assert_response(action_invocations,
                    'workflow_id',
                    'workflow_action_id',
                    'status',
                    'event_id',
                    'action_type',
                    'action_invocations')

    assert actions_id == action_invocations.workflow_action_id
    assert payment_event.data[0].id == action_invocations.event_id
