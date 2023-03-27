from __future__ import absolute_import

from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta

from checkout_sdk.reports.reports import ReportsQuery
from tests.checkout_test_utils import assert_response

__query = ReportsQuery()
__query.created_after = datetime.now(timezone.utc) - relativedelta(days=7)
__query.created_before = datetime.now(timezone.utc)


def test_should_get_all_reports(default_api):
    response = default_api.reports.get_all_reports(__query)
    assert_response(response,
                    'http_metadata',
                    'count',
                    'limit',
                    'data',
                    '_links')

    if response.data:
        reports = response.data
        for report in reports:
            assert_response(report,
                            'id',
                            'created_on',
                            'type',
                            'description',
                            'account',
                            'from',
                            'to')


def test_should_get_report_details(default_api):
    response = default_api.reports.get_all_reports(__query)
    assert_response(response,
                    'http_metadata',
                    'count',
                    'limit',
                    'data',
                    '_links')

    if response.data:
        report = response.data[0]

        details = default_api.reports.get_report_details(report.id)
        assert_response(details,
                        'id',
                        'created_on',
                        'type',
                        'description',
                        'account',
                        'from',
                        'to')

        assert report.id == details.id
        assert report.created_on == details.created_on
        assert report.type == details.type
        assert report.description == details.description


def test_should_get_report_file(default_api):
    response = default_api.reports.get_all_reports(__query)
    assert_response(response,
                    'http_metadata',
                    'count',
                    'limit',
                    'data',
                    '_links')

    if response.data:
        report = response.data[0]

        details = default_api.reports.get_report_details(report.id)
        assert_response(details,
                        'id',
                        'created_on',
                        'type',
                        'description',
                        'account',
                        'from',
                        'to')

        assert report.id == details.id
        assert report.created_on == details.created_on
        assert report.type == details.type
        assert report.description == details.description

        file = default_api.reports.get_report_file(report.id, report.files[0].id)

        assert file.contents is not None
