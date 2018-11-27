class Charge:
    def __init__(self, charge):
        self._charge = charge

    @property
    def id(self):
        return self._charge['id']

    @property
    def charge_mode(self):
        return self._charge['chargeMode']

    @property
    def created(self):
        return self._charge['created']

    @property
    def email(self):
        return self._charge['email']

    @property
    def live_mode(self):
        return self._charge['liveMode']

    @property
    def status(self):
        return self._charge['status']

    @property
    def track_id(self):
        return self._charge['trackId']

    @property
    def value(self):
        return self._charge['value']

    @property
    def currency(self):
        return self._charge['currency']

    @property
    def response_code(self):
        return self._charge['responseCode']
