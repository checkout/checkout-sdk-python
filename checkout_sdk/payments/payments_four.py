from __future__ import absolute_import

from datetime import datetime
from enum import Enum

import checkout_sdk
from checkout_sdk.common.common import CustomerRequest, Address, Phone
from checkout_sdk.common.common_four import AccountHolder, BankDetails, MarketplaceData
from checkout_sdk.common.enums import PaymentSourceType, Currency, Country
from checkout_sdk.common.enums_four import AccountType
from checkout_sdk.payments.payments import PaymentType, ShippingDetails, ThreeDsRequest, RiskRequest, \
    PaymentRecipient, ProcessingSettings, PaymentDestinationType


class AuthorizationType(str, Enum):
    FINAL = 'Final'
    ESTIMATED = 'Estimated'
    INCREMENTAL = 'Incremental'


class CaptureType(str, Enum):
    NON_FINAL = 'NonFinal'
    FINAL = 'Final'


class InstructionScheme(str, Enum):
    SWIFT = 'swift'
    LOCAL = 'local'
    INSTANT = 'instant'


class PaymentSenderType(str, Enum):
    INDIVIDUAL = 'individual'
    CORPORATE = 'corporate'
    INSTRUMENT = 'instrument'


class IdentificationType(str, Enum):
    PASSPORT = 'passport'
    DRIVING_LICENSE = 'driving_licence'
    NATIONAL_ID = 'national_id'


class PayoutSourceType(str, Enum):
    CURRENCY_ACCOUNT = 'currency_account'


class BillingDescriptor(checkout_sdk.payments.payments.BillingDescriptor):
    reference: str


class PaymentInstruction:
    purpose: str
    charge_bearer: str
    repair: bool
    scheme: InstructionScheme
    quote_id: str


class PayoutBillingDescriptor:
    reference: str


class Identification:
    type: IdentificationType
    number: str
    issuing_country: Country


# Payment Sender
class PaymentSender:
    type: PaymentSenderType

    def __init__(self, type_p: PaymentSenderType):
        self.type = type_p


class PaymentCorporateSender(PaymentSender):
    company_name: str
    address: Address

    def __init__(self):
        super().__init__(PaymentSenderType.CORPORATE)


class PaymentIndividualSender(PaymentSender):
    first_name: str
    last_name: str
    address: Address
    identification: Identification

    def __init__(self):
        super().__init__(PaymentSenderType.INDIVIDUAL)


class PaymentInstrumentSender(PaymentSender):

    def __init__(self):
        super().__init__(PaymentSenderType.INSTRUMENT)


# Payment Request Source
class PaymentRequestSource:
    type: PaymentSourceType

    def __init__(self, type_p: PaymentSourceType):
        self.type = type_p


class PaymentRequestCardSource(PaymentRequestSource):
    number: str
    expiry_month: int
    expiry_year: int
    name: str
    cvv: str
    stored: bool
    billing_address: Address
    phone: Phone

    def __init__(self):
        super().__init__(PaymentSourceType.CARD)


class PaymentRequestTokenSource(PaymentRequestSource):
    token: str
    billing_address: Address
    phone: Phone

    def __init__(self):
        super().__init__(PaymentSourceType.TOKEN)


class PaymentRequestNetworkTokenSource(PaymentRequestSource):
    token: str
    expiry_month: int
    expiry_year: int
    token_type: str
    cryptogram: str
    eci: str
    stored: bool
    name: str
    cvv: str
    billing_address: Address
    phone: Phone

    def __init__(self):
        super().__init__(PaymentSourceType.NETWORK_TOKEN)


class PaymentRequestIdSource(PaymentRequestSource):
    id: str
    cvv: str

    def __init__(self):
        super().__init__(PaymentSourceType.ID)


class RequestProviderTokenSource(PaymentRequestSource):
    payment_method: str
    token: str
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(PaymentSourceType.PROVIDER_TOKEN)


class RequestBankAccountSource(PaymentRequestSource):
    payment_method: str
    account_type: str
    country: Country
    account_number: str
    bank_code: str
    account_holder: AccountHolder

    def __init__(self):
        super().__init__(PaymentSourceType.BANK_ACCOUNT)


# Request Payment
class PaymentRequest:
    source: PaymentRequestSource
    amount: int
    currency: Currency
    payment_type: PaymentType
    merchant_initiated: bool
    reference: str
    description: str
    authorization_type: AuthorizationType
    capture: bool
    capture_on: datetime
    customer: CustomerRequest
    billing_descriptor: BillingDescriptor
    shipping: ShippingDetails
    three_ds: ThreeDsRequest
    processing_channel_id: str
    previous_payment_id: str
    risk: RiskRequest
    success_url: str
    failure_url: str
    payment_ip: str
    sender: PaymentSender
    recipient: PaymentRecipient
    marketplace: MarketplaceData
    processing: ProcessingSettings
    metadata: dict
    items: list  # four/Product


# Payout Request Source
class PayoutRequestSource:
    type: PayoutSourceType

    def __init__(self, type_p: PayoutSourceType):
        self.type = type_p


class PayoutRequestCurrencyAccountSource(PayoutRequestSource):
    id: str

    def __init__(self):
        super().__init__(PayoutSourceType.CURRENCY_ACCOUNT)


# Payment Request Destination
class PaymentRequestDestination:
    type: PaymentDestinationType

    def __init__(self, type_p: PaymentDestinationType):
        self.type = type_p


class PaymentBankAccountDestination(PaymentRequestDestination):
    account_type: AccountType
    account_number: str
    bank_code: str
    branch_code: str
    iban: str
    swift_bic: str
    country: Country
    account_holder: AccountHolder
    bank: BankDetails

    def __init__(self):
        super().__init__(PaymentDestinationType.BANK_ACCOUNT)


class PaymentRequestIdDestination(PaymentRequestDestination):
    id: str

    def __init__(self):
        super().__init__(PaymentDestinationType.ID)


# Request Payout
class PayoutRequest:
    source: PayoutRequestSource
    destination: PaymentRequestDestination
    amount: int
    currency: Currency
    reference: str
    billing_descriptor: PayoutBillingDescriptor
    sender: PaymentSender
    instruction: PaymentInstruction
    processing_channel_id: str


# Captures
class CaptureRequest:
    amount: int
    capture_type: CaptureType
    reference: str
    metadata: dict


# Authorization
class AuthorizationRequest:
    amount: int
    reference: str
    metadata: dict
