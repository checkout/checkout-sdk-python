class ThreeDSEnrollment:
    def __init__(self, threeds):
        self._threeds = threeds

    @property
    def downgraded(self):
        return self._threeds.get('downgraded')

    @property
    def enrolled(self):
        return self._threeds.get('enrolled')

    @property
    def signature_valid(self):
        return self._threeds.get('signature_valid')

    @property
    def authentication_response(self):
        return self._threeds.get('authentication_response')

    @property
    def eci(self):
        return self._threeds.get('eci')

    @property
    def cryptogram(self):
        return self._threeds.get('cryptogram')

    @property
    def xid(self):
        return self._threeds.get('xid')
