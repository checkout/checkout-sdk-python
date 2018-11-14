from checkout_sdk.common import RequestDTO


class Address(RequestDTO):
    def __init__(self, address_line1=None, address_line2=None,
                 city=None, state=None, zip=None, country=None):
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country
