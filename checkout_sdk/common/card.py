class Card:
    def __init__(self, card):
        self._card = card

    @property
    def id(self):
        return self._card['id']

    @property
    def scheme(self):
        return self._card['paymentMethod']

    @property
    def last4(self):
        return self._card['last4']

    @property
    def expiry_month(self):
        return self._card['expiryMonth']

    @property
    def expiry_year(self):
        return self._card['expiryYear']

    @property
    def name(self):
        return self._card['name']

    """
    ******************************************************************
    BACKWARDS COMPATIBILITY - Please use the snake_case versions above
    ******************************************************************
    """
    @property
    def expiryMonth(self):
        return self._card['expiryMonth']

    @property
    def expiryYear(self):
        return self._card['expiryYear']
