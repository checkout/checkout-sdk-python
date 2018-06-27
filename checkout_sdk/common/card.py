class Card:
    def __init__(self, card):
        self._id = card['id']
        self._scheme = card['paymentMethod']
        self._expiryMonth = card['expiryMonth']
        self._expiryYear = card['expiryYear']
        self._last4 = card['last4']
        self._name = card['name']

    @property
    def id(self):
        return self._id

    @property
    def scheme(self):
        return self._scheme

    @property
    def last4(self):
        return self._last4

    @property
    def expiryMonth(self):
        return self._expiryMonth

    @property
    def expiryYear(self):
        return self._expiryYear

    @property
    def name(self):
        return self._name
