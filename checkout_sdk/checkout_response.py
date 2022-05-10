class ResponseWrapper:

    def __init__(self, http_metadata=None, data=None):
        if http_metadata is not None:
            setattr(self, 'http_metadata', http_metadata)
        if data is not None:
            if self._is_collection(data):
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
