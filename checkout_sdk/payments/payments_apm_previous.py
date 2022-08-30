from __future__ import absolute_import

from datetime import datetime
from enum import Enum

from checkout_sdk.common.enums import Country, PaymentSourceType
from checkout_sdk.payments.payments_previous import RequestSource
from checkout_sdk.payments.payments import Payer


class IntegrationType(str, Enum):
    DIRECT = 'direct'
    REDIRECT = 'redirect'


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


class GiroPayInfoFields:
    label: str
    text: str


class RequestAlipaySource(RequestSource):
    def __init__(self):
        super().__init__(PaymentSourceType.ALIPAY)


class RequestBalotoSource(RequestSource):
    integration_type: IntegrationType = IntegrationType.REDIRECT
    country: Country
    description: str
    payer: Payer

    def __init__(self):
        super().__init__(PaymentSourceType.BALOTO)


class RequestBancontactSource(RequestSource):
    payment_country: Country
    account_holder_name: str
    billing_descriptor: str
    language: str

    def __init__(self):
        super().__init__(PaymentSourceType.BANCONTACT)


class RequestBenefitPaySource(RequestSource):
    integration_type: str

    def __init__(self):
        super().__init__(PaymentSourceType.BENEFITPAY)


class RequestBoletoSource(RequestSource):
    integration_type: IntegrationType = IntegrationType.REDIRECT
    country: Country
    description: str
    payer: Payer

    def __init__(self):
        super().__init__(PaymentSourceType.BOLETO)


class RequestEpsSource(RequestSource):
    purpose: str
    bic: str

    def __init__(self):
        super().__init__(PaymentSourceType.EPS)


class RequestFawrySource(RequestSource):
    description: str
    customer_profile_id: str
    customer_mobile: str
    customer_email: str
    expires_on: datetime
    products: list  # FawryProduct

    def __init__(self):
        super().__init__(PaymentSourceType.FAWRY)


class RequestGiropaySource(RequestSource):
    purpose: str
    bic: str
    info_fields: list  # GiroPayInfoFields

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
    auto_capture: bool
    billing_address: dict
    shipping_address: dict
    tax_amount: int
    products: list  # KlarnaProduct
    customer: KlarnaCustomer
    merchant_reference1: str
    merchant_reference2: str
    merchant_data: str
    attachment: dict
    custom_payment_method_ids: list

    def __init__(self):
        super().__init__(PaymentSourceType.KLARNA)


class RequestKnetSource(RequestSource):
    language: str
    user_defined_field1: str
    user_defined_field2: str
    user_defined_field3: str
    user_defined_field4: str
    user_defined_field5: str
    card_token: str
    ptlf: str

    def __init__(self):
        super().__init__(PaymentSourceType.KNET)


class RequestMultiBancoSource(RequestSource):
    payment_country: Country
    account_holder_name: str
    billing_descriptor: str

    def __init__(self):
        super().__init__(PaymentSourceType.MULTIBANCO)


class RequestOxxoSource(RequestSource):
    integration_type: IntegrationType = IntegrationType.REDIRECT
    country: Country
    payer: Payer
    description: str

    def __init__(self):
        super().__init__(PaymentSourceType.OXXO)


class RequestP24Source(RequestSource):
    payment_country: Country
    account_holder_name: str
    account_holder_email: str
    billing_descriptor: str

    def __init__(self):
        super().__init__(PaymentSourceType.P24)


class RequestPagoFacilSource(RequestSource):
    integration_type: IntegrationType = IntegrationType.REDIRECT
    country: Country
    payer: Payer
    description: str

    def __init__(self):
        super().__init__(PaymentSourceType.PAGOFACIL)


class RequestPayPalSource(RequestSource):
    invoice_number: str
    recipient_name: str
    logo_url: str
    stc: dict

    def __init__(self):
        super().__init__(PaymentSourceType.PAYPAL)


class RequestPoliSource(RequestSource):
    def __init__(self):
        super().__init__(PaymentSourceType.POLI)


class RequestQPaySource(RequestSource):
    quantity: int
    description: str
    language: str
    national_id: str

    def __init__(self):
        super().__init__(PaymentSourceType.QPAY)


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
    countryCode: Country
    languageCode: str

    def __init__(self):
        super().__init__(PaymentSourceType.SOFORT)
