class Customer:
    def __init__(self, customer):
        self._customer = customer

    @property
    def id(self):
        return self._customer.get('id')

    @property
    def email(self):
        return self._customer.get('email')

    @property
    def name(self):
        return self._customer.get('name')
