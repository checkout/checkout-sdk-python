from enum import Enum

from checkout_sdk.common.common import Phone, Address
from checkout_sdk.common.enums import Currency, ChallengeIndicator


class ChannelType(str, Enum):
    BROWSER = 'browser'
    APP = 'app'


class SdkInterfaceType(str, Enum):
    NATIVE = 'native'
    HTML = 'html'
    BOTH = 'both'


class ThreeDsMethodCompletion(str, Enum):
    Y = 'y'
    N = 'n'
    U = 'u'


class CompletionInfoType(str, Enum):
    HOSTED = 'hosted'
    NON_HOSTED = 'non_hosted'


class SessionSourceType(str, Enum):
    CARD = 'card'
    ID = 'id'
    TOKEN = 'token'
    NETWORK_TOKEN = 'network_token'


class AuthenticationType(str, Enum):
    REGULAR = 'regular'
    RECURRING = 'recurring'


class Category(str, Enum):
    PAYMENT = 'payment'
    NON_PAYMENT = 'nonPayment'


class TransactionType(str, Enum):
    GOODS_SERVICE = 'goods_service'
    CHECK_ACCEPTANCE = 'check_acceptance'
    ACCOUNT_FUNDING = 'account_funding'
    QUASHI_CARD_TRANSACTION = 'quashi_card_transaction'
    PREPAID_ACTIVATION_AND_LOAD = 'prepaid_activation_and_load'


class UIElements(str, Enum):
    TEXT = 'text'
    SINGLE_SELECT = 'single_select'
    MULTI_SELECT = 'multi_select'
    OOB = 'oob'
    HTML_OTHER = 'html_other'


class SessionScheme(str, Enum):
    VISA = 'visa'
    MASTERCARD = 'mastercard'
    JCB = 'jcb'
    AMEX = 'amex'
    DINERS = 'diners'
    CARTES_BANCAIRES = 'cartes_bancaires'


class AuthenticationMethod(str, Enum):
    NO_AUTHENTICATION = 'no_authentication'
    OWN_CREDENTIALS = 'own_credentials'
    FEDERATED_ID = 'federated_id'
    ISSUER_CREDENTIALS = 'issuer_credentials'
    THIRD_PARTY_AUTHENTICATION = 'third_party_authentication'
    FIDO = 'fido'


class DeliveryTimeframe(str, Enum):
    ELECTRONIC_DELIVERY = 'electronic_delivery'
    SAME_DAY = 'same_day'
    OVERNIGHT = 'overnight'
    TWO_DAY_OR_MORE = 'two_day_or_more'


class ShippingIndicator(str, Enum):
    VISA = 'visa'


class SdkEphemeralPublicKey:
    kty: str
    crv: str
    x: str
    y: str


class SessionAddress(Address):
    address_line3: str


class SessionMarketplaceData:
    sub_entity_id: str


class SessionsBillingDescriptor:
    name: str


# Channel
class ChannelData:
    channel: ChannelType

    def __init__(self, channel_p: ChannelType):
        self.channel = channel_p


class AppSession(ChannelData):
    sdk_app_id: str
    sdk_max_timeout: int
    sdk_ephem_pub_key: SdkEphemeralPublicKey
    sdk_reference_number: str
    sdk_encrypted_data: str
    sdk_transaction_id: str
    sdk_interface_type: SdkInterfaceType
    sdk_ui_elements: list  # UIElements

    def __init__(self):
        super().__init__(ChannelType.APP)


class BrowserSession(ChannelData):
    three_ds_method_completion: ThreeDsMethodCompletion
    accept_header: str
    java_enabled: bool
    language: str
    color_depth: str
    screen_height: str
    screen_width: str
    timezone: str
    user_agent: str
    ip_address: str

    def __init__(self):
        super().__init__(ChannelType.BROWSER)


# Completion
class Completion:
    type: CompletionInfoType

    def __init__(self, type_p: CompletionInfoType):
        self.type = type_p


class HostedCompletionInfo(Completion):
    callback_url: str
    success_url: str
    failure_url: bool

    def __init__(self):
        super().__init__(CompletionInfoType.HOSTED)


class NonHostedCompletionInfo(Completion):
    callback_url: str

    def __init__(self):
        super().__init__(CompletionInfoType.NON_HOSTED)


# Source
class SessionSource:
    type: SessionSourceType
    billing_address: SessionAddress
    home_phone: Phone
    mobile_phone: Phone
    work_phone: Phone
    email: str

    def __init__(self, type_p: SessionSourceType):
        self.type = type_p


class SessionCardSource(SessionSource):
    number: str
    expiry_month: int
    expiry_year: int
    name: str
    scheme: SessionScheme
    stored: bool
    store_for_future_use: bool

    def __init__(self):
        super().__init__(SessionSourceType.CARD)


class SessionIdSource(SessionSource):
    id: str

    def __init__(self):
        super().__init__(SessionSourceType.ID)


class SessionTokenSource(SessionSource):
    token: str
    store_for_future_use: bool

    def __init__(self):
        super().__init__(SessionSourceType.TOKEN)


class NetworkTokenSource(SessionSource):
    token: str
    expiry_month: int
    expiry_year: int
    name: str
    stored: bool

    def __init__(self):
        super().__init__(SessionSourceType.NETWORK_TOKEN)


class CardholderAccountInfo:
    purchase_count: int
    account_age: str
    add_card_attempts: int
    shipping_address_age: str
    account_name_matches_shipping_name: bool
    suspicious_account_activity: bool
    transactions_today: int
    authentication_method: AuthenticationMethod


class MerchantRiskInfo:
    delivery_email: str
    delivery_timeframe: DeliveryTimeframe
    is_preorder: bool
    is_reorder: bool
    shipping_indicator: ShippingIndicator


class Recurring:
    days_between_payments: int
    expiry: str


class Installment:
    number_of_payments: int
    days_between_payments: int
    expiry: str


class SessionRequest:
    source: SessionSource
    amount: int
    currency: Currency
    processing_channel_id: str
    marketplace: SessionMarketplaceData
    authentication_type: AuthenticationType
    authentication_category: Category
    account_info: CardholderAccountInfo
    challenge_indicator: ChallengeIndicator
    billing_descriptor: SessionsBillingDescriptor
    reference: str
    merchant_risk_info: MerchantRiskInfo
    prior_transaction_reference: str
    transaction_type: TransactionType
    shipping_address: SessionAddress
    shipping_address_matches_billing: bool
    completion: Completion
    channel_data: ChannelData
    recurring: Recurring
    installment: Installment


class ThreeDsMethodCompletionRequest:
    three_ds_method_completion: ThreeDsMethodCompletion
