from enum import Enum

from checkout_sdk.common.common import Address, Phone
from checkout_sdk.common.enums import Country
from checkout_sdk.common.enums_four import AccountHolderIdentificationType, AccountHolderType


class ResidentialStatusType(str, Enum):
    RESIDENT = 'resident'
    NON_RESIDENT = 'non_resident'


class AccountHolderIdentification:
    type: AccountHolderIdentificationType
    number: str
    issuing_country: Country


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
    unit_price: int
    reference: str
    image_url: str
    url: str
    total_amount: int
    tax_amount: int
    discount_amount: int
    sku: str
    goods_id: str
    wxpay_goods_id: str
