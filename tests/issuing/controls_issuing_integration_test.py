import pytest

from checkout_sdk.issuing.controls import ControlType, CardControlsQuery, VelocityWindowType, UpdateCardControlRequest, \
    VelocityWindow, VelocityLimit
from tests.checkout_test_utils import assert_response


@pytest.mark.skip("Avoid creating cards all the time")
class TestControlsIssuing:
    def test_should_create_card(self, issuing_checkout_api, card, control):
        assert_response(control,
                        'id',
                        'description',
                        'control_type',
                        'target_id')

        assert control.target_id == card.id
        assert control.control_type == ControlType.VELOCITY_LIMIT

    def test_should_get_card_controls(self, issuing_checkout_api, card):
        query = CardControlsQuery()
        query.target_id = card.id

        response = issuing_checkout_api.issuing.get_card_controls(query)

        assert_response(response,
                        'controls')

        for control in response.controls:
            assert control.target_id == card.id

    def test_should_get_control_details(self, issuing_checkout_api, control):
        response = issuing_checkout_api.issuing.get_card_control_details(control.id)

        assert_response(response,
                        'id',
                        'description',
                        'control_type',
                        'target_id',
                        'velocity_limit')

        assert response.id == control.id
        assert response.target_id == control.target_id
        assert response.control_type == ControlType.VELOCITY_LIMIT
        assert response.velocity_limit.amount_limit == 500
        assert response.velocity_limit.velocity_window.type == VelocityWindowType.WEEKLY

    def test_should_update_card_controls(self, issuing_checkout_api, control):
        window = VelocityWindow()
        window.type = VelocityWindowType.MONTHLY

        limit = VelocityLimit()
        limit.amount_limit = 1000
        limit.velocity_window = window

        request = UpdateCardControlRequest()
        request.description = 'Max spend of 100€ per month for restaurants'
        request.velocity_limit = limit

        response = issuing_checkout_api.issuing.update_card_control(control.id, request)

        assert_response(response,
                        'id',
                        'description',
                        'control_type',
                        'target_id',
                        'velocity_limit')

        assert response.id == control.id
        assert response.target_id == control.target_id
        assert response.control_type == ControlType.VELOCITY_LIMIT
        assert response.velocity_limit.amount_limit == 1000
        assert response.velocity_limit.velocity_window.type == VelocityWindowType.MONTHLY

    def test_should_remove_control(self, issuing_checkout_api, control):
        response = issuing_checkout_api.issuing.remove_control(control.id)

        assert_response(response, 'id')
        assert response.http_metadata.status_code == 200
        assert response.id == control.id
