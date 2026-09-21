import json
from unittest.mock import MagicMock

import pytest

from checkout_sdk.api_client import ApiClient
from checkout_sdk.identities.addressdocumentverification.addressdocumentverification_client import \
    AddressDocumentVerificationClient
from checkout_sdk.identities.iddocumentverification.iddocumentverification_client import \
    IdDocumentVerificationClient
from checkout_sdk.identities.identityverification.identityverification_client import \
    IdentityVerificationClient


# The four identities client tests mock ApiClient and return the bare string 'response', so none of
# them exercises a response shape. These feed the swagger examples verbatim through the real
# ApiClient and ResponseWrapper, which is what actually maps the payload for a caller.
#
# The examples below are copied verbatim from shared/swagger-latest.json components.examples so a
# key renamed in the spec fails the test rather than being carried forward by a hand-written
# fixture. asset_url in particular is the only link the asset schemas declare, and it is required.
#
# Every KEY below is verbatim. The href VALUES are abbreviated to keep lines under the line
# length limit: the assertions only read the filename fragment, and the keys are what the tests
# exist to protect.

ADV_ATTEMPT_ASSETS = """
{
  "total_count": 1,
  "skip": 0,
  "limit": 10,
  "data": [
    {
      "type": "document",
      "_links": {
        "asset_url": {
          "href": "https://storage-b.env.ubble.ai/ubble-ai/NDY/a54/bb6/address_document.png?X-Amz-Expires=3600"
        }
      }
    }
  ],
  "_links": {
    "self": {"href": "https://idv.checkout.com/address-document-verifications/adv_1/attempts/adva_1/assets"},
    "next": {"href": "https://idv.checkout.com/address-document-verifications/adv_1/attempts/adva_1/assets?..."},
    "previous": {"href": "https://idv.checkout.com/address-document-verifications/adv_1/attempts/adva_1/assets?..."}
  }
}
"""

IDDV_ATTEMPT_ASSETS = """
{
  "total_count": 2,
  "skip": 0,
  "limit": 10,
  "data": [
    {
      "type": "document_front_image",
      "_links": {
        "asset_url": {
          "href": "https://storage-b.env.ubble.ai/ubble-ai/NDY/a54/bb6/document_front.png?X-Amz-Expires=3600"
        }
      }
    },
    {
      "type": "document_back_image",
      "_links": {
        "asset_url": {
          "href": "https://storage-b.env.ubble.ai/ubble-ai/NDY/a54/bb6/document_back.png?X-Amz-Expires=3600"
        }
      }
    }
  ],
  "_links": {
    "self": {"href": "https://idv.checkout.com/id-document-verifications/iddv_1/attempts/datp_1/assets"}
  }
}
"""

EMPTY_ASSETS_PAGE = """
{
  "total_count": 0,
  "skip": 0,
  "limit": 10,
  "data": [],
  "_links": {
    "self": {"href": "https://idv.checkout.com/address-document-verifications/adv_1/attempts/adva_1/assets"}
  }
}
"""

ADV_PDF_REPORT = '{"pdf_report": "https://www.example.com/reports/adv_tkoi5db4hryu5cei5vwoabr7we.pdf"}'
IDV_PDF_REPORT = '{"pdf_report": "https://www.example.com/reports/idv_tkoi5db4hryu5cei5vwoabr7we.pdf"}'


def _client(cls, mock_sdk_configuration, body):
    api_client = ApiClient(configuration=mock_sdk_configuration,
                           base_uri=mock_sdk_configuration.environment.base_uri)
    http_client = MagicMock()
    response = MagicMock()
    response.status_code = 200
    response.text = body
    response.headers = {'Content-Type': 'application/json'}
    response.json.return_value = json.loads(body)
    response.raise_for_status.return_value = None
    http_client.request.return_value = response
    api_client._http_client = http_client

    authorization = MagicMock()
    authorization.get_authorization_header.return_value = 'Bearer test'

    client = cls(api_client=api_client, configuration=mock_sdk_configuration)
    client._sdk_authorization = lambda *args, **kwargs: authorization
    return client


class TestAttemptAssetsResponseShape:

    def test_address_document_verification_assets_from_the_swagger_example(self, mock_sdk_configuration):
        client = _client(AddressDocumentVerificationClient, mock_sdk_configuration, ADV_ATTEMPT_ASSETS)

        assets = client.get_address_document_verification_attempt_assets('adv_1', 'adva_1')

        assert assets.total_count == 1
        assert assets.skip == 0
        assert assets.limit == 10
        assert len(assets.data) == 1
        assert assets.data[0].type == 'document'
        assert 'address_document.png' in assets.data[0]._links.asset_url.href
        assert assets._links.self.href.endswith('/assets')
        assert assets._links.next is not None
        assert assets._links.previous is not None

    def test_id_document_verification_assets_from_the_swagger_example(self, mock_sdk_configuration):
        client = _client(IdDocumentVerificationClient, mock_sdk_configuration, IDDV_ATTEMPT_ASSETS)

        assets = client.get_id_document_verification_attempt_assets('iddv_1', 'datp_1')

        assert assets.total_count == 2
        assert len(assets.data) == 2
        assert assets.data[0].type == 'document_front_image'
        assert assets.data[1].type == 'document_back_image'
        assert 'document_front.png' in assets.data[0]._links.asset_url.href
        assert 'document_back.png' in assets.data[1]._links.asset_url.href

    @pytest.mark.parametrize('body', [ADV_ATTEMPT_ASSETS, IDDV_ATTEMPT_ASSETS])
    def test_the_asset_link_is_asset_url_and_not_download(self, mock_sdk_configuration, body):
        """asset_url is the only link the AdvAttemptAsset and IddvAttemptAsset schemas declare,
        and it is required. A hand-written fixture guessing 'download' would pass a test that
        asserted the same guess, so this asserts against the spec's own example."""
        client = _client(AddressDocumentVerificationClient, mock_sdk_configuration, body)

        assets = client.get_address_document_verification_attempt_assets('adv_1', 'adva_1')

        for asset in assets.data:
            assert hasattr(asset._links, 'asset_url')
            assert not hasattr(asset._links, 'download')

    def test_an_empty_assets_page_is_a_valid_response(self, mock_sdk_configuration):
        """data declares minItems 0, so an attempt with no assets yet is a legal page."""
        client = _client(AddressDocumentVerificationClient, mock_sdk_configuration, EMPTY_ASSETS_PAGE)

        assets = client.get_address_document_verification_attempt_assets('adv_1', 'adva_1')

        assert assets.total_count == 0
        assert assets.data == []
        assert assets._links.self.href.endswith('/assets')


class TestPdfReportResponseShape:

    def test_address_document_verification_report_carries_pdf_report(self, mock_sdk_configuration):
        client = _client(AddressDocumentVerificationClient, mock_sdk_configuration, ADV_PDF_REPORT)

        report = client.get_address_document_verification_report('adv_1')

        assert report.pdf_report.endswith('.pdf')

    def test_id_document_verification_report_carries_pdf_report(self, mock_sdk_configuration):
        client = _client(IdDocumentVerificationClient, mock_sdk_configuration, IDV_PDF_REPORT)

        report = client.get_id_document_verification_report('iddv_1')

        assert report.pdf_report.endswith('.pdf')

    def test_identity_verification_report_carries_pdf_report(self, mock_sdk_configuration):
        client = _client(IdentityVerificationClient, mock_sdk_configuration, IDV_PDF_REPORT)

        report = client.get_identity_verification_report('idv_1')

        assert report.pdf_report.endswith('.pdf')

    def test_the_report_no_longer_carries_signed_url(self, mock_sdk_configuration):
        """IdvPdf declares pdf_report as its only property. signed_url was the pre 2026-09-02
        name and five integration assertions still named it."""
        client = _client(IdentityVerificationClient, mock_sdk_configuration, IDV_PDF_REPORT)

        report = client.get_identity_verification_report('idv_1')

        assert hasattr(report, 'pdf_report')
        assert not hasattr(report, 'signed_url')
