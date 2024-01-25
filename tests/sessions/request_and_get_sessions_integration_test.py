from __future__ import absolute_import

import pytest

from checkout_sdk.common.enums import ChallengeIndicator
from checkout_sdk.checkout_api import CheckoutApi
from checkout_sdk.sessions.sessions import Category, TransactionType
from tests.checkout_test_utils import assert_response
from tests.sessions.sessions_test_utils import get_browser_session, get_non_hosted_session, get_app_session


@pytest.mark.skip(reason='unstable')
def test_request_and_get_card_session_browser_session(oauth_api: CheckoutApi):
    browser_session = get_browser_session()
    session_request = get_non_hosted_session(browser_session, Category.PAYMENT,
                                             ChallengeIndicator.NO_PREFERENCE, TransactionType.GOODS_SERVICE)

    request_session_response = oauth_api.sessions.request_session(session_request)
    assert_response(request_session_response, 'id', 'session_secret')

    session_id = request_session_response.id
    session_secret = request_session_response.session_secret

    assert_response(oauth_api.sessions.get_session_details(session_id), 'id', 'session_secret')
    assert_response(oauth_api.sessions.get_session_details(session_id, session_secret), 'id')


@pytest.mark.skip(reason='unstable')
def test_request_and_get_card_session_app_session(oauth_api: CheckoutApi):
    browser_session = get_app_session()
    session_request = get_non_hosted_session(browser_session, Category.PAYMENT,
                                             ChallengeIndicator.NO_PREFERENCE, TransactionType.GOODS_SERVICE)

    request_session_response = oauth_api.sessions.request_session(session_request)
    assert_response(request_session_response, 'id', 'session_secret')

    session_id = request_session_response.id
    session_secret = request_session_response.session_secret

    assert_response(oauth_api.sessions.get_session_details(session_id), 'id', 'session_secret')
    assert_response(oauth_api.sessions.get_session_details(session_id, session_secret), 'id')
