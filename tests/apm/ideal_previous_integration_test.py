from __future__ import absolute_import

import pytest

from tests.checkout_test_utils import assert_response


@pytest.mark.skip(reason='not available')
def test_should_get_info(previous_api):
    response = previous_api.ideal.get_info()
    assert_response(response,
                    'http_metadata',
                    '_links',
                    '_links.self',
                    '_links.ideal:issuers',
                    '_links.curies')


@pytest.mark.skip(reason='not available')
def test_should_get_issuers(previous_api):
    response = previous_api.ideal.get_issuers()
    assert_response(response,
                    'http_metadata',
                    'countries',
                    '_links',
                    '_links.self')
