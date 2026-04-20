import os

import pytest

from checkout_sdk.identities.amlscreening.amlscreening import AmlScreeningRequest, SearchParameters
from tests.checkout_test_utils import assert_response

# tests

@pytest.mark.skip(reason='Requires valid applicant ID and AML configuration')
def test_should_create_aml_screening(default_api):
    response = default_api.aml_screening.create_aml_screening(aml_screening_request())
    assert_aml_screening_response(response)


@pytest.mark.skip(reason='Requires valid applicant ID and AML configuration')
def test_should_get_aml_screening(default_api):
    created = default_api.aml_screening.create_aml_screening(aml_screening_request())
    retrieved = default_api.aml_screening.get_aml_screening(created.id)
    assert_aml_screening_response(retrieved)


@pytest.mark.skip(reason='Requires valid applicant ID and AML configuration')
def test_should_create_and_track_aml_screening_workflow(default_api):
    created = default_api.aml_screening.create_aml_screening(aml_screening_request())
    assert_aml_screening_response(created)

    updated = default_api.aml_screening.get_aml_screening(created.id)
    assert_aml_screening_response(updated)
    assert updated.id == created.id
    assert updated.applicant_id == created.applicant_id


@pytest.mark.skip(reason='Requires valid applicant ID and AML configuration')
def test_should_validate_monitoring_configuration(default_api):
    request = aml_screening_request()
    request.monitored = False

    response = default_api.aml_screening.create_aml_screening(request)
    assert_aml_screening_response(response)
    assert response.monitored is False

# common functions

def aml_screening_request() -> AmlScreeningRequest:
    search_parameters = SearchParameters()
    search_parameters.configuration_identifier = os.environ.get('CHECKOUT_TEST_AML_CONFIG_ID', 'config_test_id')

    request = AmlScreeningRequest()
    request.applicant_id = os.environ.get('CHECKOUT_TEST_APPLICANT_ID', 'aplt_test_applicant_id')
    request.search_parameters = search_parameters
    request.monitored = True
    return request


def assert_aml_screening_response(response):
    assert_response(response, 'http_metadata', 'id', 'applicant_id', 'status', 'search_parameters')
