class ResponseDTO:
    def __init__(self, kvp):
        self._kvp = kvp
        self._create_attributes()

    # add class attributes to enable access via dot notation
    def _create_attributes(self):
        for key in self._kvp:
            val = self._kvp[key]
            if isinstance(val, dict):
                setattr(self, key, ResponseDTO(val))
            elif isinstance(val, list):
                dto_list = []
                for item in val:
                    dto_list.append(ResponseDTO(item))
                setattr(self, key, dto_list)
            else:
                setattr(self, key, val)

    @property
    def _attr_count(self):
        return len(self._kvp)
