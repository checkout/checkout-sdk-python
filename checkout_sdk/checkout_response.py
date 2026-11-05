from collections.abc import Iterable, Mapping


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

        Note: attributes prefixed with a single underscore are included in the output.
        If you store sensitive data on underscore-prefixed attributes,
        filter the result before logging or persisting.
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
            attr: cls._unwrap(getattr(data, attr), paths_by_id, path + [attr])
            for attr in dir(data)
            if not attr.startswith('__')
            and not cls._is_executable_attr(data, attr)
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
            if not cls._is_executable(value)
        }

    @classmethod
    @_handle_circular_ref
    def _unwrap_iterable(cls, data: Iterable, paths_by_id, path):
        return [
            cls._unwrap(value, paths_by_id, path + [str(idx)])
            for idx, value in enumerate(data)
            if not cls._is_executable(value)
        ]

    @classmethod
    def _is_executable_attr(cls, data, attr: str) -> bool:
        return cls._is_executable(getattr(type(data), attr, None))

    @staticmethod
    def _is_executable(data) -> bool:
        return hasattr(data, '__get__')
