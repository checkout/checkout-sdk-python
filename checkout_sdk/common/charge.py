class Charge:
    def __init__(self, charge):
        self._id = charge['id']
        self._chargeMode = charge['chargeMode']
        self._created = charge['created']
        self._email = charge['email']
        self._liveMode = charge['liveMode']
        self._status = charge['status']
        self._trackId = charge['trackId']
        self._value = charge['value']
        self._currency = charge['currency']
        self._responseCode = charge['responseCode']

    @property
    def id(self):
        return self._id

    @property
    def chargeMode(self):
        return self._chargeMode

    @property
    def created(self):
        return self._created

    @property
    def email(self):
        return self._email

    @property
    def liveMode(self):
        return self._liveMode

    @property
    def status(self):
        return self._status

    @property
    def trackId(self):
        return self._trackId

    @property
    def value(self):
        return self._value

    @property
    def currency(self):
        return self._currency

    @property
    def responseCode(self):
        return self._responseCode
