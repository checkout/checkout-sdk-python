from checkout_sdk.common.enums import Country


class Address:
    address_line1: str
    address_line2: str
    city: str
    state: str
    zip: str
    country: Country


class Phone:
    country_code: str
    number: str


class CustomerRequest:
    id: str
    email: str
    name: str
    phone: Phone


class Product:
    name: str
    quantity: int
    price: int
