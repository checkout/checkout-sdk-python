from checkout_sdk.four.checkout_api import CheckoutApi
from checkout_sdk.workflows.workflows import ReflowByEventsRequest, ReflowBySubjectsRequest
from tests.checkout_test_utils import assert_response, retriable
from tests.payments.four.payments_four_test_utils import make_card_payment
from tests.workflows.workflows_test_utils import create_workflow, clean_workflows


def test__should_reflow_by_event(four_api):
    create_workflow(four_api)

    payment = make_card_payment(four_api)

    payment_event = __get_subject_event(four_api, payment['id'])

    four_api.workflows.reflow_by_event(payment_event['id'])

    clean_workflows(four_api)


def test__should_reflow_by_subject(four_api):
    create_workflow(four_api)

    payment = make_card_payment(four_api)

    retriable(callback=four_api.workflows.reflow_by_subject,
              subject_id=payment['id'])

    clean_workflows(four_api)


def test_should_reflow_by_event_and_workflow(four_api):
    workflow = create_workflow(four_api)

    payment = make_card_payment(four_api)

    payment_event = __get_subject_event(four_api, payment['id'])

    retriable(callback=four_api.workflows.reflow_by_event_and_workflow,
              event_id=payment_event['id'],
              workflow_id=workflow['id'])

    clean_workflows(four_api)


def test_should_reflow_by_events(four_api):
    workflow = create_workflow(four_api)

    payment = make_card_payment(four_api)

    payment_event = __get_subject_event(four_api, payment['id'])

    request = ReflowByEventsRequest()
    request.events = [payment_event['id']]
    request.workflows = [workflow['id']]

    retriable(callback=four_api.workflows.reflow,
              reflow_request=request)

    clean_workflows(four_api)


def test_reflow_by_subject_and_workflow(four_api):
    workflow = create_workflow(four_api)

    payment = make_card_payment(four_api)

    retriable(callback=four_api.workflows.reflow_by_subject_and_workflow,
              subject_id=payment['id'],
              workflow_id=workflow['id'])

    clean_workflows(four_api)


def test__should_reflow_subjects(four_api):
    workflow = create_workflow(four_api)

    payment = make_card_payment(four_api)

    request = ReflowBySubjectsRequest()
    request.subjects = [payment['id']]
    request.workflows = [workflow['id']]

    retriable(callback=four_api.workflows.reflow,
              reflow_request=request)

    clean_workflows(four_api)


def __get_subject_event(four_api: CheckoutApi, subject_id: str):
    response = retriable(callback=four_api.workflows.get_subject_events,
                         predicate=__payment_is_approved,
                         subject_id=subject_id)

    approved_event = __find_payment_approved(response)
    assert_response(approved_event, 'id',
                    'type',
                    'timestamp')

    return approved_event


def __payment_is_approved(response) -> bool:
    return 'data' in response and response['data'].__len__() == 1 and __find_payment_approved(response) is not None


def __find_payment_approved(response):
    return next((event for event in response['data'] if event['type'] == 'payment_approved'), None)
