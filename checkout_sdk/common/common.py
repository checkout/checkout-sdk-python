from datetime import datetime
from enum import Enum

from checkout_sdk.common.enums import AccountHolderIdentificationType, AccountHolderType, Country


class Address:
    address_line1: str
    address_line2: str
    city: str
    state: str
    zip: str
    country: Country


class Phone:
    country_code: str
    number: str


class CustomerRequest:
    id: str
    email: str
    name: str
    phone: Phone


class ResidentialStatusType(str, Enum):
    RESIDENT = 'resident'
    NON_RESIDENT = 'non_resident'


class AccountHolderIdentification:
    type: AccountHolderIdentificationType
    number: str
    issuing_country: Country
    date_of_expiry: str


class AccountHolder:
    type: AccountHolderType
    first_name: str
    last_name: str
    company_name: str
    tax_id: str
    date_of_birth: str
    country_of_birth: Country
    residential_status: ResidentialStatusType
    billing_address: Address
    phone: Phone
    identification: AccountHolderIdentification
    email: str
    gender: str
    middle_name: str


class BankDetails:
    name: str
    branch: str
    address: Address


class UpdateCustomerRequest:
    id: str
    default: bool


class MarketplaceCommission:
    amount: int
    percentage: float


class MarketplaceDataSubEntity:
    id: str
    amount: int
    reference: str
    commission: MarketplaceCommission


class MarketplaceData:
    sub_entity_id: str
    sub_entities: list  # MarketplaceDataSubEntity


class Product:
    name: str
    quantity: int
    price: int


class Commission:
    amount: int
    percentage: float


class AmountAllocations:
    id: str
    amount: int
    reference: str
    commission: Commission


class ShippingInfo:
    shipping_company: str
    shipping_method: str
    tracking_number: str
    tracking_uri: str
    return_shipping_company: str
    return_tracking_number: str
    return_tracking_uri: str


class QueryFilterDateRange:
    from_: datetime
    to: datetime
