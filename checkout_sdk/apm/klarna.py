from checkout_sdk.common.enums import PaymentSourceType, Country, Currency


class KlarnaProduct:
    name: str
    quantity: int
    unit_price: int
    tax_rate: int
    total_amount: int
    total_tax_amount: int


class KlarnaShippingInfo:
    shipping_company: str
    shipping_method: str
    tracking_number: str
    tracking_uri: str
    return_shipping_company: str
    return_tracking_number: str
    return_tracking_uri: str


class Klarna:
    description: str
    products: list  # KlarnaProduct
    shipping_info: list  # KlarnaShippingInfo
    shipping_delay: int


class CreditSessionRequest:
    purchase_country: Country
    currency: Currency
    locale: str
    amount: int
    tax_amount: int
    products: list  # KlarnaProduct


class OrderCaptureRequest:
    type: PaymentSourceType = PaymentSourceType.KLARNA
    amount: int
    reference: str
    metadata: dict
    klarna: Klarna
    shipping_info: KlarnaShippingInfo
    shipping_delay: int
