import inspect
import json


class JsonSerializer(json.JSONEncoder):
    _KEYS_TRANSFORMATIONS: dict = {'three_ds': '3ds',
                                   'account_holder_type': 'account-holder-type',
                                   'payment_network': 'payment-network',
                                   'from_': 'from'}

    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return self.default(obj.to_json())
        elif hasattr(obj, '__dict__'):
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
        elif hasattr(obj, 'strftime'):
            return self.default(obj.replace(microsecond=0).isoformat())
        return obj

    def apply_key_transformations(self, props):
        for key in self._KEYS_TRANSFORMATIONS:
            if key in props:
                props[self._KEYS_TRANSFORMATIONS[key]] = props.pop(key)

        return props
