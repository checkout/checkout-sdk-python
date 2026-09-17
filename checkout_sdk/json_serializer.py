import inspect
import json
from datetime import date, datetime


class JsonSerializer(json.JSONEncoder):
    _KEYS_TRANSFORMATIONS: dict = {'three_ds': '3ds',
                                   'account_holder_type': 'account-holder-type',
                                   'payment_network': 'payment-network',
                                   'from_': 'from',
                                   'if_match': 'if-match',
                                   'with_currency_account_id': 'withCurrencyAccountId',
                                   'balances_at': 'balancesAt'}

    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return self.default(obj.to_json())
        elif isinstance(obj, date) and not isinstance(obj, datetime):
            # A `format: date` value has no time component, so emit yyyy-MM-dd.
            #
            # datetime is excluded explicitly because it subclasses date and keeps its existing
            # full-timestamp rendering below. Without this branch a plain date reaches the
            # strftime branch and raises
            # TypeError: replace() got an unexpected keyword argument 'microsecond',
            # because date has no `microsecond` keyword on replace(). time is unaffected -- it
            # does accept `microsecond` -- and still falls through.
            return self.default(obj.isoformat())
        elif hasattr(obj, 'strftime'):
            return self.default(obj.replace(microsecond=0).isoformat())
        elif hasattr(obj, '__dict__'):
            # Checked after the date branches on purpose. A date/datetime/time SUBCLASS defined
            # in Python has a __dict__, so reflecting first would walk its class attributes
            # (min, max, resolution) instead of rendering the value, which fails outright.
            props = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith('__')
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            return self.default(self.apply_key_transformations(props))
        return obj

    def apply_key_transformations(self, props):
        for key in self._KEYS_TRANSFORMATIONS:
            if key in props:
                props[self._KEYS_TRANSFORMATIONS[key]] = props.pop(key)

        return props
