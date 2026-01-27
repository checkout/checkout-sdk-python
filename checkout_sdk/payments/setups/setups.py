from __future__ import absolute_import
from datetime import datetime
from enum import Enum

from checkout_sdk.common.common import Address, Phone
from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.contexts.contexts import PaymentContextsTicket
from checkout_sdk.payments.payments import PaymentType, ShippingDetails


# Enums
class PaymentMethodInitialization(str, Enum):
    DISABLED = 'disabled'
    ENABLED = 'enabled'


# Customer entities
class CustomerEmail:
    address: str
    verified: bool


class CustomerDevice:
    locale: str


class MerchantAccount:
    id: str
    registration_date: datetime
    last_modified: datetime
    returning_customer: bool
    first_transaction_date: datetime
    last_transaction_date: datetime
    total_order_count: int
    last_payment_amount: int


class Customer:
    email: CustomerEmail
    name: str
    phone: Phone
    device: CustomerDevice
    merchant_account: MerchantAccount


# Payment Method Common entities
class PaymentMethodAction:
    type: str
    client_token: str
    session_id: str


class PaymentMethodOption:
    id: str
    flags: list  # list of str
    action: PaymentMethodAction


class PaymentMethodOptions:
    sdk: PaymentMethodOption
    pay_in_full: PaymentMethodOption
    installments: PaymentMethodOption
    pay_now: PaymentMethodOption


class PaymentMethodBase:
    status: str
    flags: list  # list of str
    initialization: PaymentMethodInitialization = PaymentMethodInitialization.DISABLED


# Klarna entities
class KlarnaAccountHolder:
    billing_address: Address


class Klarna(PaymentMethodBase):
    def __init__(self):
        super().__init__()
        self.account_holder: KlarnaAccountHolder
        self.payment_method_options: PaymentMethodOptions


# Stcpay entities
class Stcpay(PaymentMethodBase):
    def __init__(self):
        super().__init__()
        self.otp: str
        self.payment_method_options: PaymentMethodOptions


# Tabby entities
class Tabby(PaymentMethodBase):
    def __init__(self):
        super().__init__()
        self.payment_method_options: PaymentMethodOptions


# Bizum entities
class Bizum(PaymentMethodBase):
    def __init__(self):
        super().__init__()
        self.payment_method_options: PaymentMethodOptions


class PaymentMethods:
    klarna: Klarna
    stcpay: Stcpay
    tabby: Tabby
    bizum: Bizum


# Settings entity
class Settings:
    success_url: str
    failure_url: str


# Order entities
class OrderSubMerchant:
    id: str
    product_category: str
    number_of_trades: int
    registration_date: datetime


class Order:
    items: list  # list of PaymentContextsItems
    shipping: ShippingDetails
    sub_merchants: list  # list of OrderSubMerchant
    discount_amount: int


# Industry entities
class AirlineData:
    ticket: PaymentContextsTicket
    passengers: list  # list of PaymentContextsPassenger
    flight_leg_details: list  # list of PaymentContextsFlightLegDetails


class Industry:
    airline_data: AirlineData
    accommodation_data: list  # list of AccommodationData


# Main Request and Response classes
class PaymentSetupsRequest:
    processing_channel_id: str
    amount: int
    currency: Currency
    payment_type: PaymentType
    reference: str
    description: str
    payment_methods: PaymentMethods
    settings: Settings
    customer: Customer
    order: Order
    industry: Industry
