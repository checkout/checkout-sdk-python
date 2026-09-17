import json
from datetime import date, datetime, time

import pytest

from checkout_sdk.json_serializer import JsonSerializer


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class _Holder:
    """Minimal stand-in for an SDK request class: a plain attribute holder."""


def _wrap(value):
    holder = _Holder()
    holder.value = value
    return _serialize(holder)['value']


class TestDateRendering:
    """The serializer renders date-like values, it does not reflect over them.

    The specification distinguishes `format: date` (yyyy-MM-dd) from `format: date-time`
    (RFC 3339). A datetime renders as a full timestamp, which is correct for a date-time
    property; a date renders without a time component.
    """

    def test_a_date_renders_without_a_time_component(self):
        assert _wrap(date(2026, 10, 1)) == '2026-10-01'

    @pytest.mark.parametrize('value,expected', [
        (date(2026, 1, 9), '2026-01-09'),      # single-digit month and day are padded
        (date(2024, 2, 29), '2024-02-29'),     # leap day
        (date(2026, 12, 31), '2026-12-31'),
    ])
    def test_every_date_renders_as_an_iso_date(self, value, expected):
        assert _wrap(value) == expected

    def test_a_date_used_to_raise_a_type_error(self):
        # Regression guard. date has no `microsecond` keyword on replace(), so before the date
        # branch existed this raised
        # TypeError: replace() got an unexpected keyword argument 'microsecond'
        # for any date on any field, including nested objects and lists.
        assert _wrap(date.today()) == date.today().isoformat()


class TestDateTimeRenderingIsUnchanged:
    """datetime subclasses date, so it must be excluded from the date branch explicitly."""

    @pytest.mark.parametrize('value,expected', [
        (datetime(2026, 10, 1), '2026-10-01T00:00:00'),
        (datetime(2026, 10, 1, 13, 45, 30), '2026-10-01T13:45:30'),
        # microseconds are still truncated, as before
        (datetime(2026, 10, 1, 13, 45, 30, 123456), '2026-10-01T13:45:30'),
    ])
    def test_a_datetime_still_renders_a_full_timestamp(self, value, expected):
        assert _wrap(value) == expected

    def test_a_time_still_renders_through_the_strftime_branch(self):
        assert _wrap(time(12, 30)) == '12:30:00'


class TestDateLikeSubclasses:
    """A date-like subclass defined in Python has a __dict__.

    The date branches therefore sit above the __dict__ reflection: reflecting first would walk
    the class attributes (min, max, resolution) instead of rendering the value, which fails.
    Libraries that fake the clock, such as freezegun, hand the SDK exactly these types.
    """

    def test_a_date_subclass_renders_as_a_date(self):
        class FakeDate(date):
            pass

        assert _wrap(FakeDate(2026, 10, 1)) == '2026-10-01'

    def test_a_datetime_subclass_renders_as_a_timestamp(self):
        class FakeDateTime(datetime):
            pass

        assert _wrap(FakeDateTime(2026, 10, 1, 13, 45, 30)) == '2026-10-01T13:45:30'


class TestNestedPaths:
    """A date must render the same wherever it appears in a request body."""

    def test_a_date_nested_in_an_object_renders_as_a_date(self):
        inner = _Holder()
        inner.value = date(2026, 10, 1)
        outer = _Holder()
        outer.value = inner

        assert _serialize(outer)['value']['value'] == '2026-10-01'

    def test_a_date_inside_a_list_renders_as_a_date(self):
        holder = _Holder()
        holder.value = date(2026, 10, 1)

        assert _serialize({'items': [holder]})['items'][0]['value'] == '2026-10-01'

    def test_a_date_as_a_bare_dict_value_renders_as_a_date(self):
        assert _serialize({'when': date(2026, 10, 1)})['when'] == '2026-10-01'


class TestObjectReflectionStillWorks:
    """Moving the date branches up must not change how ordinary objects serialize."""

    def test_an_object_is_still_reflected_into_its_attributes(self):
        holder = _Holder()
        holder.value = 'plain'

        assert _serialize(holder) == {'value': 'plain'}

    def test_key_transformations_are_still_applied(self):
        holder = _Holder()
        holder.three_ds = True

        assert _serialize(holder) == {'3ds': True}
