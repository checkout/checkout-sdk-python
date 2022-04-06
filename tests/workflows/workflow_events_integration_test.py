from tests.checkout_test_utils import assert_response, retriable
from tests.payments.four.payments_four_test_utils import make_card_payment
from tests.workflows.workflows_test_utils import create_workflow, clean_workflows


def test_should_get_event_types(four_api):
    response = four_api.workflows.get_event_types()

    results = response.items
    assert results is not None
    assert results.__len__() == 8

    for event_type in results:
        assert_response(event_type,
                        'id',
                        'description',
                        'display_name',
                        'events')
        for event in event_type.events:
            assert_response(event, 'description', 'display_name', 'id')


def test_should_get_subject_event_and_events(four_api):
    create_workflow(four_api)

    payment_response = make_card_payment(four_api, capture=True)

    payment_event = retriable(callback=four_api.workflows.get_subject_events,
                              predicate=__there_are_two_events,
                              subject_id=payment_response.id)

    for event in payment_event.data:
        assert_response(event, 'id', 'type', 'timestamp')

        get_event = four_api.workflows.get_event(event.id)
        assert_response(get_event, 'id',
                        'source',
                        'type',
                        'timestamp',
                        'version',
                        'data')

    clean_workflows(four_api)


def __there_are_two_events(response) -> bool:
    return hasattr(response, 'data') and response.data.__len__() == 2
