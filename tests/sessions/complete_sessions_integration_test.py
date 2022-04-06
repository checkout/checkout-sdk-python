from __future__ import absolute_import

import pytest

from checkout_sdk.exception import CheckoutApiException
from checkout_sdk.four.checkout_api import CheckoutApi
from tests.checkout_test_utils import assert_response
from tests.sessions.sessions_test_utils import get_hosted_session


def test_try_complete_sessions(oauth_api: CheckoutApi):
    session_request = get_hosted_session()

    request_session_response = oauth_api.sessions.request_session(session_request)
    assert_response(request_session_response, 'id', 'session_secret')

    session_id = request_session_response.id
    session_secret = request_session_response.session_secret

    try:
        oauth_api.sessions.complete_session(session_id)
        pytest.fail()
    except CheckoutApiException as err:
        assert err.args[0] == 'The API response status code (403) does not indicate success.'
        assert err.error_details[0] == 'update_not_allowed_due_to_state'

    try:
        oauth_api.sessions.complete_session(session_id, session_secret)
        pytest.fail()
    except CheckoutApiException as err:
        assert err.error_details[0] == 'update_not_allowed_due_to_state'
