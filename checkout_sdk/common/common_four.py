from checkout_sdk.common.common import Address, Phone


class AccountHolder:
    first_name: str
    last_name: str
    billing_address: Address
    phone: Phone


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
