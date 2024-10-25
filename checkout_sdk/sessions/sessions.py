from datetime import datetime
from enum import Enum

from checkout_sdk.common.common import Phone, Address
from checkout_sdk.common.enums import Currency, ChallengeIndicator, CardholderAccountAgeIndicatorType, \
    AccountChangeIndicatorType, AccountPasswordChangeIndicatorType, AccountTypeCardProductType


class ChannelType(str, Enum):
    APP = 'app'
    BROWSER = 'browser'
    MERCHANT_INITIATED = 'merchant_initiated'


class SdkInterfaceType(str, Enum):
    BOTH = 'both'
    HTML = 'html'
    NATIVE = 'native'


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
    ADD_CARD = 'add_card'
    INSTALLMENT = 'installment'
    MAINTAIN_CARD = 'maintain_card'
    RECURRING = 'recurring'
    REGULAR = 'regular'


class Category(str, Enum):
    PAYMENT = 'payment'
    NON_PAYMENT = 'nonPayment'


class TransactionType(str, Enum):
    ACCOUNT_FUNDING = 'account_funding'
    CHECK_ACCEPTANCE = 'check_acceptance'
    GOODS_SERVICE = 'goods_service'
    PREPAID_ACTIVATION_AND_LOAD = 'prepaid_activation_and_load'
    QUASHI_CARD_TRANSACTION = 'quashi_card_transaction'


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
    FEDERATED_ID = 'federated_id'
    FIDO = 'fido'
    ISSUER_CREDENTIALS = 'issuer_credentials'
    NO_AUTHENTICATION = 'no_authentication'
    OWN_CREDENTIALS = 'own_credentials'
    THIRD_PARTY_AUTHENTICATION = 'third_party_authentication'


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
    three_ds_method_completion: ThreeDsMethodCompletion = ThreeDsMethodCompletion.U
    accept_header: str
    java_enabled: bool
    javascript_enabled: bool
    language: str
    color_depth: str
    screen_height: str
    screen_width: str
    timezone: str
    user_agent: str
    ip_address: str

    def __init__(self):
        super().__init__(ChannelType.BROWSER)


class RequestType(str, Enum):
    ACCOUNT_VERIFICATION = "account_verification"
    ADD_CARD = "add_card"
    INSTALLMENT_TRANSACTION = "installment_transaction"
    MAIL_ORDER = "mail_order"
    MAINTAIN_CARD_INFORMATION = "maintain_card_information"
    OTHER_PAYMENT = "other_payment"
    RECURRING_TRANSACTION = "recurring_transaction"
    SPLIT_OR_DELAYED_SHIPMENT = "split_or_delayed_shipment"
    TELEPHONE_ORDER = "telephone_order"
    TOP_UP = "top_up"
    WHITELIST_STATUS_CHECK = "whitelist_status_check"


class MerchantInitiatedSession(ChannelData):
    request_type: RequestType

    def __init__(self):
        super().__init__(ChannelType.MERCHANT_INITIATED)


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
    challenge_notification_url: str

    def __init__(self):
        super().__init__(CompletionInfoType.NON_HOSTED)


# Source
class SessionSource:
    type: SessionSourceType
    scheme: SessionScheme
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
    stored: bool = False
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


class ThreeDsReqAuthMethod(str, Enum):
    NoThreedsRequestorAuthenticationOccurred = "no_threeds_requestor_authentication_occurred"
    Three3dsRequestorOwnCredentials = "three3ds_requestor_own_credentials"
    FederatedId = "federated_id"
    IssuerCredentials = "issuer_credentials"
    ThirdPartyAuthentication = "third_party_authentication"
    FidoAuthenticator = "fido_authenticator"
    FidoAuthenticatorFidoAssuranceDataSigned = "fido_authenticator_fido_assurance_data_signed"
    SrcAssuranceData = "src_assurance_data"


class ThreeDsRequestorAuthenticationInfo:
    three_ds_req_auth_method: ThreeDsReqAuthMethod
    three_ds_req_auth_timestamp: datetime
    three_ds_req_auth_data: str


class CardholderAccountInfo:
    purchase_count: int
    account_age: str
    add_card_attempts: int
    shipping_address_age: str
    account_name_matches_shipping_name: bool
    suspicious_account_activity: bool
    transactions_today: int
    # @deprecated This property will be removed in the future, and should not be used.
    authentication_method: AuthenticationMethod
    cardholder_account_age_indicator: CardholderAccountAgeIndicatorType
    account_change: datetime
    account_change_indicator: AccountChangeIndicatorType
    account_date: datetime
    account_password_change: str
    account_password_change_indicator: AccountPasswordChangeIndicatorType
    transactions_per_year: int
    payment_account_age: datetime
    shipping_address_usage: datetime
    account_type: AccountTypeCardProductType
    account_id: str
    three_ds_requestor_authentication_info: ThreeDsRequestorAuthenticationInfo


class ReorderItemsIndicatorType(str, Enum):
    FIRST_TIME_ORDERED = "first_time_ordered"
    REORDERED = "reordered"


class PreOrderPurchaseIndicatorType(str, Enum):
    FUTURE_AVAILABILITY = "future_availability"
    MERCHANDISE_AVAILABLE = "merchandise_available"


class MerchantRiskInfo:
    delivery_email: str
    delivery_timeframe: DeliveryTimeframe
    is_preorder: bool
    is_reorder: bool
    shipping_indicator: ShippingIndicator
    reorder_items_indicator: ReorderItemsIndicatorType
    pre_order_purchase_indicator: PreOrderPurchaseIndicatorType
    pre_order_date: datetime
    gift_card_amount: str
    gift_card_currency: str
    gift_card_count: str


class Recurring:
    days_between_payments: int = 1
    expiry: str = '99991231'


class Installment:
    number_of_payments: int
    days_between_payments: int = 1
    expiry: str = '99991231'


class OptimizedProperties:
    field: str
    original_value: str
    optimized_value: str


class Optimization:
    optimized: bool
    framework: str
    optimized_properties: list  # OptimizedProperties


class InitialTransaction:
    acs_transaction_id: str
    authentication_method: str
    authentication_timestamp: str
    authentication_data: str
    initial_session_id: str


class SessionRequest:
    source: SessionSource = SessionCardSource()
    amount: int
    currency: Currency
    processing_channel_id: str
    marketplace: SessionMarketplaceData
    authentication_type: AuthenticationType = AuthenticationType.REGULAR
    authentication_category: Category = Category.PAYMENT
    account_info: CardholderAccountInfo
    challenge_indicator: ChallengeIndicator = ChallengeIndicator.NO_PREFERENCE
    billing_descriptor: SessionsBillingDescriptor
    reference: str
    merchant_risk_info: MerchantRiskInfo
    prior_transaction_reference: str
    transaction_type: TransactionType = TransactionType.GOODS_SERVICE
    shipping_address: SessionAddress
    shipping_address_matches_billing: bool
    completion: Completion
    channel_data: ChannelData
    recurring: Recurring
    installment: Installment
    optimization: Optimization
    initial_transaction: InitialTransaction


class ThreeDsMethodCompletionRequest:
    three_ds_method_completion: ThreeDsMethodCompletion
