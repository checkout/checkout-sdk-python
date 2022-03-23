from __future__ import absolute_import

from enum import Enum

from checkout_sdk.common.enums import Country, PaymentSourceType
from checkout_sdk.payments.payments import RequestSource


class IntegrationType(str, Enum):
    DIRECT = 'direct',
    REDIRECT = 'redirect'


class BalotoPayer:
    name: str
    email: str


class FawryProduct:
    product_id: str
    quantity: int
    price: int
    description: str


class KlarnaCustomer:
    date_of_birth: str
    gender: str


class KlarnaProduct:
    name: str
    quantity: int
    unit_price: int
    tax_rate: int
    total_amount: int
    total_tax_amount: int


class Payer:
    name: str
    email: str
    document: str


class RequestBalotoSource(RequestSource):
    integration_type: IntegrationType = IntegrationType.REDIRECT
    country: Country
    description: str
    payer: BalotoPayer

    def __init__(self):
        super().__init__(PaymentSourceType.BALOTO)


class RequestBoletoSource(RequestSource):
    integration_type: IntegrationType = IntegrationType.REDIRECT
    country: Country
    description: str
    payer: Payer

    def __init__(self):
        super().__init__(PaymentSourceType.BOLETO)


class RequestFawrySource(RequestSource):
    description: str
    customer_mobile: str
    customer_email: str
    products: list  # FawryProduct

    def __init__(self):
        super().__init__(PaymentSourceType.FAWRY)


class RequestGiropaySource(RequestSource):
    purpose: str

    def __init__(self):
        super().__init__(PaymentSourceType.GIROPAY)


class RequestIdealSource(RequestSource):
    bic: str
    description: str
    language: str

    def __init__(self):
        super().__init__(PaymentSourceType.IDEAL)


class RequestKlarnaSource(RequestSource):
    authorization_token: str
    locale: str
    purchase_country: Country
    tax_amount: int
    billing_address: str
    customer: KlarnaCustomer
    products: list  # KlarnaProduct

    def __init__(self):
        super().__init__(PaymentSourceType.KLARNA)


class RequestOxxoSource(RequestSource):
    integration_type: IntegrationType = IntegrationType.REDIRECT
    country: Country
    payer: Payer
    description: str

    def __init__(self):
        super().__init__(PaymentSourceType.OXXO)


class RequestPagoFacilSource(RequestSource):
    integration_type: IntegrationType = IntegrationType.REDIRECT
    country: Country
    payer: Payer
    description: str

    def __init__(self):
        super().__init__(PaymentSourceType.PAGOFACIL)


class RequestRapiPagoSource(RequestSource):
    integration_type: IntegrationType = IntegrationType.REDIRECT
    country: Country
    payer: Payer
    description: str

    def __init__(self):
        super().__init__(PaymentSourceType.RAPIPAGO)


class RequestSepaSource(RequestSource):
    id: str

    def __init__(self):
        super().__init__(PaymentSourceType.ID)


class RequestSofortSource(RequestSource):

    def __init__(self):
        super().__init__(PaymentSourceType.SOFORT)
