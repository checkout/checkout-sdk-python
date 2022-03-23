from __future__ import absolute_import

from tests.checkout_test_utils import assert_response


def test_should_get_info(four_api):
    response = four_api.ideal.get_info()
    assert_response(response,
                    '_links',
                    '_links.self',
                    '_links.ideal:issuers',
                    '_links.curies')


def test_should_get_issuers(four_api):
    response = four_api.ideal.get_issuers()
    assert_response(response,
                    'countries',
                    '_links',
                    '_links.self')
