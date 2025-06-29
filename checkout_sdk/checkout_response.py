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
        return self._unwrap_object(self, paths_by_id={}, path=['#'])

    @staticmethod
    def _handle_circular_ref(method):
        def decorated_method(cls, data, paths_by_id, path):
            if id(data) in paths_by_id:
                for ref_path in paths_by_id[id(data)]:
                    if path[:len(ref_path)] == ref_path:
                        return {'$ref': '/'.join(ref_path)}

                paths_by_id[id(data)].append(path)

            else:
                paths_by_id[id(data)] = [path]

            return method(cls, data, paths_by_id, path)

        return decorated_method

    @classmethod
    @_handle_circular_ref
    def _unwrap_object(cls, data, paths_by_id, path):
        return {
            key: cls._unwrap(getattr(data, key), paths_by_id, path + [key])
            for key in dir(data)
            if not key.startswith('__')
            and not cls._is_function(getattr(data, key))
        }

    @classmethod
    def _unwrap(cls, data, paths_by_id, path):
        if isinstance(data, (str, int, float, bool, type(None))):
            return data

        elif isinstance(data, Mapping):
            return cls._unwrap_mapping(data, paths_by_id, path)

        elif isinstance(data, Iterable):
            return cls._unwrap_iterable(data, paths_by_id, path)

        else:
            return cls._unwrap_object(data, paths_by_id, path)

    @classmethod
    @_handle_circular_ref
    def _unwrap_mapping(cls, data: Mapping, paths_by_id, path):
        return {
            key: cls._unwrap(value, paths_by_id, path + [key])
            for key, value in data.items()
            if not cls._is_function(value)
        }

    @classmethod
    @_handle_circular_ref
    def _unwrap_iterable(cls, data: Iterable, paths_by_id, path):
        return [
            cls._unwrap(value, paths_by_id, path + [str(idx)])
            for idx, value in enumerate(data)
            if not cls._is_function(value)
        ]

    @staticmethod
    def _is_function(data):
        return isfunction(data) or ismethod(data)
