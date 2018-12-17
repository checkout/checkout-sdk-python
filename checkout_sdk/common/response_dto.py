import checkout_sdk


class ResponseDTO:
    def __init__(self, kvp=None,
                 read_only=checkout_sdk.default_response_immutable):
        if kvp is not None and not isinstance(kvp, dict):
            raise TypeError('Dictionary expected')

        # load the DTO
        self._read_only = False
        self._kvp = {}
        if kvp is not None:
            for (k, v) in kvp.items():
                # calls __setitem__ further below
                self[k] = v

        # make the DTO immutable if required
        self._read_only = read_only

    # only called for attributes which are not declared directly
    def __getattr__(self, k):
        # this will in turn call __getitem__
        # we catch KeyError to raise AttributeError
        # this maintains expected behaviour
        #   when used with getattr() and hasattr()
        try:
            return self[k]
        except KeyError:
            raise AttributeError

    # KeyError if key does not exist
    def __getitem__(self, k):
        return self._kvp[k]

    # safer option with fallback option (None as default)
    def get(self, k, d=None):
        return self._kvp.get(k, d)

    def __setattr__(self, k, v):
        # avoiding infinite loop here
        # private attributes are registered via the super class (`object`)
        if k[0] == '_':
            super().__setattr__(k, v)
        else:
            # this will in turn call __setitem__
            try:
                self[k] = v
            except KeyError as err:
                raise AttributeError(err)

    def __setitem__(self, k, v):
        if self._read_only:
            raise KeyError(
                '{} is read-only.'.format(self.__class__.__name__))
        else:
            if isinstance(v, dict):
                self._kvp[k] = ResponseDTO(v, self._read_only)
            elif isinstance(v, list):
                self._kvp[k] = [ResponseDTO(item, self._read_only)
                                for item in v]
            else:
                self._kvp[k] = v

    def __len__(self):
        return len(self._kvp)
