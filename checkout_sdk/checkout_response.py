from collections.abc import Iterable, Mapping
from inspect import isfunction, ismethod


class ResponseWrapper:

    def __init__(self, http_metadata=None, data=None):
        if http_metadata is not None:
            setattr(self, 'http_metadata', http_metadata)
        if data is not None:
            if isinstance(data, str):
                setattr(self, 'contents', self._wrap(data))
            elif self._is_collection(data):
                setattr(self, 'items', self._wrap(data))
            else:
                for name, value in data.items():
                    setattr(self, name, self._wrap(value))

    def _wrap(self, value):
        if self._is_collection(value):
            return type(value)([self._wrap(v) for v in value])
        else:
            return ResponseWrapper(None, value) if isinstance(value, dict) else value

    @staticmethod
    def _is_collection(value):
        return isinstance(value, (tuple, list, set, frozenset))

    def dict(self):
        """
        Serializes the instance to a dictionary recursively.

        The result shall only contain JSON compatible data structures.

        Circular references shall be replaced with representations of appropriate
        JSON references (https://json-spec.readthedocs.io/reference.html).
        """
        return self._unwrap_object(self, cache={}, path=['#'])

    @staticmethod
    def _cache(method):
        def decorated_method(cls, data, cache, path):
            if id(data) in cache:
                for ref_path in cache[id(data)]:
                    if path[:len(ref_path)] == ref_path:
                        return {'$ref': '/'.join(ref_path)}

                cache[id(data)].append(path)

            else:
                cache[id(data)] = [path]

            return method(cls, data, cache, path)

        return decorated_method

    @classmethod
    @_cache
    def _unwrap_object(cls, data, cache, path):
        return {
            key: cls._unwrap(attr, cache, path + [key])
            for key in dir(data)
            if not key.startswith('__')
            and not cls._is_function(attr := getattr(data, key))
        }

    @classmethod
    def _unwrap(cls, data, cache, path):
        if isinstance(data, (str, int, float, bool, type(None))):
            return data

        elif isinstance(data, Mapping):
            return cls._unwrap_mapping(data, cache, path)

        elif isinstance(data, Iterable):
            return cls._unwrap_iterable(data, cache, path)

        else:
            return cls._unwrap_object(data, cache, path)

    @classmethod
    @_cache
    def _unwrap_mapping(cls, data: Mapping, cache, path):
        return {
            key: cls._unwrap(value, cache, path + [key])
            for key, value in data.items()
            if not cls._is_function(value)
        }

    @classmethod
    @_cache
    def _unwrap_iterable(cls, data: Iterable, cache, path):
        return [
            cls._unwrap(value, cache, path + [str(idx)])
            for idx, value in enumerate(data)
            if not cls._is_function(value)
        ]

    @staticmethod
    def _is_function(data):
        return isfunction(data) or ismethod(data)
