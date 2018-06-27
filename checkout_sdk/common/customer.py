class Customer:
    def __init__(self, id, email=None, name=None):
        self._id = id
        self._email = email
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def name(self):
        return self._name
