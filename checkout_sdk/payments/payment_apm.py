from __future__ import absolute_import

from datetime import datetime

from checkout_sdk.common.common import Address, AccountHolder
from checkout_sdk.common.enums import PaymentSourceType, Country, Currency
from checkout_sdk.payments.payments import PaymentRequestSource, BillingPlan


class RequestIdealSource(PaymentRequestSource):
    bic: str
    description: str
    language: str

    def __init__(self):
        super().__init__(PaymentSourceType.IDEAL)


class RequestSofortSource(PaymentRequestSource):
    countryCode: Country
    languageCode: str

    def __init__(self):
        super().__init__(PaymentSourceType.SOFORT)


class RequestTamaraSource(PaymentRequestSource):
    billing_address: Address

    def __init__(self):
        super().__init__(PaymentSourceType.TAMARA)


class RequestPayPalSource(PaymentRequestSource):
    plan: BillingPlan

    def __init__(self):
        super().__init__(PaymentSourceType.PAYPAL)


class PaymentRequestWeChatPaySource(PaymentRequestSource):
    billing_address: Address

    def __init__(self):
        super().__init__(PaymentSourceType.WECHATPAY)


class RequestAlipayPlusSource(PaymentRequestSource):

    def __init__(self, source_type: PaymentSourceType):
        super().__init__(source_type)

    @staticmethod
    def request_alipay_plus_source():
        return RequestAlipayPlusSource(PaymentSourceType.ALIPAY_PLUS)

    @staticmethod
    def request_alipay_plus_cn_source():
        return RequestAlipayPlusSource(PaymentSourceType.ALIPAY_CN)

    @staticmethod
    def request_alipay_plus_hk_source():
        return RequestAlipayPlusSource(PaymentSourceType.ALIPAY_HK)

    @staticmethod
    def request_alipay_plus_gcash_source():
        return RequestAlipayPlusSource(PaymentSourceType.GCASH)

    @staticmethod
    def request_alipay_plus_dana_source():
        return RequestAlipayPlusSource(PaymentSourceType.DANA)

    @staticmethod
    def request_alipay_plus_kakao_pay_source():
        return RequestAlipayPlusSource(PaymentSourceType.KAKAOPAY)

    @staticmethod
    def request_alipay_plus_true_money_source():
        return RequestAlipayPlusSource(PaymentSourceType.TRUEMONEY)

    @staticmethod
    def request_alipay_plus_tng_source():
        return RequestAlipayPlusSource(PaymentSourceType.TNG)


class RequestAfterPaySource(PaymentRequestSource):
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(PaymentSourceType.AFTERPAY)


class RequestBenefitSource(PaymentRequestSource):

    def __init__(self):
        super().__init__(PaymentSourceType.BENEFIT)


class RequestEpsSource(PaymentRequestSource):
    purpose: str

    def __init__(self):
        super().__init__(PaymentSourceType.EPS)


class RequestIllicadoSource(PaymentRequestSource):
    billing_address: Address

    def __init__(self):
        super().__init__(PaymentSourceType.ILLICADO)


class RequestGiropaySource(PaymentRequestSource):
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(PaymentSourceType.GIROPAY)


class RequestMbwaySource(PaymentRequestSource):

    def __init__(self):
        super().__init__(PaymentSourceType.MBWAY)


class RequestQPaySource(PaymentRequestSource):
    quantity: int
    description: str
    language: str
    national_id: str

    def __init__(self):
        super().__init__(PaymentSourceType.QPAY)


class RequestBancontactSource(PaymentRequestSource):
    payment_country: Country
    account_holder_name: str
    billing_descriptor: str
    language: str

    def __init__(self):
        super().__init__(PaymentSourceType.BANCONTACT)


class RequestKnetSource(PaymentRequestSource):
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


class RequestMultiBancoSource(PaymentRequestSource):
    payment_country: Country
    account_holder_name: str
    billing_descriptor: str

    def __init__(self):
        super().__init__(PaymentSourceType.MULTIBANCO)


class RequestP24Source(PaymentRequestSource):
    payment_country: Country
    account_holder_name: str
    account_holder_email: str
    billing_descriptor: str

    def __init__(self):
        super().__init__(PaymentSourceType.P24)


class RequestPostFinanceSource(PaymentRequestSource):
    payment_country: Country
    account_holder_name: str
    billing_descriptor: str

    def __init__(self):
        super().__init__(PaymentSourceType.POSTFINANCE)


class RequestStcPaySource(PaymentRequestSource):
    def __init__(self):
        super().__init__(PaymentSourceType.STCPAY)


class RequestAlmaSource(PaymentRequestSource):
    billing_address: Address

    def __init__(self):
        super().__init__(PaymentSourceType.ALMA)


class RequestKlarnaSource(PaymentRequestSource):
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(PaymentSourceType.KLARNA)


class RequestFawrySource(PaymentRequestSource):
    description: str
    customer_profile_id: str
    customer_mobile: str
    customer_email: str
    expires_on: datetime
    products: list  # FawryProduct

    def __init__(self):
        super().__init__(PaymentSourceType.FAWRY)


class RequestCvConnectSource(PaymentRequestSource):
    billing_address: Address

    def __init__(self):
        super().__init__(PaymentSourceType.CVCONNECT)


class RequestTrustlySource(PaymentRequestSource):
    billing_address: Address

    def __init__(self):
        super().__init__(PaymentSourceType.TRUSTLY)


class RequestSepaSource(PaymentRequestSource):
    country: Country
    account_number: str
    bank_code: str
    currency: Currency
    mandate_id: str
    date_of_signature: str
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(PaymentSourceType.SEPA)
