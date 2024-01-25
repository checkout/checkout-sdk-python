from __future__ import absolute_import

import pytest

from checkout_sdk.checkout_api import CheckoutApi
from checkout_sdk.sessions.sessions import ThreeDsMethodCompletionRequest, ThreeDsMethodCompletion
from tests.checkout_test_utils import assert_response, retriable
from tests.sessions.sessions_test_utils import get_hosted_session, get_browser_session


@pytest.mark.skip(reason='unstable')
def test_update_card_session_using_id_browser_session(oauth_api: CheckoutApi):
    request_session_response = oauth_api.sessions.request_session(get_hosted_session())
    assert_response(request_session_response, 'id', 'session_secret')

    session_id = request_session_response.id

    update_session = retriable(callback=oauth_api.sessions.update_session,
                               session_id=session_id,
                               channel_data=get_browser_session())

    assert_response(update_session, 'id', 'session_secret')


@pytest.mark.skip(reason='unstable')
def test_update_card_session_using_session_secret_browser_session(oauth_api: CheckoutApi):
    request_session_response = oauth_api.sessions.request_session(get_hosted_session())
    assert_response(request_session_response, 'id', 'session_secret')

    session_id = request_session_response.id
    session_secret = request_session_response.session_secret

    update_session = retriable(callback=oauth_api.sessions.update_session,
                               session_id=session_id,
                               channel_data=get_browser_session(),
                               session_secret=session_secret)

    assert_response(update_session, 'id')


@pytest.mark.skip(reason='unstable')
def test_update_3ds_method_completion_indicator_session_id(oauth_api: CheckoutApi):
    request_session_response = oauth_api.sessions.request_session(get_hosted_session())
    assert_response(request_session_response, 'id', 'session_secret')

    session_id = request_session_response.id

    three_ds_request = ThreeDsMethodCompletionRequest()
    three_ds_request.three_ds_method_completion = ThreeDsMethodCompletion.Y

    update_session = retriable(callback=oauth_api.sessions.update_3ds_method_completion,
                               session_id=session_id,
                               three_ds_method_completion_request=three_ds_request)

    assert_response(update_session, 'id', 'session_secret')


@pytest.mark.skip(reason='unstable')
def test_update_3ds_method_completion_indicator_session_secret(oauth_api: CheckoutApi):
    request_session_response = oauth_api.sessions.request_session(get_hosted_session())
    assert_response(request_session_response, 'id', 'session_secret')

    session_id = request_session_response.id
    session_secret = request_session_response.session_secret

    three_ds_request = ThreeDsMethodCompletionRequest()
    three_ds_request.three_ds_method_completion = ThreeDsMethodCompletion.Y

    update_session = retriable(callback=oauth_api.sessions.update_3ds_method_completion,
                               session_id=session_id,
                               three_ds_method_completion_request=three_ds_request,
                               session_secret=session_secret)

    assert_response(update_session, 'id')
