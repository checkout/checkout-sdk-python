import pytest

from tests.checkout_test_utils import assert_response, retriable
from tests.payments.payments_test_utils import make_card_payment
from tests.workflows.workflows_test_utils import create_workflow, clean_workflows


def test_should_get_event_types(default_api):
    response = default_api.workflows.get_event_types()

    results = response.items
    assert results is not None
    assert results.__len__() >= 7

    for event_type in results:
        assert_response(event_type,
                        'id',
                        'description',
                        'display_name',
                        'events')
        for event in event_type.events:
            assert_response(event, 'description', 'display_name', 'id')


@pytest.mark.skip(reason='unstable')
def test_should_get_subject_event_and_events(default_api):
    create_workflow(default_api)

    payment_response = make_card_payment(default_api, capture=True)

    payment_event = retriable(callback=default_api.workflows.get_subject_events,
                              predicate=__there_are_two_events,
                              subject_id=payment_response.id)

    for event in payment_event.data:
        assert_response(event, 'id', 'type', 'timestamp')

        get_event = default_api.workflows.get_event(event.id)
        assert_response(get_event, 'id',
                        'source',
                        'type',
                        'timestamp',
                        'version',
                        'data')

    clean_workflows(default_api)


def __there_are_two_events(response) -> bool:
    return hasattr(response, 'data') and response.data.__len__() == 2
