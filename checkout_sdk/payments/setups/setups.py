from __future__ import absolute_import
from datetime import datetime
from enum import Enum

from checkout_sdk.common.common import Address, Phone
from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.payments import PaymentType, ShippingDetails


# Enums
class PaymentMethodInitialization(str, Enum):
    """The initialization state of a payment method on a Payment Setup."""
    DISABLED = 'disabled'
    ENABLED = 'enabled'


# Shared payment-method enums
class TerminalType(str, Enum):
    """The client-side terminal type of the wallet payment methods."""
    WEB = 'web'
    WAP = 'wap'
    APP = 'app'


class OsType(str, Enum):
    """An operating system type. Used by the wallet payment methods and by the customer device."""
    ANDROID = 'android'
    IOS = 'ios'


# Customer entities
class CustomerEmail:
    """Details of the customer's email."""
    # The customer's email address.
    # [Optional]
    address: str
    # Specifies whether the customer's email address is verified.
    # [Optional]
    verified: bool


class CustomerDeviceClient(str, Enum):
    """The type of client the customer uses to initiate the payment."""
    WEB = 'web'
    MOBILE_WEB = 'mobile_web'
    APP = 'app'


class CustomerDevice:
    """Details of the customer's device."""
    # The locale of the device. For example, en_GB.
    # [Optional]
    locale: str
    # A unique identifier for the customer's device.
    # [Optional]
    fingerprint: str
    # The customer's device IPv4 address, used by some payment methods for risk and
    # eligibility checks.
    # [Optional]
    ipv4: str
    # The customer's device IPv6 address, used by some payment methods for risk and
    # eligibility checks.
    # [Optional]
    ipv6: str
    # The type of client the customer uses to initiate the payment. Required when using
    # Cash App Pay.
    # [Optional]
    client: CustomerDeviceClient
    # The operating system of the customer's device.
    # [Optional]
    os: OsType


class MerchantAccount:
    """Details of the account the customer holds with the merchant."""
    # The merchant's unique identifier for the customer's account.
    # [Optional]
    id: str
    # The date the customer registered their account with the merchant.
    # [Optional]
    # Format: date (yyyy-MM-dd)
    registration_date: str
    # The date the customer's account with the merchant was last modified.
    # [Optional]
    # Format: date (yyyy-MM-dd)
    last_modified: str
    # Specifies if the customer is a returning customer.
    # [Optional]
    returning_customer: bool
    # The date of the customer's first transaction.
    # [Optional]
    # Format: date (yyyy-MM-dd)
    first_transaction_date: str
    # The date of the customer's most recent transaction.
    # [Optional]
    # Format: date (yyyy-MM-dd)
    last_transaction_date: str
    # The total number of orders made by the customer.
    # [Optional]
    total_order_count: int
    # The payment amount of the customer's most recent transaction.
    # [Optional]
    last_payment_amount: int


class Customer:
    """The customer's details."""
    # Details of the customer's email.
    # [Optional]
    email: CustomerEmail
    # The customer's full name.
    # [Optional]
    # max 100 characters
    name: str
    # The customer's phone number. country_code is min 1, max 7 characters; number is
    # min 6, max 25 characters.
    # [Optional]
    phone: Phone
    # Details of the customer's device.
    # [Optional]
    device: CustomerDevice
    # Details of the account the customer holds with the merchant.
    # [Optional]
    merchant_account: MerchantAccount
    # The two-letter ISO country code of the customer for this payment.
    # [Optional]
    # min 2 characters, max 2 characters
    country: str
    # The unique identifier of the customer.
    # [Optional]
    id: str
    # The customer's tax identification number.
    # [Optional]
    tax_number: str


# Payment Method Common entities
class PaymentMethodAction:
    """The next available action for the Klarna, PayPal or instrument payment method.

    The Cash App and Pay by Bank methods have their own action types (CashAppAction,
    PayByBankAction), because their actions carry different properties.
    """
    # The type of action.
    # [Optional]
    # readOnly
    # Enum: "sdk" (Klarna, PayPal) "set_instrument" (instrument)
    type: str
    # The client token for the Klarna SDK.
    # [Optional]
    # readOnly
    client_token: str
    # The session ID.
    # [Optional]
    # readOnly
    session_id: str
    # The PayPal order ID to use with the PayPal SDK.
    # [Optional]
    # readOnly
    order_id: str


class PaymentMethodOption:
    """A payment method option. Not present in the current Payment Setup schema."""
    # The identifier of the payment method option.
    # [Optional]
    id: str
    # The list of error codes or indicators that highlight missing or invalid information.
    # [Optional]
    flags: list  # list of str
    # The next available action for the payment method option.
    # [Optional]
    action: PaymentMethodAction


class PaymentMethodOptions:
    """The payment method options. Not present in the current Payment Setup schema."""
    # The SDK payment method option.
    # [Optional]
    sdk: PaymentMethodOption
    # The pay in full payment method option.
    # [Optional]
    pay_in_full: PaymentMethodOption
    # The installments payment method option.
    # [Optional]
    installments: PaymentMethodOption
    # The pay now payment method option.
    # [Optional]
    pay_now: PaymentMethodOption


class PaymentMethodBase:
    """Base for payment methods that carry status, flags and the writable initialization field
    (swagger PaymentSetupPaymentMethod plus PaymentMethodInitialization)."""
    # The payment method status.
    # [Optional]
    # readOnly
    # Enum: "unavailable" "action_required" "ready" "initialization_required" "invalid"
    status: str
    # The list of error codes or indicators that highlight missing or invalid information.
    # [Optional]
    # readOnly
    flags: list  # list of str
    # The initialization state of the payment method. When you create a Payment Setup, this
    # defaults to disabled.
    # [Optional]
    # Default: "disabled"
    initialization: PaymentMethodInitialization = PaymentMethodInitialization.DISABLED


# Klarna entities
class KlarnaAccountHolder:
    """The account holder details returned by Klarna after the shopper completes verification."""
    # The full name of the account holder.
    # [Optional]
    # readOnly
    name: str


class Klarna(PaymentMethodBase):
    """The Klarna payment method's details and configuration."""

    def __init__(self):
        super().__init__()
        # The account holder details returned by Klarna after the shopper completes
        # verification.
        # [Optional]
        # readOnly
        self.account_holder: KlarnaAccountHolder
        # The payment method options. Not present in the current Klarna schema.
        # [Optional]
        self.payment_method_options: PaymentMethodOptions


# Stcpay entities
class Stcpay(PaymentMethodBase):
    """The stc pay payment method's details and configuration."""

    def __init__(self):
        super().__init__()
        # The one-time password (OTP) for stc pay.
        # [Optional]
        self.otp: str
        # The payment method options. Not present in the current stc pay schema.
        # [Optional]
        self.payment_method_options: PaymentMethodOptions


# Tabby entities
class Tabby(PaymentMethodBase):
    """The Tabby payment method's details and configuration."""
    # The available payment types for Tabby. For example, installments.
    # [Optional]
    payment_types: list  # list of str

    def __init__(self):
        super().__init__()
        # The payment method options. Not present in the current Tabby schema.
        # [Optional]
        self.payment_method_options: PaymentMethodOptions


# Bizum entities
class Bizum(PaymentMethodBase):
    """The Bizum payment method's details and configuration."""

    def __init__(self):
        super().__init__()
        # The payment method options. Not present in the current Bizum schema.
        # [Optional]
        self.payment_method_options: PaymentMethodOptions


class Blik(PaymentMethodBase):
    """The Blik payment method's details and configuration."""
    # The 6-digit BLIK code generated by the customer's banking app.
    # [Optional]
    # ^[0-9]{6}$
    partner_code: str


class PaypalUserAction(str, Enum):
    """The user action for the PayPal widget."""
    PAY_NOW = 'pay_now'
    CONTINUE = 'continue'


class PaypalShippingPreference(str, Enum):
    """Where to obtain the shipping information."""
    NO_SHIPPING = 'no_shipping'
    GET_FROM_FILE = 'get_from_file'
    SET_PROVIDED_ADDRESS = 'set_provided_address'


class Paypal(PaymentMethodBase):
    """The PayPal payment method's details and configuration."""
    # The user action for the PayPal widget. pay_now redirects the customer to finalize the
    # payment immediately; continue lets them review the order before paying.
    # [Optional]
    user_action: PaypalUserAction
    # The brand name to display in the PayPal checkout experience.
    # [Optional]
    # max 127 characters
    brand_name: str
    # Where to obtain the shipping information.
    # [Optional]
    shipping_preference: PaypalShippingPreference
    # The next available action for the payment method.
    # [Optional]
    # readOnly
    action: PaymentMethodAction


# Base for payment methods that only expose status/flags (swagger PaymentSetupPaymentMethod).
# Distinct from PaymentMethodBase, which also carries the writable `initialization` field.
class PaymentSetupPaymentMethod:
    """Base for payment methods that expose only status and flags (swagger
    PaymentSetupPaymentMethod)."""
    # The payment method status.
    # [Optional]
    # readOnly
    # Enum: "unavailable" "action_required" "ready" "initialization_required" "invalid"
    status: str
    # The list of error codes or indicators that highlight missing or invalid information.
    # [Optional]
    # readOnly
    flags: list  # list of str


class KnetLanguage(str, Enum):
    """The customer's preferred KNET language, as an ISO 639-1 code."""
    EN = 'en'
    AR = 'ar'


class PaymentSetupAccountHolderType(str, Enum):
    """The type of account holder."""
    INDIVIDUAL = 'individual'
    CORPORATE = 'corporate'
    GOVERNMENT = 'government'


# Account holder shared by card, wallet and instrument methods
class PaymentSetupAccountHolder:
    """Account holder details for the payment."""
    # The card account holder type.
    # [Optional]
    type: PaymentSetupAccountHolderType
    # The card account holder's first name.
    # [Optional]
    first_name: str
    # The card account holder's last name.
    # [Optional]
    last_name: str
    # The card account holder's middle name.
    # [Optional]
    middle_name: str
    # The card account holder's company name.
    # [Optional]
    company_name: str
    # Indicates whether the ANI (account name inquiry) check is performed with the card scheme
    # (Visa or Mastercard).
    # [Optional]
    account_name_inquiry: bool


# Instrument entities
class PaymentSetupInstrument(PaymentSetupPaymentMethod):
    """The instrument payment method's details and configuration."""
    # The unique identifier of the selected instrument.
    # [Optional]
    id: str
    # The customer's phone number. Not present in the current instrument schema.
    # [Optional]
    phone: Phone
    # Account holder details for the payment. Not present in the current instrument schema.
    # [Optional]
    account_holder: PaymentSetupAccountHolder
    # Indicates whether to use the Real-Time Account Updater to update the card information.
    # Not present in the current instrument schema.
    # [Optional]
    allow_update: bool
    # The next available action for the payment method.
    # [Optional]
    # readOnly
    action: PaymentMethodAction


# Status/flags-only methods
class PayNow(PaymentSetupPaymentMethod):
    """The PayNow payment method's details and configuration. Read-only."""
    pass


class Eps(PaymentSetupPaymentMethod):
    """The EPS payment method's details and configuration. Read-only."""
    pass


class Benefit(PaymentSetupPaymentMethod):
    """The Benefit payment method's details and configuration. Read-only."""
    pass


class Vipps(PaymentSetupPaymentMethod):
    """The Vipps payment method's details and configuration. Read-only."""
    pass


class Twint(PaymentSetupPaymentMethod):
    """The Twint payment method's details and configuration. Read-only."""
    pass


class MobilePay(PaymentSetupPaymentMethod):
    """The MobilePay payment method's details and configuration. Read-only."""
    pass


class Tamara(PaymentSetupPaymentMethod):
    """The Tamara payment method's details and configuration."""
    pass


class MBWay(PaymentSetupPaymentMethod):
    """The MBWay payment method's details and configuration. Read-only."""
    pass


class WeChatPay(PaymentSetupPaymentMethod):
    """The WeChatPay payment method's details and configuration. Read-only."""
    pass


class Octopus(PaymentSetupPaymentMethod):
    """The Octopus payment method's details and configuration. Read-only."""
    pass


class Alma(PaymentSetupPaymentMethod):
    """The Alma payment method's details and configuration."""
    pass


class Sequra(PaymentSetupPaymentMethod):
    """The Sequra payment method's details and configuration."""
    pass


# Wallets that share terminal_type/os_type configuration
class TerminalPaymentMethod(PaymentSetupPaymentMethod):
    """Base for the wallet payment methods that take a terminal type and an OS type."""
    # The client-side terminal type. Indicates whether the customer is using a PC browser,
    # mobile browser, or mobile application.
    # [Optional]
    terminal_type: TerminalType
    # The customer's operating system type. Required when terminal_type is not web.
    # [Optional]
    os_type: OsType


class AlipayCn(TerminalPaymentMethod):
    """The Alipay CN payment method's details and configuration."""
    pass


class AlipayHK(TerminalPaymentMethod):
    """The Alipay HK payment method's details and configuration."""
    pass


class GCash(TerminalPaymentMethod):
    """The GCash payment method's details and configuration."""
    pass


class Tng(TerminalPaymentMethod):
    """The TNG payment method's details and configuration."""
    pass


class Dana(TerminalPaymentMethod):
    """The Dana payment method's details and configuration."""
    pass


class KakaoPay(TerminalPaymentMethod):
    """The KakaoPay payment method's details and configuration."""
    pass


class TrueMoney(TerminalPaymentMethod):
    """The TrueMoney payment method's details and configuration."""
    pass


# Methods with specific fields
class Qpay(PaymentSetupPaymentMethod):
    """The QPay payment method's details and configuration."""
    # The Qatari national ID. Must start with 2 or 3, followed by 10 digits.
    # [Optional]
    national_id: str
    # A description of the payment order. Alphanumeric characters only.
    # [Optional]
    # max 255 characters
    description: str


class Ideal(PaymentSetupPaymentMethod):
    """The iDEAL payment method's details and configuration."""
    # A description of the products or services being paid for. Do not include HTML tags or
    # special characters, as these are rejected by iDEAL.
    # [Optional]
    # max 35 characters
    description: str


class Knet(PaymentSetupPaymentMethod):
    """The KNET payment method's details and configuration."""
    # The customer's preferred language, as an ISO 639-1 code. For example, the language
    # selected on your site, if the issuer's site supports it.
    # [Optional]
    language: KnetLanguage


class Bancontact(PaymentSetupPaymentMethod):
    """The Bancontact payment method's details and configuration."""
    # The account holder's name.
    # [Optional]
    # min 3 characters, max 100 characters
    account_holder_name: str


class Multibanco(PaymentSetupPaymentMethod):
    """The Multibanco payment method's details and configuration."""
    # The account holder's name.
    # [Optional]
    # min 3 characters, max 100 characters
    account_holder_name: str


class P24AccountHolder:
    """The P24 account holder's details."""
    # The account holder's name.
    # [Optional]
    # min 3 characters, max 100 characters
    name: str
    # The account holder's email address.
    # [Optional]
    # Format: email
    # max 254 characters
    email: str


class P24(PaymentSetupPaymentMethod):
    """The P24 (Przelewy24) payment method's details and configuration."""
    # The account holder's details.
    # [Optional]
    account_holder: P24AccountHolder


class SwishAccountHolder:
    """The Swish account holder's details."""
    # The account holder's first name.
    # [Optional]
    # min 1 characters
    first_name: str
    # The account holder's last name.
    # [Optional]
    # min 1 characters
    last_name: str


class Swish(PaymentSetupPaymentMethod):
    """The Swish payment method's details and configuration."""
    # A description that appears on the customer's billing statement.
    # [Optional]
    billing_descriptor: str
    # The account holder's details.
    # [Optional]
    account_holder: SwishAccountHolder


# ACH entities
class AchAccountType(str, Enum):
    """The type of Direct Debit account."""
    SAVINGS = 'savings'
    CURRENT = 'current'
    CASH = 'cash'


class AchAccountHolderIdentification:
    """The account holder's government document identification, for example a Social Security
    Number (SSN)."""
    # The document type.
    # [Optional]
    type: str
    # The country where the document was issued.
    # [Optional]
    issuing_country: str
    # The document number.
    # [Optional]
    number: str


class AchAccountHolder:
    """The ACH account holder details."""
    # The type of account holder.
    # [Optional]
    type: PaymentSetupAccountHolderType
    # The first name of the account holder.
    # [Optional]
    first_name: str
    # The last name of the account holder.
    # [Optional]
    last_name: str
    # The legal name of a registered company that holds the account.
    # [Optional]
    company_name: str
    # The account holder's date of birth.
    # [Optional]
    date_of_birth: str
    # The account holder's government document identification, for example a Social Security
    # Number (SSN).
    # [Optional]
    identification: AchAccountHolderIdentification


class Ach(PaymentSetupPaymentMethod):
    """The ACH payment method's details and configuration."""
    # The type of Direct Debit account.
    # [Optional]
    account_type: AchAccountType
    # The account holder details.
    # [Optional]
    account_holder: AchAccountHolder
    # The account number of the Direct Debit account.
    # [Optional]
    # min 4 characters, max 17 characters
    account_number: str
    # The bank code of the Direct Debit account.
    # [Optional]
    # min 8 characters, max 9 characters
    bank_code: str
    # The two-letter ISO country code of the bank account.
    # [Optional]
    # min 2 characters, max 2 characters
    country: str


# SEPA entities
class SetupsSepaMandateType(str, Enum):
    """The type of SEPA mandate on a Payment Setup.

    The Sepa.mandate.type schema declares these values lowercase. The payment-source and
    instrument positions declare them capitalized - see common.enums.SepaMandateType.
    Named apart so the two casings cannot be mixed up.
    """
    CORE = 'core'
    B2B = 'b2b'


class SepaMandate:
    """The SEPA mandate details."""
    # The ID of the mandate.
    # [Optional]
    id: str
    # The type of mandate.
    # [Optional]
    type: SetupsSepaMandateType
    # The date the mandate was signed.
    # [Optional]
    # Format: date (yyyy-MM-dd)
    date_of_signature: str


class SepaAccountHolder:
    """The SEPA account holder details."""
    # The type of account holder. The SEPA schema allows individual and corporate only.
    # [Optional]
    type: PaymentSetupAccountHolderType
    # The first name of the account holder.
    # [Optional]
    first_name: str
    # The last name of the account holder.
    # [Optional]
    last_name: str
    # The legal name of a registered company that holds the account.
    # [Optional]
    company_name: str


class Sepa(PaymentSetupPaymentMethod):
    """The SEPA payment method's details and configuration."""
    # The account holder details.
    # [Optional]
    account_holder: SepaAccountHolder
    # The account holder's IBAN.
    # [Optional]
    account_number: str
    # The account's country, as an ISO 3166-1 alpha-2 code.
    # [Optional]
    # min 2 characters, max 2 characters
    country: str
    # The account holder's account currency.
    # [Optional]
    currency: Currency
    # The mandate details.
    # [Optional]
    mandate: SepaMandate


# Google Pay entities
class GooglePayTokenData:
    """The Google Pay token data."""
    # The encryption and signing scheme used to create this message. If not set, the default
    # is ECv0.
    # [Optional]
    protocol_version: str
    # The signature that verifies the message came from Google, created using ECDSA.
    # [Optional]
    signature: str
    # A serialized JSON string containing the encryptedMessage, ephemeralPublicKey, and tag.
    # To simplify the signature verification process, this value is serialized.
    # [Optional]
    signed_message: str
    # The public key provided to the Google API in the
    # tokenizationSpecification.parameters.gatewayMerchantId field.
    # [Optional]
    tokenization_key: str


class GooglePay(PaymentSetupPaymentMethod):
    """The Google Pay payment method's details and configuration."""
    # The Google Pay token data.
    # [Optional]
    token_data: GooglePayTokenData
    # The Checkout.com Google Pay token. The spec declares token as an object with id and
    # expires_on; this SDK field carries the token identifier only.
    # [Optional]
    token: str
    # The date and time the token expires, in ISO 8601 format. The spec nests it under token.
    # [Optional]
    # Format: date-time (RFC 3339)
    expires_on: datetime
    # Set to true if you intend to reuse the payment credentials in subsequent payments. If set
    # to false, a payment instrument will not be included in the payment response.
    # [Optional]
    store_for_future_use: bool
    # The customer's phone number.
    # [Optional]
    phone: Phone
    # Account holder details for the payment.
    # [Optional]
    account_holder: PaymentSetupAccountHolder


# Apple Pay entities
class ApplePayTokenDataHeader:
    """Additional version-dependent information used to decrypt and verify the payment."""
    # The ephemeral public key.
    # [Optional]
    ephemeral_public_key: str
    # The hash of the public key.
    # [Optional]
    public_key_hash: str
    # The transaction identifier.
    # [Optional]
    transaction_id: str


class ApplePayTokenData:
    """The Apple Pay token data."""
    # The version of the payment token. The token uses EC_v1 for ECC-encrypted data, and
    # RSA_v1 for RSA-encrypted data.
    # [Optional]
    version: str
    # The encrypted payment data, Base64-encoded.
    # [Optional]
    data: str
    # The signature of the payment and header data. The signature includes the signing
    # certificate, its intermediate CA certificate, and information about the signing algorithm.
    # [Optional]
    signature: str
    # Additional version-dependent information used to decrypt and verify the payment.
    # [Optional]
    header: ApplePayTokenDataHeader


class ApplePay(PaymentSetupPaymentMethod):
    """The Apple Pay payment method's details and configuration."""
    # The Apple Pay token data.
    # [Optional]
    token_data: ApplePayTokenData
    # The Checkout.com Apple Pay token. The spec declares token as an object with id and
    # expires_on; this SDK field carries the token identifier only.
    # [Optional]
    token: str
    # The date and time the token expires, in ISO 8601 format. The spec nests it under token.
    # [Optional]
    # Format: date-time (RFC 3339)
    expires_on: datetime
    # Set to true if you intend to reuse the payment credentials in subsequent payments. If set
    # to false, a payment instrument will not be included in the payment response.
    # [Optional]
    store_for_future_use: bool
    # The customer's phone number.
    # [Optional]
    phone: Phone
    # Account holder details for the payment.
    # [Optional]
    account_holder: PaymentSetupAccountHolder


# Bacs entities
class BacsAccountHolderType(str, Enum):
    """The type of Bacs account holder."""
    INDIVIDUAL = 'individual'
    CORPORATE = 'corporate'


class BacsAccountHolder:
    """The Bacs account holder details."""
    # The type of account holder.
    # [Optional]
    type: BacsAccountHolderType
    # The first name of the account holder.
    # [Optional]
    first_name: str
    # The last name of the account holder.
    # [Optional]
    last_name: str
    # The legal name of a registered company that holds the account.
    # [Optional]
    company_name: str
    # The email address of the account holder.
    # [Optional]
    email: str


class Bacs(PaymentMethodBase):
    """The Bacs payment method's details and configuration."""
    # The ID of the Bacs instrument used for the payment.
    # [Optional]
    # readOnly
    instrument_id: str
    # The account holder details.
    # [Optional]
    account_holder: BacsAccountHolder
    # The account number of the Bacs Direct Debit account.
    # [Optional]
    account_number: str
    # The sort code of the Bacs Direct Debit account.
    # [Optional]
    bank_code: str
    # The account's country, as an ISO 3166-1 alpha-2 code.
    # [Optional]
    # min 2 characters, max 2 characters
    country: str
    # The account holder's account currency.
    # [Optional]
    currency: Currency
    # Indicates whether the Bacs instrument is created when account validation returns a
    # partial match. When true, the instrument is created on a partial match; when false,
    # instrument creation fails on a partial match. Defaults to false.
    # [Optional]
    allow_partial_match: bool


# Card Present entities
class CardPresentPin:
    """The PIN block details of a card-present payment. Not present in the current Payment Setup
    schema."""
    # The identifier of the key set used to encrypt the PIN block.
    # [Optional]
    key_set_id: str
    # The encrypted PIN block.
    # [Optional]
    block: str
    # The format of the PIN block.
    # [Optional]
    block_format: str


class CardPresent(PaymentSetupPaymentMethod):
    """The card-present payment method. Not present in the current Payment Setup schema."""
    # The track 2 data read from the card.
    # [Optional]
    track2: str
    # The EMV data read from the card.
    # [Optional]
    emv: str
    # The way the card details were entered.
    # [Optional]
    entry_mode: str
    # The PIN block details.
    # [Optional]
    pin: CardPresentPin
    # Set to true if you intend to reuse the payment credentials in subsequent payments.
    # [Optional]
    store_for_future_use: bool
    # The cardholder's name.
    # [Optional]
    name: str


# Pay by Bank entities
class PayByBankBank:
    """A bank available for the customer to select."""
    # The unique identifier of the bank.
    # [Optional]
    # readOnly
    bank_id: str
    # The display name of the bank.
    # [Optional]
    # readOnly
    display_name: str
    # The URL of the bank's logo.
    # [Optional]
    # readOnly
    logo_url: str
    # Whether the bank is currently available for selection.
    # [Optional]
    # readOnly
    available: bool


class PayByBankActionType(str, Enum):
    """The type of the Pay by Bank action."""
    SELECT_BANK = 'select_bank'


class PayByBankAction:
    """The next available action for the Pay by Bank payment method. Response only."""
    # The type of action.
    # [Optional]
    # readOnly
    type: PayByBankActionType
    # The list of banks available for the customer to select.
    # [Optional]
    # readOnly
    banks: list  # list of PayByBankBank


class PayByBank(PaymentSetupPaymentMethod):
    """The Pay by Bank (Open Banking) payment method's details and configuration."""
    # The identifier of the bank the customer has selected for the payment.
    # [Optional]
    bank_id: str
    # The next available action for the payment method.
    # [Optional]
    # readOnly
    action: PayByBankAction


# Cash App Pay entities
class CashAppActionType(str, Enum):
    """The type of the Cash App action."""
    REDIRECT = 'redirect'


class CashAppAction:
    """The next available action for the Cash App payment method. Response only."""
    # The type of action.
    # [Optional]
    # readOnly
    type: CashAppActionType
    # The URL to redirect the customer to so they can authorize the payment with Cash App.
    # [Optional]
    # readOnly
    # Format: uri
    redirect_url: str


class CashAppAddress:
    """The customer's address in their Cash App profile. Response only.

    These are Cash App's key names (address_line_1, administrative_district_level_1), not the
    Checkout.com Address keys (address_line1, city, state, zip), so the common Address type
    does not apply.
    """
    # The first line of the address.
    # [Optional]
    # readOnly
    address_line_1: str
    # The second line of the address.
    # [Optional]
    # readOnly
    address_line_2: str
    # The third line of the address.
    # [Optional]
    # readOnly
    address_line_3: str
    # The address locality, such as the city or town.
    # [Optional]
    # readOnly
    locality: str
    # The address sublocality, such as the district or neighborhood.
    # [Optional]
    # readOnly
    sublocality: str
    # The address's top-level administrative district, such as the state or province.
    # [Optional]
    # readOnly
    administrative_district_level_1: str
    # The postal or zip code.
    # [Optional]
    # readOnly
    postal_code: str
    # The address country, in ISO 3166-1 alpha-2 format.
    # [Optional]
    # readOnly
    # max 2 characters
    country: str


class CashAppCustomerProfile:
    """The customer's Cash App profile that they consented to share. Response only."""
    # Cash App's identifier for the customer. This is not a Checkout.com customer identifier.
    # [Optional]
    # readOnly
    customer_id: str
    # The customer's $Cashtag.
    # [Optional]
    # readOnly
    cashtag: str
    # Cash App's reference for the customer profile.
    # [Optional]
    # readOnly
    reference_id: str
    # The customer's full name.
    # [Optional]
    # readOnly
    full_name: str
    # The customer's given name.
    # [Optional]
    # readOnly
    given_name: str
    # The customer's middle name.
    # [Optional]
    # readOnly
    middle_name: str
    # The customer's family name.
    # [Optional]
    # readOnly
    family_name: str
    # The suffix of the customer's name.
    # [Optional]
    # readOnly
    suffix: str
    # The customer's date of birth. Kept as the raw string returned by the API, because the
    # provider's value is not always a plain yyyy-MM-dd date.
    # [Optional]
    # readOnly
    # Format: date
    birth_date: str
    # The customer's address.
    # [Optional]
    # readOnly
    address: CashAppAddress
    # The customer's phone number.
    # [Optional]
    # readOnly
    phone_number: str
    # The customer's email address.
    # [Optional]
    # readOnly
    email_address: str
    # The date and time the customer's Cash App account was created. Kept as the raw string
    # returned by the API, because the provider's format varies.
    # [Optional]
    # readOnly
    # Format: date-time
    customer_since: str


class CashApp(PaymentMethodBase):
    """The Cash App payment method's details and configuration.

    Serialized under the key cashapp, one lowercase word. Assigning None to an attribute sends
    null; leave an attribute unset to omit it from the request.
    """
    # Indicates whether the customer consents to share their Cash App customer profile with
    # Checkout.com.
    # [Optional]
    customer_profile_sharing: bool
    # The customer's Cash App profile that they consented to share. Included in the response
    # when customer_profile_sharing is enabled. Cash App releases this profile only once. It's
    # present in the first successful response when you get the Payment Setup after the
    # customer authorizes the payment. Every subsequent response omits it, so store it on
    # first read.
    # [Optional]
    # readOnly
    customer_profile: CashAppCustomerProfile
    # A reference for the Cash App Pay transaction, returned by the provider.
    # [Optional]
    # readOnly
    # max 80 characters
    reference: str
    # The next available action for the payment method. When its type is redirect, send the
    # customer to redirect_url to authorize the payment with Cash App.
    # [Optional]
    # readOnly
    action: CashAppAction


# Stablecoin entities
class Stablecoin(PaymentSetupPaymentMethod):
    """The Stablecoin payment method's details and configuration."""
    pass


# Card entities
class Card(PaymentSetupPaymentMethod):
    """The Card payment method's details and configuration.

    The spec nests the card fields under details (and the token under token.id); this class
    keeps them at the top level of the card object.
    """
    # The card number (without separators). The spec nests it under details.
    # [Optional]
    number: str
    # The last four digits of the card number. The spec nests it under details.
    # [Optional]
    # readOnly
    last4: str
    # The card issuer's Bank Identification Number (BIN). The spec nests it under details.
    # [Optional]
    # readOnly
    bin: str
    # The card scheme. The spec nests it under details.
    # [Optional]
    # readOnly
    scheme: str
    # The expiry month of the card. The spec nests it under details.
    # [Optional]
    expiry_month: int
    # The expiry year of the card. The spec nests it under details.
    # [Optional]
    expiry_year: int
    # The cardholder's name. The spec nests it under details.
    # [Optional]
    name: str
    # The card verification value/code. 3 digits, except for American Express (4 digits).
    # The spec nests it under details.
    # [Optional]
    cvv: str
    # Indicates whether this card is being submitted from your own stored card-on-file system,
    # rather than being entered by the customer at the time of payment. The spec nests it
    # under details.
    # [Optional]
    stored: bool
    # The time by which the card details must be confirmed. The spec nests it under details.
    # [Optional]
    # readOnly
    # Format: date-time (RFC 3339)
    expires_on: datetime
    # Set to true if you intend to reuse the payment credentials in subsequent payments. If set
    # to false, a payment instrument will not be included in the payment response.
    # [Optional]
    store_for_future_use: bool
    # The customer's phone number.
    # [Optional]
    phone: Phone
    # Account holder details for the payment.
    # [Optional]
    account_holder: PaymentSetupAccountHolder
    # Indicates whether to use the Real-Time Account Updater to update the card information.
    # The spec nests it under details.
    # [Optional]
    allow_update: bool


class PaymentMethods:
    """The payment methods that are enabled on your account and available for use."""
    # The instrument payment method's details and configuration.
    # [Optional]
    instrument: PaymentSetupInstrument
    # The Klarna payment method's details and configuration.
    # [Optional]
    klarna: Klarna
    # The stc pay payment method's details and configuration.
    # [Optional]
    stcpay: Stcpay
    # The Tabby payment method's details and configuration.
    # [Optional]
    tabby: Tabby
    # The Bizum payment method's details and configuration.
    # [Optional]
    # readOnly
    bizum: Bizum
    # The PayNow payment method's details and configuration.
    # [Optional]
    # readOnly
    paynow: PayNow
    # The QPay payment method's details and configuration.
    # [Optional]
    qpay: Qpay
    # The EPS payment method's details and configuration.
    # [Optional]
    # readOnly
    eps: Eps
    # The iDEAL payment method's details and configuration.
    # [Optional]
    ideal: Ideal
    # The KNET payment method's details and configuration.
    # [Optional]
    knet: Knet
    # The Bancontact payment method's details and configuration.
    # [Optional]
    bancontact: Bancontact
    # The Benefit payment method's details and configuration.
    # [Optional]
    # readOnly
    benefit: Benefit
    # The Blik payment method's details and configuration.
    # [Optional]
    blik: Blik
    # The Vipps payment method's details and configuration.
    # [Optional]
    # readOnly
    vipps: Vipps
    # The Twint payment method's details and configuration.
    # [Optional]
    # readOnly
    twint: Twint
    # The Alipay CN payment method's details and configuration.
    # [Optional]
    alipay_cn: AlipayCn
    # The Alipay HK payment method's details and configuration.
    # [Optional]
    alipay_hk: AlipayHK
    # The GCash payment method's details and configuration.
    # [Optional]
    gcash: GCash
    # The TNG payment method's details and configuration.
    # [Optional]
    tng: Tng
    # The Dana payment method's details and configuration.
    # [Optional]
    dana: Dana
    # The MobilePay payment method's details and configuration.
    # [Optional]
    # readOnly
    mobilepay: MobilePay
    # The Tamara payment method's details and configuration.
    # [Optional]
    tamara: Tamara
    # The MBWay payment method's details and configuration.
    # [Optional]
    # readOnly
    mbway: MBWay
    # The Multibanco payment method's details and configuration.
    # [Optional]
    multibanco: Multibanco
    # The WeChatPay payment method's details and configuration.
    # [Optional]
    # readOnly
    wechatpay: WeChatPay
    # The KakaoPay payment method's details and configuration.
    # [Optional]
    kakaopay: KakaoPay
    # The TrueMoney payment method's details and configuration.
    # [Optional]
    truemoney: TrueMoney
    # The Octopus payment method's details and configuration.
    # [Optional]
    # readOnly
    octopus: Octopus
    # The P24 (Przelewy24) payment method's details and configuration.
    # [Optional]
    p24: P24
    # The Alma payment method's details and configuration.
    # [Optional]
    alma: Alma
    # The Swish payment method's details and configuration.
    # [Optional]
    swish: Swish
    # The Sequra payment method's details and configuration.
    # [Optional]
    sequra: Sequra
    # The ACH payment method's details and configuration.
    # [Optional]
    ach: Ach
    # The SEPA payment method's details and configuration.
    # [Optional]
    sepa: Sepa
    # The PayPal payment method's details and configuration.
    # [Optional]
    paypal: Paypal
    # The Google Pay payment method's details and configuration.
    # [Optional]
    googlepay: GooglePay
    # The Apple Pay payment method's details and configuration.
    # [Optional]
    applepay: ApplePay
    # The Card payment method's details and configuration.
    # [Optional]
    card: Card
    # The Bacs payment method's details and configuration.
    # [Optional]
    bacs: Bacs
    # The card-present payment method. Not present in the current Payment Setup schema.
    # [Optional]
    card_present: CardPresent
    # The Pay by Bank (Open Banking) payment method's details and configuration. The spec
    # names this key paybybank.
    # [Optional]
    pay_by_bank: PayByBank
    # The Stablecoin payment method's details and configuration.
    # [Optional]
    stablecoin: Stablecoin
    # The Cash App payment method's details and configuration. Serialized as cashapp.
    # [Optional]
    cashapp: CashApp


# Settings entity
class Settings:
    """Settings for the Payment Setup."""
    # The URL to redirect the customer to, if the payment is successful. For payment methods
    # with a redirect, this value overrides the default success redirect URL configured on
    # your account.
    # [Optional]
    # Format: uri
    # max 255 characters
    success_url: str
    # The URL to redirect the customer to, if the payment is unsuccessful. For payment methods
    # with a redirect, this value overrides the default failure redirect URL configured on
    # your account.
    # [Optional]
    # Format: uri
    # max 255 characters
    failure_url: str
    # Indicates whether to capture the payment immediately. Defaults to true.
    # [Optional]
    capture: bool
    # The list of payment methods excluded from the Payment Setup.
    # [Optional]
    excluded_payment_methods: list  # list of str (PaymentSourceType values)


# Order entities
class OrderSubMerchant:
    """The details of a sub-merchant."""
    # The unique identifier for the sub-merchant.
    # [Optional]
    id: str
    # The product category for the sub-merchant.
    # [Optional]
    product_category: str
    # The number of orders the sub-merchant has processed.
    # [Optional]
    number_of_sales: int
    # The date the sub-merchant was registered.
    # [Optional]
    # Format: date (yyyy-MM-dd)
    registration_date: str


class AmountAllocationCommission:
    """Commission you'd like to collect from this split, credited to your currency account. The
    commission cannot exceed the split amount. The commission is the split amount multiplied by
    commission.percentage, plus commission.amount."""
    # Optional fixed amount of commission to collect, in the minor currency unit.
    # [Optional]
    # Format: int64
    # min 0
    amount: int
    # Optional percentage of commission to collect. Supports up to 8 decimal places.
    # [Optional]
    # min 0, max 100
    percentage: float


class PaymentSetupAmountAllocation:
    """A sub-entity that the payment is being processed on behalf of."""
    # The id of the sub-entity.
    # [Required]
    id: str
    # The split amount, credited to your sub-entity's currency account. The sum of all split
    # amounts must be equal to the payment amount. The amount must be provided in the minor
    # currency unit.
    # [Required]
    # Format: int64
    # min 0, max 9999999999
    amount: int
    # A reference you can later use to identify this split, such as an order number.
    # [Optional]
    # max 50 characters
    reference: str
    # Commission you'd like to collect from this split, credited to your currency account.
    # [Optional]
    commission: AmountAllocationCommission


class Order:
    """The customer's order details."""
    # A list of items in the order.
    # [Optional]
    items: list  # list of PaymentContextsItems
    # The customer's shipping details.
    # [Optional]
    shipping: ShippingDetails
    # The details of the sub-merchants.
    # [Optional]
    sub_merchants: list  # list of OrderSubMerchant
    # The discount amount the merchant applied to the transaction.
    # [Optional]
    # min 0
    discount_amount: int
    # The unique identifier for the invoice.
    # [Optional]
    invoice_id: str
    # The total shipping amount for the order.
    # [Optional]
    # min 0
    shipping_amount: int
    # The total tax amount for the order.
    # [Optional]
    # min 0
    tax_amount: int
    # The total tipping amount for the order.
    # [Optional]
    # Format: int64
    # min 0
    tipping_amount: int
    # The total surcharge amount for the order.
    # [Optional]
    # Format: int64
    # min 0
    surcharge_amount: int
    # The sub-entities that the payment is being processed on behalf of.
    # [Optional]
    amount_allocations: list  # list of PaymentSetupAmountAllocation


# Industry entities

class PaymentSetupAccommodationAddress:
    """The accommodation's address."""
    # The first line of the address.
    # [Optional]
    address_line1: str
    # The address city.
    # [Optional]
    city: str
    # The address state or county.
    # [Optional]
    state: str
    # The address country, in ISO 3166-1 alpha-2 format.
    # [Optional]
    country: str
    # The zip code or postal code.
    # [Optional]
    zip: str


class PaymentSetupAccommodationGuest:
    """A guest staying at the accommodation."""
    # The guest's first name.
    # [Optional]
    first_name: str
    # The guest's last name.
    # [Optional]
    last_name: str
    # The guest's date of birth.
    # [Optional]
    # Format: date (yyyy-MM-dd)
    date_of_birth: str


class PaymentSetupAccommodationRoom:
    """A room booked by the customer."""
    # The rate or cost of the room per day.
    # [Optional]
    rate: float
    # The number of nights the room is booked for.
    # [Optional]
    number_of_nights: int
    # The room class or type booked. For example, `deluxe`. Free-form string, not an enum.
    # [Optional]
    type: str


class PaymentSetupAccommodationHost:
    """Details about the host of the accommodation."""
    # The date the host registered.
    # [Optional]
    # Format: date (yyyy-MM-dd)
    registration_date: str
    # The total number of reservations the host has received.
    # [Optional]
    total_reservation_count: int


class PaymentSetupAccommodation:
    """Details about the accommodation booking. For lodging or cruise bookings."""
    # For lodging, contains the lodging name that appears on the storefront/customer receipts.
    # For cruise, contains the ship name booked for the cruise.
    # [Optional]
    name: str
    # A unique identifier for the booking.
    # [Optional]
    booking_reference: str
    # For lodging bookings, the customer's check-in date.
    # For cruise bookings, the cruise departure date (sail date).
    # [Optional]
    # Format: date (yyyy-MM-dd)
    check_in_date: str
    # For lodging bookings, the customer's check-out date.
    # For cruise bookings, the cruise return date.
    # [Optional]
    # Format: date (yyyy-MM-dd)
    check_out_date: str
    # The accommodation's address.
    # [Optional]
    address: PaymentSetupAccommodationAddress
    # The total number of rooms booked for the accommodation.
    # [Optional]
    number_of_rooms: int
    # The list of guests staying at the accommodation.
    # [Optional]
    guests: list  # list of PaymentSetupAccommodationGuest
    # The list of rooms booked by the customer.
    # [Optional]
    room: list  # list of PaymentSetupAccommodationRoom
    # The total number of guests on the booking.
    # [Optional]
    total_number_of_guests: int
    # Specifies whether the booking is refundable.
    # [Optional]
    refundable: bool
    # The recipient the booking confirmation is delivered to.
    # [Optional]
    delivery_recipient: str
    # Details about the host of the accommodation.
    # [Optional]
    host: PaymentSetupAccommodationHost


class PaymentSetupAirlineTicket:
    """Details about the airline ticket."""
    # The ticket's unique identifier.
    # [Optional]
    number: str
    # The date the airline ticket was issued.
    # [Optional]
    # Format: date (yyyy-MM-dd)
    issue_date: str
    # The carrier code of the ticket issuer.
    # [Optional]
    issuing_carrier_code: str
    # The travel package indicator, as one of the following codes: `A` (Airline flight
    # reservation), `B` (Car rental and airline reservation), `C` (Car rental reservation),
    # `N` (Unknown). Free-form string in the spec, not a typed enum.
    # [Optional]
    travel_package_indicator: str
    # The name of the travel agency.
    # [Optional]
    travel_agency_name: str
    # The IATA or ARC unique identifier for the travel agency that issues the ticket.
    # [Optional]
    travel_agency_code: str


class PaymentSetupAirlinePassengerAddress:
    """Details about the passenger's address."""
    # The two-letter ISO country code of the passenger's country of residence.
    # [Optional]
    country: str


class PaymentSetupAirlinePassenger:
    """A passenger on the flight."""
    # The passenger's first name.
    # [Optional]
    first_name: str
    # The passenger's last name.
    # [Optional]
    last_name: str
    # The passenger's date of birth.
    # [Optional]
    # Format: date (yyyy-MM-dd)
    date_of_birth: str
    # Details about the passenger's address.
    # [Optional]
    address: PaymentSetupAirlinePassengerAddress


class PaymentSetupFlightLegDetails:
    """A flight leg booked by the customer."""
    # The flight identifier.
    # [Optional]
    flight_number: str
    # The IATA 2-letter accounting code (PAX) that identifies the carrier. Required if the
    # airline data includes leg details.
    # [Optional]
    carrier_code: str
    # A one-letter identifier for the travel class. For example: `F` (First class),
    # `J` (Business class), `W` (Premium economy class), `Y` (Economy class).
    # [Optional]
    class_of_travelling: str
    # The IATA three-letter airport code for the departure airport. Required if the
    # airline data includes leg details.
    # [Optional]
    departure_airport: str
    # The date of the scheduled take-off.
    # [Optional]
    # Format: date (yyyy-MM-dd)
    departure_date: str
    # The time of the scheduled take-off.
    # [Optional]
    departure_time: str
    # The IATA three-letter airport code for the destination airport. Required if the
    # airline data includes leg details.
    # [Optional]
    arrival_airport: str
    # A one-letter code that indicates whether the passenger is entitled to make a stopover.
    # Specify `O` or a blank space if the passenger is entitled. Specify `X` if not entitled.
    # [Optional]
    stop_over_code: str
    # The alphanumeric fare basis code.
    # [Optional]
    fare_basis_code: str


class PaymentSetupAirlineInsurancePrice:
    """The price of the travel insurance."""
    # The insurance amount, in the minor currency unit.
    # [Optional]
    amount: float
    # The currency of the insurance amount, as a three-letter ISO currency code.
    # [Optional]
    currency: str


class PaymentSetupAirlineInsurance:
    """Details about the travel insurance purchased with the booking."""
    # The type of insurance.
    # [Optional]
    type: str
    # The name of the insurance company.
    # [Optional]
    company: str
    # The price of the insurance.
    # [Optional]
    price: PaymentSetupAirlineInsurancePrice


class PaymentSetupAirline:
    """Details about the airline ticket and flights the customer booked."""
    # Details about the airline ticket.
    # [Optional]
    ticket: PaymentSetupAirlineTicket
    # The list of passengers on the flight.
    # [Optional]
    passengers: list  # list of PaymentSetupAirlinePassenger
    # The list of flight legs booked by the customer.
    # [Optional]
    flight_leg_details: list  # list of PaymentSetupFlightLegDetails
    # The total number of passengers on the booking.
    # [Optional]
    total_number_of_passengers: int
    # The type of travel. For example, `domestic` or `international`. Free-form string,
    # not a typed enum.
    # [Optional]
    travel_type: str
    # The type of trip. For example, `one_way` or `round_trip`. Free-form string,
    # not a typed enum.
    # [Optional]
    trip_type: str
    # Specifies whether the booking is refundable.
    # [Optional]
    refundable: bool
    # The recipient the ticket is delivered to.
    # [Optional]
    delivery_recipient: str
    # Any additional add-ons purchased with the booking. For example, `extra_baggage`.
    # A single string per the spec, not an array, despite the plural name.
    # [Optional]
    ancillaries: str
    # Details about the travel insurance purchased with the booking.
    # [Optional]
    insurance: PaymentSetupAirlineInsurance


class Industry:
    """Industry-specific information."""
    # The list of airline bookings associated with the payment.
    # [Optional]
    airline: list  # list of PaymentSetupAirline
    # The list of accommodation bookings associated with the payment.
    # [Optional]
    accommodation: list  # list of PaymentSetupAccommodation


# Billing entity
class PaymentSetupBilling:
    """The billing details for the payment."""
    # A physical address. address_line1 and address_line2 are max 200 characters; city,
    # state and zip are max 50 characters; country is max 2 characters (ISO 3166-1 alpha-2).
    # [Optional]
    address: Address


class PaymentSetupBillingDescriptor:
    """The billing descriptor for the payment."""
    # A dynamic description of the payment.
    # [Optional]
    # max 25 characters
    name: str
    # The city from which the payment was made.
    # [Optional]
    # max 13 characters
    city: str
    # The reference shown on the statement.
    # [Optional]
    # max 50 characters
    reference: str


class PaymentSetupPresentmentDetails:
    """The amount and currency to present to the customer, when the settlement currency differs
    from the customer-facing currency."""
    # The presentment amount, in the minor currency unit.
    # [Optional]
    # Format: int64
    amount: int
    # The presentment currency, as a three-letter ISO currency code.
    # [Optional]
    currency: str


class PaymentSetupTerminal:
    """Terminal details."""
    # Terminal identifier.
    # [Optional]
    # min 8 characters, max 8 characters
    id: str
    # The local date and time on the terminal, in ISO 8601 format.
    # [Optional]
    # Format: date-time
    local_date_time: str


class AccountFundingTransactionIdentificationType(str, Enum):
    """The type of identification used to identify the sender."""
    PASSPORT = 'passport'
    DRIVING_LICENSE = 'driving_license'
    NATIONAL_ID = 'national_id'


class AccountFundingTransactionIdentification:
    """Sender identification details."""
    # The type of identification used to identify the sender.
    # [Optional]
    type: AccountFundingTransactionIdentificationType
    # The identification number.
    # [Optional]
    number: str
    # The two-letter ISO country code of the country that issued the identification.
    # [Optional]
    issuing_country: str


class AccountFundingTransactionSender:
    """Account funding transaction sender details."""
    # Date of birth of the sender (yyyy-mm-dd).
    # [Optional]
    # Format: date (yyyy-MM-dd)
    date_of_birth: str
    # The unique reference for the sender of the payment.
    # [Optional]
    reference: str
    # Sender identification details.
    # [Optional]
    identification: AccountFundingTransactionIdentification


class AccountFundingTransactionPurpose(str, Enum):
    """The purpose of the account funding transaction."""
    DONATIONS = 'donations'
    EDUCATION = 'education'
    EMERGENCY_NEED = 'emergency_need'
    EXPATRIATION = 'expatriation'
    FAMILY_SUPPORT = 'family_support'
    FINANCIAL_SERVICES = 'financial_services'
    GIFTS = 'gifts'
    INCOME = 'income'
    INSURANCE = 'insurance'
    INVESTMENT = 'investment'
    IT_SERVICES = 'it_services'
    LEISURE = 'leisure'
    LOAN_PAYMENT = 'loan_payment'
    MEDICAL_TREATMENT = 'medical_treatment'
    OTHER = 'other'
    PENSION = 'pension'
    ROYALTIES = 'royalties'
    SAVINGS = 'savings'
    TRAVEL_AND_TOURISM = 'travel_and_tourism'


class AccountFundingTransactionRecipient:
    """Account funding transaction recipient details."""
    # Date of birth of the recipient (yyyy-mm-dd).
    # [Optional]
    # Format: date (yyyy-MM-dd)
    date_of_birth: str
    # Any identifier like part of the PAN (first six digits and last four digits), an IBAN, an
    # internal account number, or a phone number related to the primary recipient's account.
    # [Optional]
    # max 34 characters
    account_number: str
    # The recipient's first name.
    # [Optional]
    # max 50 characters
    first_name: str
    # The recipient's last name.
    # [Optional]
    # max 50 characters
    last_name: str
    # A physical address. address_line1 and address_line2 are max 200 characters; city,
    # state and zip are max 50 characters; country is max 2 characters (ISO 3166-1 alpha-2).
    # [Optional]
    address: Address


class PaymentSetupAccountFundingTransaction:
    """Account funding transaction details for the payment."""
    # Whether to process this payment as an account funding transaction.
    # [Optional]
    enabled: bool
    # The purpose of the account funding transaction.
    # [Optional]
    purpose: AccountFundingTransactionPurpose
    # Account funding transaction sender details.
    # [Optional]
    sender: AccountFundingTransactionSender
    # Account funding transaction recipient details.
    # [Optional]
    recipient: AccountFundingTransactionRecipient


# Main Request and Response classes
class PaymentSetupsRequest:
    """Request body for POST /payments/setups and PUT /payments/setups/{id} (swagger
    PaymentSetup). The responses of the create, update, get and confirm operations are returned
    as a ResponseWrapper with the same keys."""
    # The processing channel to use for the payment.
    # [Required]
    # ^(pc)_(\w{26})$
    processing_channel_id: str
    # The payment amount, in the minor currency unit.
    # [Required]
    amount: int
    # The currency of the payment, as a three-letter ISO currency code.
    # [Required]
    currency: Currency
    # The type of payment. You must provide this field for card payments in which the
    # cardholder is not present. For example, if the transaction is a recurring payment, or a
    # mail order/telephone order (MOTO) payment. Defaults to regular.
    # [Optional]
    payment_type: PaymentType
    # A reference you can use to identify the payment. For example, an order number.
    # [Optional]
    # max 80 characters
    reference: str
    # A description of the payment.
    # [Optional]
    # max 100 characters
    description: str
    # The payment methods that are enabled on your account and available for use.
    # [Optional]
    payment_methods: PaymentMethods
    # Settings for the Payment Setup.
    # [Optional]
    settings: Settings
    # The customer's details.
    # [Optional]
    customer: Customer
    # The customer's order details.
    # [Optional]
    order: Order
    # Industry-specific information.
    # [Optional]
    industry: Industry
    # The billing details for the payment.
    # [Optional]
    billing: PaymentSetupBilling
    # The billing descriptor for the payment.
    # [Optional]
    billing_descriptor: PaymentSetupBillingDescriptor
    # The amount and currency to present to the customer, when the settlement currency differs
    # from the customer-facing currency.
    # [Optional]
    presentment_details: PaymentSetupPresentmentDetails
    # Terminal details.
    # [Optional]
    terminal: PaymentSetupTerminal
    # Account funding transaction details for the payment.
    # [Optional]
    account_funding_transaction: PaymentSetupAccountFundingTransaction
