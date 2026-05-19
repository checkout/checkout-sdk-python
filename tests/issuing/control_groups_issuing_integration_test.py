import pytest

from checkout_sdk.issuing.controls import ControlGroupQueryTarget, FailIfType
from tests.checkout_test_utils import assert_response
from tests.issuing.conftest import get_control_group_request


@pytest.mark.skip("Avoid creating cards all the time")
@pytest.mark.usefixtures("card", "control_group")
class TestControlGroupsIssuing:
    # tests

    def test_should_create_control_group(self, card, control_group):
        assert_response(control_group,
                        'id',
                        'target_id',
                        'fail_if',
                        'description',
                        'controls')

        assert control_group.id.startswith('cgr_')
        assert control_group.target_id == card.id
        assert control_group.fail_if == FailIfType.ALL_FAIL
        assert control_group.description == 'Integration test control group'

    def test_should_get_target_control_groups(self, issuing_checkout_api, card, control_group):
        query = ControlGroupQueryTarget()
        query.target_id = card.id

        response = issuing_checkout_api.issuing.get_target_control_groups(query)

        assert_response(response, 'control_groups')
        assert any(cg.id == control_group.id for cg in response.control_groups)

    def test_should_get_control_group_details(self, issuing_checkout_api, control_group):
        response = issuing_checkout_api.issuing.get_control_group_details(control_group.id)

        assert_response(response,
                        'id',
                        'target_id',
                        'fail_if',
                        'description')

        assert response.id == control_group.id
        assert response.target_id == control_group.target_id
        assert response.fail_if == control_group.fail_if

    def test_should_delete_control_group(self, issuing_checkout_api, card):
        request = get_control_group_request(card.id)
        created = issuing_checkout_api.issuing.create_control_group(request)

        response = issuing_checkout_api.issuing.delete_control_group(created.id)

        assert_response(response)
        assert response.http_metadata.status_code == 200
