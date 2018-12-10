# pylint: disable=too-few-public-methods


class ResponseDTO:
    def __init__(self, kvp):
        self._kvp = kvp
        self._create_attributes()

    def __getitem__(self, arg):
        return self._kvp.get(arg)

    # add class attributes to enable access via dot notation
    def _create_attributes(self):
        for (key, val) in self._kvp.items():
            if isinstance(val, dict):
                setattr(self, key, ResponseDTO(val))
            elif isinstance(val, list):
                setattr(self, key, [ResponseDTO(item) for item in val])
            else:
                setattr(self, key, val)

    @property
    def _attr_count(self):
        return len(self._kvp)
