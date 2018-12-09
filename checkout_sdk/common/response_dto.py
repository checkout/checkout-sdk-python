class ResponseDTO:
    def __init__(self, kvp):
        self._kvp = kvp
        self._create_attributes()

    # add class attributes to enable access via dot notation
    def _create_attributes(self):
        for (k, v) in self._kvp.items():
            if isinstance(v, dict):
                setattr(self, k, ResponseDTO(v))
            elif isinstance(v, list):
                dto_list = []
                for item in v:
                    dto_list.append(ResponseDTO(item))
                setattr(self, k, dto_list)
            else:
                setattr(self, k, v)

    @property
    def _attr_count(self):
        return len(self._kvp)
