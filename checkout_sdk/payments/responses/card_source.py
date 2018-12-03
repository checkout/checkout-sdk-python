from checkout_sdk.common import Address, Phone


class CardSource:
    def __init__(self, card):
        self._card = card

        billing_address = self._card.get('billing_address')
        self._billing_address = Address(
            address_line1=billing_address.get('address_line_1'),
            address_line2=billing_address.get('address_line_2'),
            city=billing_address.get('city'),
            state=billing_address.get('state'),
            zip=billing_address.get('zip'),
            country=billing_address.get('country')
        ) if billing_address is not None else None

        phone = self._card.get('phone')
        self._phone = Phone(
            country_code=phone.get('country_code'),
            number=phone.get('number')
        ) if phone is not None else None

    @property
    def id(self):
        return self._card.get('id')

    @property
    def type(self):
        return self._card.get('type')

    @property
    def billing_address(self):
        return self._billing_address

    @property
    def phone(self):
        return self._phone

    @property
    def expiry_month(self):
        return self._card.get('expiry_month')

    @property
    def expiry_year(self):
        return self._card.get('expiry_year')

    @property
    def name(self):
        return self._card.get('name')

    @property
    def scheme(self):
        return self._card.get('scheme')

    @property
    def last4(self):
        return self._card.get('last4')

    @property
    def fingerprint(self):
        return self._card.get('fingerprint')

    @property
    def bin(self):
        return self._card.get('bin')

    @property
    def card_type(self):
        return self._card.get('card_type')

    @property
    def card_category(self):
        return self._card.get('card_category')

    @property
    def issuer(self):
        return self._card.get('issuer')

    @property
    def issuer_country(self):
        return self._card.get('issuer_country')

    @property
    def product_id(self):
        return self._card.get('product_id')

    @property
    def product_type(self):
        return self._card.get('product_type')

    @property
    def avs_check(self):
        return self._card.get('avs_check')

    @property
    def cvv_check(self):
        return self._card.get('cvv_check')
