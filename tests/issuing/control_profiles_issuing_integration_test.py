import pytest

from checkout_sdk.issuing.controls import ControlGroupQueryTarget, ControlProfileRequest
from tests.checkout_test_utils import assert_response


@pytest.mark.skip("Avoid creating cards all the time")
@pytest.mark.usefixtures("control_profile")
class TestControlProfilesIssuing:
    # tests

    def test_should_create_control_profile(self, control_profile):
        assert_response(control_profile,
                        'id',
                        'name')

        assert control_profile.name == 'Test Control Profile'

    def test_should_get_all_control_profiles(self, issuing_checkout_api, control_profile):
        query = ControlGroupQueryTarget()
        query.target_id = control_profile.id

        response = issuing_checkout_api.issuing.get_all_control_profiles(query)

        assert_response(response, 'control_profiles')
        assert any(cp.id == control_profile.id for cp in response.control_profiles)

    def test_should_get_control_profile_details(self, issuing_checkout_api, control_profile):
        response = issuing_checkout_api.issuing.get_control_profile_details(control_profile.id)

        assert_response(response,
                        'id',
                        'name')

        assert response.id == control_profile.id
        assert response.name == control_profile.name

    def test_should_update_control_profile(self, issuing_checkout_api, control_profile):
        request = build_update_control_profile_request()

        response = issuing_checkout_api.issuing.update_control_profile(control_profile.id, request)

        assert_response(response, 'id', 'name')
        assert response.id == control_profile.id
        assert response.name == 'Updated Control Profile'

    def test_should_add_target_to_control_profile(self, issuing_checkout_api, active_card, control_profile):
        response = issuing_checkout_api.issuing.add_target_to_control_profile(control_profile.id, active_card.id)

        assert_response(response)
        assert response.http_metadata.status_code == 200

    def test_should_remove_target_from_control_profile(self, issuing_checkout_api, active_card, control_profile):
        issuing_checkout_api.issuing.add_target_to_control_profile(control_profile.id, active_card.id)

        response = issuing_checkout_api.issuing.remove_target_from_control_profile(control_profile.id, active_card.id)

        assert_response(response)
        assert response.http_metadata.status_code == 200

    def test_should_delete_control_profile(self, issuing_checkout_api):
        created = issuing_checkout_api.issuing.create_control_profile(build_create_control_profile_request())

        response = issuing_checkout_api.issuing.delete_control_profile(created.id)

        assert_response(response)
        assert response.http_metadata.status_code == 200


# common methods

def build_create_control_profile_request() -> ControlProfileRequest:
    request = ControlProfileRequest()
    request.name = 'Test Control Profile'
    return request


def build_update_control_profile_request() -> ControlProfileRequest:
    request = ControlProfileRequest()
    request.name = 'Updated Control Profile'
    return request
