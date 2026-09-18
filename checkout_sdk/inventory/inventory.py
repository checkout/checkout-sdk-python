from __future__ import absolute_import

from datetime import datetime
from enum import Enum


class InventoryHalLink:
    """A single HAL-style link describing an action available on an inventory resource."""
    # Absolute URI of the linked resource or action.
    # [Optional]
    href: str
    # HTTP methods supported at `href`.
    # [Optional]
    actions: list  # values of str
    # Media types supported at `href`.
    # [Optional]
    types: list  # values of str


class InventoryLevelsLinks:
    """HAL links exposed alongside stock level responses."""
    # Link to retrieve the current stock levels for the variant.
    # [Optional]
    self: InventoryHalLink
    # Link to set the stock levels for the variant.
    # [Optional]
    set: InventoryHalLink


class InventoryState(str, Enum):
    IN_STOCK = 'in_stock'
    LIMITED = 'limited'
    OUT_OF_STOCK = 'out_of_stock'


class InventorySource(str, Enum):
    MANAGED = 'managed'
    SYNC = 'sync'


class InventoryCondition(str, Enum):
    NEW = 'new'
    USED = 'used'
    REFURBISHED = 'refurbished'


class InventoryReservationState(str, Enum):
    HELD = 'held'
    COMMITTED = 'committed'
    RELEASED = 'released'
    EXPIRED = 'expired'


class InventoryMoney:
    """An amount expressed in a currency's minor unit, used by inventory product knowledge."""
    # The amount, in the minor unit of `currency`.
    # [Required]
    amount: int
    # The 3-letter ISO 4217 currency code.
    # [Required]
    # exactly 3 characters
    currency: str


class InventoryAdjustmentRequest:
    """Request body for POST /inventory/adjustments."""
    # Identifier of the variant to adjust. The variant must already exist.
    # [Required]
    # max 128 characters
    variant_id: str
    # Signed change to apply to `on_hand`. A negative delta that would drive `on_hand` below zero
    # is rejected with 409. The value must be non-zero (enforced by the API, not a formal schema
    # constraint).
    # [Required]
    delta: int
    # Free-text reason recorded in the adjustment ledger. Must not contain personal data.
    # [Required]
    # min 1, max 256 characters
    reason: str


class InventoryReservationItem:
    """A single line item within an inventory reservation."""
    # Identifier of the variant to reserve. The variant must already exist.
    # [Required]
    # max 128 characters
    variant_id: str
    # Quantity of the variant to reserve.
    # [Required]
    # minimum 1
    quantity: int


class InventoryReservationRequest:
    """Request body for POST /inventory/reservations."""
    # Type of the entity that owns this reservation, echoed back on the response.
    # [Required]
    # max 64 characters
    owner_type: str
    # Reference identifying the specific owner, echoed back on the response.
    # [Required]
    # max 256 characters
    owner_reference: str
    # Variants and quantities to reserve. Variant ids must be unique within the request.
    # [Required]
    # min 1, max 45 items
    items: list  # values of InventoryReservationItem
    # Time to live for the hold, in seconds.
    # [Optional]
    # minimum 60, maximum 3600, default 900
    ttl_seconds: int


class InventoryReservationLinks:
    """HAL links exposed alongside an inventory reservation. A `held` reservation exposes all
    three; terminal states (`committed`, `released`, `expired`) expose `self` only.
    """
    # Link to retrieve the reservation.
    # [Optional]
    self: InventoryHalLink
    # Link to commit the reservation. Only present while `held`.
    # [Optional]
    commit: InventoryHalLink
    # Link to release the reservation. Only present while `held`.
    # [Optional]
    release: InventoryHalLink


class InventoryReservation:
    """Response body for createInventoryReservation, getInventoryReservation,
    commitInventoryReservation and releaseInventoryReservation.
    """
    # The reservation identifier, in the form `rsv_{base32-encoded GUID}`.
    # [Optional]
    id: str
    # Current state of the reservation. A `held` reservation past `expires_at` reports as `expired`.
    # [Optional]
    # enum: held, committed, released, expired
    state: InventoryReservationState
    # Echo of the request's `owner_type`.
    # [Optional]
    owner_type: str
    # Echo of the request's `owner_reference`.
    # [Optional]
    owner_reference: str
    # The reserved variants and quantities.
    # [Optional]
    items: list  # values of InventoryReservationItem
    # When the hold expires if not committed or released.
    # [Optional]
    expires_at: datetime
    # When the reservation was created.
    # [Optional]
    created_on: datetime
    # HAL links available for this reservation, dependent on its state.
    # [Optional]
    _links: InventoryReservationLinks


class InventorySetLevelsRequest:
    """Request body for PUT /inventory/{variant_id}."""
    # Physical stock on hand.
    # [Required]
    # minimum 0
    on_hand: int
    # Buffer withheld from sale. Defaults to 0 on create; left unchanged on update if omitted.
    # [Optional]
    # minimum 0
    safety_stock: int
    # Free-text reason recorded in the ledger. Must not contain personal data.
    # [Optional]
    # max 256 characters
    reason: str


class InventoryProductKnowledgeLinks:
    """HAL links exposed alongside inventory product knowledge."""
    # Link to retrieve the product knowledge.
    # [Required]
    self: InventoryHalLink
    # Link to set the product knowledge.
    # [Required]
    set: InventoryHalLink
    # Link to delete the product knowledge.
    # [Required]
    delete: InventoryHalLink


class InventoryProductKnowledge:
    """Response body for getInventoryProduct and setInventoryProduct. Also embeddable as
    `InventoryLevels.product` when `?expand=product` is passed.

    Beta: this schema and the endpoints that return it are marked Beta in the specification.
    """
    # Identifier of the variant this product knowledge describes.
    # [Required]
    variant_id: str
    # Product title.
    # [Required]
    title: str
    # Product description.
    # [Required]
    description: str
    # Canonical URL of the product page.
    # [Required]
    product_url: str
    # URL of the primary product image.
    # [Required]
    image_url: str
    # Additional image URLs.
    # [Optional]
    additional_image_urls: list  # values of str
    # URL of a product video.
    # [Optional]
    video_url: str
    # URL of a 3D model of the product.
    # [Optional]
    model_3d_url: str
    # Merchant SKU.
    # [Optional]
    sku: str
    # Global Trade Item Number.
    # [Optional]
    gtin: str
    # Manufacturer Part Number.
    # [Optional]
    mpn: str
    # Brand name.
    # [Optional]
    brand: str
    # Product category.
    # [Optional]
    category: str
    # Regular price. Present as an embedded object (InventoryMoney), not a bare $ref.
    # [Optional]
    price: InventoryMoney
    # Discounted price. When set, must share `price`'s currency and be <= `price`.
    # [Optional]
    sale_price: InventoryMoney
    # Start of the sale price window. Pairs with `sale_price`.
    # [Optional]
    sale_price_starts_at: datetime
    # End of the sale price window. Pairs with `sale_price`.
    # [Optional]
    sale_price_ends_at: datetime
    # Identifier grouping variants of the same product (e.g. by color/size). When set, `color`
    # and `size` are both expected (enforced by the API, not a formal schema constraint).
    # [Optional]
    group_id: str
    # Title shared across all variants in `group_id`.
    # [Optional]
    group_title: str
    # Color of this variant. Expected when `group_id` is set.
    # [Optional]
    color: str
    # Size of this variant. Expected when `group_id` is set.
    # [Optional]
    size: str
    # Sizing system used by `size` (e.g. `US`, `EU`).
    # [Optional]
    size_system: str
    # Target gender.
    # [Optional]
    gender: str
    # Condition of the item. Defaults to `new`.
    # [Required]
    # enum: new, used, refurbished
    condition: InventoryCondition
    # Material composition.
    # [Optional]
    material: str
    # Target age group.
    # [Optional]
    age_group: str
    # Length of the item.
    # [Optional]
    length: float
    # Width of the item.
    # [Optional]
    width: float
    # Height of the item.
    # [Optional]
    height: float
    # Unit used by `length`, `width` and `height`.
    # [Optional]
    dimension_unit: str
    # Weight of the item.
    # [Optional]
    weight: float
    # Unit used by `weight`.
    # [Optional]
    weight_unit: str
    # Expiration date of the item, if applicable.
    # [Optional]
    expiration_date: datetime
    # Harmonized System code, for customs.
    # [Optional]
    harmonized_system_code: str
    # 2-letter ISO 3166-1 alpha-2 country of origin.
    # [Optional]
    country_of_origin: str
    # Name of the seller.
    # [Optional]
    seller_name: str
    # URL of the seller.
    # [Optional]
    seller_url: str
    # URL of the seller's privacy policy.
    # [Optional]
    seller_privacy_policy: str
    # URL of the seller's terms of service.
    # [Optional]
    seller_tos: str
    # When the product knowledge was created.
    # [Required]
    created_on: datetime
    # When the product knowledge was last modified.
    # [Required]
    modified_on: datetime
    # HAL links available for this product knowledge.
    # [Required]
    _links: InventoryProductKnowledgeLinks


class InventorySetProductRequest:
    """Request body for PUT /inventory/{variant_id}/product.

    Beta: this schema and the endpoint it targets are marked Beta in the specification.
    """
    # Product title.
    # [Required]
    # max 512 characters
    title: str
    # Product description.
    # [Required]
    # max 4000 characters
    description: str
    # Canonical URL of the product page.
    # [Required]
    # max 2048 characters
    product_url: str
    # URL of the primary product image.
    # [Required]
    # max 2048 characters
    image_url: str
    # Additional image URLs.
    # [Optional]
    additional_image_urls: list  # values of str
    # URL of a product video.
    # [Optional]
    video_url: str
    # URL of a 3D model of the product.
    # [Optional]
    model_3d_url: str
    # Merchant SKU.
    # [Optional]
    # max 128 characters
    sku: str
    # Global Trade Item Number.
    # [Optional]
    gtin: str
    # Manufacturer Part Number.
    # [Optional]
    mpn: str
    # Brand name.
    # [Optional]
    brand: str
    # Product category.
    # [Optional]
    category: str
    # Regular price.
    # [Optional]
    price: InventoryMoney
    # Discounted price. Must share `price`'s currency and be <= `price`.
    # [Optional]
    sale_price: InventoryMoney
    # Start of the sale price window. Pairs with `sale_price`.
    # [Optional]
    sale_price_starts_at: datetime
    # End of the sale price window. Pairs with `sale_price`.
    # [Optional]
    sale_price_ends_at: datetime
    # Identifier grouping variants of the same product. When set, `color` and `size` are both
    # expected.
    # [Optional]
    group_id: str
    # Title shared across all variants in `group_id`.
    # [Optional]
    group_title: str
    # Color of this variant. Expected when `group_id` is set.
    # [Optional]
    color: str
    # Size of this variant. Expected when `group_id` is set.
    # [Optional]
    size: str
    # Sizing system used by `size`.
    # [Optional]
    size_system: str
    # Target gender.
    # [Optional]
    gender: str
    # Condition of the item. Exact lowercase match. Defaults to `new`.
    # [Optional]
    # enum: new, used, refurbished
    condition: InventoryCondition
    # Material composition.
    # [Optional]
    material: str
    # Target age group.
    # [Optional]
    age_group: str
    # Length of the item.
    # [Optional]
    length: float
    # Width of the item.
    # [Optional]
    width: float
    # Height of the item.
    # [Optional]
    height: float
    # Unit used by `length`, `width` and `height`.
    # [Optional]
    dimension_unit: str
    # Weight of the item.
    # [Optional]
    weight: float
    # Unit used by `weight`.
    # [Optional]
    weight_unit: str
    # Expiration date of the item, if applicable.
    # [Optional]
    expiration_date: datetime
    # Harmonized System code, for customs.
    # [Optional]
    harmonized_system_code: str
    # 2-letter ISO 3166-1 alpha-2 country of origin.
    # [Optional]
    country_of_origin: str
    # Name of the seller.
    # [Optional]
    seller_name: str
    # URL of the seller.
    # [Optional]
    seller_url: str
    # URL of the seller's privacy policy.
    # [Optional]
    seller_privacy_policy: str
    # URL of the seller's terms of service.
    # [Optional]
    seller_tos: str


class InventoryLevels:
    """Response body for getInventoryLevels, setInventoryLevels and adjustInventory."""
    # The variant identifier.
    # [Optional]
    variant_id: str
    # Physical stock on hand.
    # [Optional]
    on_hand: int
    # Sum of active holds against this variant.
    # [Optional]
    reserved: int
    # Buffer withheld from sale.
    # [Optional]
    safety_stock: int
    # max(0, on_hand - reserved - safety_stock).
    # [Optional]
    available: int
    # Stock state derived from `available`.
    # [Optional]
    # enum: in_stock, limited, out_of_stock
    state: InventoryState
    # Whether stock levels are merchant-managed or kept in sync from another system.
    # [Optional]
    # enum: managed, sync
    source: InventorySource
    # When the stock record was created.
    # [Optional]
    created_on: datetime
    # When the stock record was last modified.
    # [Optional]
    modified_on: datetime
    # Product knowledge for the variant. Only present when `?expand=product` was passed and
    # product knowledge exists for the variant.
    # [Optional]
    product: InventoryProductKnowledge
    # HAL links available for this stock record.
    # [Optional]
    _links: InventoryLevelsLinks


class InventoryLevelsQuery:
    """Query parameters for GET /inventory/{variant_id}."""
    # Set to `product` to embed the variant's product knowledge alongside the stock fields. Does
    # not change how `available` or the other stock fields are calculated. Omitted from the
    # response if product knowledge has not been set for the variant.
    # [Optional]
    # enum: product
    expand: str
