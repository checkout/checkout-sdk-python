from __future__ import absolute_import

from datetime import datetime

from checkout_sdk.common.common import Address, AccountHolder, AccountHolderIdentification
from checkout_sdk.common.enums import PaymentSourceType, Country, Currency, \
    SepaMandateType, AccountHolderType, InstrumentAccountHolderType, AchSourceAccountType
from checkout_sdk.payments.payments import PaymentRequestSource, BillingPlan, PaymentMethodDetails
from checkout_sdk.tokens.tokens import ApplePayTokenData


class SepaSourceBillingAddress:
    """The account holder's billing address on a SEPA payment source.

    Every property is required. Deliberately not Address, which also declares a state that this
    position does not accept. address_line2 max 10, city max 35, zip max 16, country max 2.
    """
    address_line1: str
    address_line2: str
    city: str
    zip: str
    country: Country


class SepaSourceAccountHolder:
    """The account holder's personal information on a SEPA payment source.

    Maps the account_holder object of PaymentRequestSEPAV4Source. Deliberately not AccountHolder,
    which is a 16-property superset. The property names match instruments.SepaAccountHolder, but the
    two positions differ: only billing_address is required here, where the instrument requires the
    names too, and the specification declares type capitalized here against lowercase on the
    instrument. Send type lowercase - every other account-holder-type position is lowercase and
    every other Checkout.com SDK sends lowercase. Pending confirmation from the API owners.

    first_name, last_name and company_name are each max 50 characters.
    """
    billing_address: SepaSourceBillingAddress
    first_name: str
    last_name: str
    company_name: str
    type: InstrumentAccountHolderType


class AchSourceAccountHolder:
    """The account holder's details on an ACH payment source.

    Maps the AccountHolderAch schema exactly. Deliberately not AccountHolder, which is a 16-property
    superset, and distinct from instruments.AchAccountHolder, which declares only four properties -
    the instrument schema has no billing address, date of birth or identification.

    type, first_name and last_name are required. billing_address reuses Address because that
    schema's six properties are exactly what this position references. identification reuses
    AccountHolderIdentification, which carries one extra property, date_of_expiry, that this
    position does not declare - do not set it.
    """
    type: AccountHolderType
    first_name: str
    last_name: str
    company_name: str
    billing_address: Address
    date_of_birth: str
    identification: AccountHolderIdentification


class RequestBacsSource(PaymentRequestSource):
    r"""Bacs Direct Debit source.

    id is the Bacs Direct Debit instrument ID and matches the pattern ^(src)_(\w{26})$.
    """
    id: str

    def __init__(self):
        super().__init__(PaymentSourceType.BACS)


class RequestIdealSource(PaymentRequestSource):
    description: str
    language: str

    def __init__(self):
        super().__init__(PaymentSourceType.IDEAL)


# Deprecated: Sofort was removed from the Checkout.com API. This source no longer functions.
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
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(PaymentSourceType.EPS)


class RequestIllicadoSource(PaymentRequestSource):
    billing_address: Address

    def __init__(self):
        super().__init__(PaymentSourceType.ILLICADO)


# Deprecated: Giropay was removed from the Checkout.com API. This source no longer functions.
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
    token_type: str
    token_data: ApplePayTokenData
    payment_method_details: PaymentMethodDetails

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
    """SEPA Direct Debit source, legacy shape.

    Superseded by RequestSepaV4Source, which matches PaymentRequestSEPAV4Source exactly. Prefer that
    class for new code: this one carries a bank_code that no SEPA schema in the specification
    declares, and omits mandate_type. Both construct PaymentSourceType.SEPA, so they are
    interchangeable on the wire apart from those two fields.

    date_of_signature is a yyyy-MM-dd string.
    """
    country: Country
    account_number: str
    # Not declared by PaymentRequestSEPAV4Source. No SEPA schema in the specification declares a
    # bank code, and the SEPA source is identified by IBAN through account_number. Retained
    # for retro-compatibility purposes only. Possibly an obsoleted field.
    bank_code: str
    currency: Currency
    mandate_id: str
    date_of_signature: str
    account_holder: SepaSourceAccountHolder

    def __init__(self):
        super().__init__(PaymentSourceType.SEPA)


class RequestAchSource(PaymentRequestSource):
    account_type: AchSourceAccountType
    country: Country
    account_number: str
    bank_code: str
    account_holder: AchSourceAccountHolder

    def __init__(self):
        super().__init__(PaymentSourceType.ACH)


class RequestBizumSource(PaymentRequestSource):
    mobile_number: str

    def __init__(self):
        super().__init__(PaymentSourceType.BIZUM)


class RequestOctopusSource(PaymentRequestSource):
    def __init__(self):
        super().__init__(PaymentSourceType.OCTOPUS)


class RequestPlaidSource(PaymentRequestSource):
    token: str
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(PaymentSourceType.PLAID)


class RequestSequraSource(PaymentRequestSource):
    billing_address: Address

    def __init__(self):
        super().__init__(PaymentSourceType.SEQURA)


class RequestMobilePaySource(PaymentRequestSource):

    def __init__(self):
        super().__init__(PaymentSourceType.MOBILEPAY)


class RequestPayNowSource(PaymentRequestSource):

    def __init__(self):
        super().__init__(PaymentSourceType.PAYNOW)


class SwishBillingDescriptor:
    name: str


class RequestSwishSource(PaymentRequestSource):
    payment_country: Country
    account_holder: AccountHolder
    billing_descriptor: SwishBillingDescriptor

    def __init__(self):
        super().__init__(PaymentSourceType.SWISH)


class RequestTwintSource(PaymentRequestSource):

    def __init__(self):
        super().__init__(PaymentSourceType.TWINT)


class RequestVippsSource(PaymentRequestSource):

    def __init__(self):
        super().__init__(PaymentSourceType.VIPPS)


class RequestSepaV4Source(PaymentRequestSource):
    """SEPA Direct Debit source.

    Matches PaymentRequestSEPAV4Source exactly. Use this rather than RequestSepaSource, which is the
    legacy shape. date_of_signature is a yyyy-MM-dd string.
    """
    country: Country
    account_number: str
    currency: Currency
    mandate_id: str
    mandate_type: SepaMandateType
    date_of_signature: str
    account_holder: SepaSourceAccountHolder

    def __init__(self):
        super().__init__(PaymentSourceType.SEPA)


class RequestBlikSource(PaymentRequestSource):
    partner_agreement_id: str

    def __init__(self):
        super().__init__(PaymentSourceType.BLIK)
