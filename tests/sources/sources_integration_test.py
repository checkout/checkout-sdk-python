from __future__ import absolute_import

from checkout_sdk.sources.sources import MandateType, SourceData, SepaSourceRequest
from tests.checkout_test_utils import assert_response, address, phone


def test_should_create_sepa_source(default_api):
    source_data = SourceData()
    source_data.first_name = 'Marcus'
    source_data.last_name = 'Barrilius Maximus'
    source_data.account_iban = 'DE68100100101234567895'
    source_data.bic = 'PBNKDEFFXXX'
    source_data.billing_descriptor = '.NET SDK test'
    source_data.mandate_type = MandateType.SINGLE

    sepa_source_request = SepaSourceRequest()
    sepa_source_request.billing_address = address()
    sepa_source_request.reference = 'Python SDK test'
    sepa_source_request.phone = phone()
    sepa_source_request.source_data = source_data

    response = default_api.sources.create_sepa_source(sepa_source_request)
    assert_response(response, 'type',
                    'customer.id',
                    'id',
                    '_links.sepa:mandate-cancel',
                    '_links.sepa:mandate-get',
                    'response_code',
                    'response_data.mandate_reference')
