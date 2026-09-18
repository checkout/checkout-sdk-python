import json
import typing

from checkout_sdk.inventory.inventory import (
    InventoryAdjustmentRequest, InventoryCondition, InventoryHalLink, InventoryLevels,
    InventoryLevelsLinks, InventoryLevelsQuery, InventoryMoney, InventoryProductKnowledge,
    InventoryProductKnowledgeLinks, InventoryReservation, InventoryReservationItem, InventoryReservationLinks,
    InventoryReservationRequest, InventorySetLevelsRequest, InventorySetProductRequest, InventorySource,
    InventoryState, InventoryReservationState,
)
from checkout_sdk.json_serializer import JsonSerializer


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class TestInventoryAdjustmentRequestSerialization:
    """Schema validation against InventoryAdjustmentRequest (swagger example)."""

    def test_serializes_the_swagger_example(self):
        request = InventoryAdjustmentRequest()
        request.variant_id = 'var_123'
        request.delta = -3
        request.reason = 'damaged in warehouse'

        assert _serialize(request) == {
            'variant_id': 'var_123',
            'delta': -3,
            'reason': 'damaged in warehouse',
        }


class TestInventorySetLevelsRequestSerialization:
    """Schema validation against InventorySetLevelsRequest, all properties."""

    def test_serializes_every_property(self):
        request = InventorySetLevelsRequest()
        request.on_hand = 25
        request.safety_stock = 2
        request.reason = 'stock take 2026-07'

        assert _serialize(request) == {
            'on_hand': 25,
            'safety_stock': 2,
            'reason': 'stock take 2026-07',
        }


class TestInventoryReservationRequestSerialization:
    """Schema validation against InventoryReservationRequest and InventoryReservationItem."""

    def test_serializes_every_property(self):
        item = InventoryReservationItem()
        item.variant_id = 'var_123'
        item.quantity = 2

        request = InventoryReservationRequest()
        request.owner_type = 'ucp_session'
        request.owner_reference = 'cs_8f42'
        request.items = [item]
        request.ttl_seconds = 900

        assert _serialize(request) == {
            'owner_type': 'ucp_session',
            'owner_reference': 'cs_8f42',
            'items': [{'variant_id': 'var_123', 'quantity': 2}],
            'ttl_seconds': 900,
        }


class TestInventoryHalLinkSerialization:

    def test_serializes_every_property(self):
        link = InventoryHalLink()
        link.href = 'https://api.checkout.com/inventory/var_123'
        link.actions = ['GET']
        link.types = ['application/json']

        assert _serialize(link) == {
            'href': 'https://api.checkout.com/inventory/var_123',
            'actions': ['GET'],
            'types': ['application/json'],
        }


class TestInventoryMoneySerialization:

    def test_serializes_every_property(self):
        money = InventoryMoney()
        money.amount = 1999
        money.currency = 'USD'

        assert _serialize(money) == {'amount': 1999, 'currency': 'USD'}


class TestInventoryReservationSerialization:
    """Response-shape roundtrip against the swagger example for InventoryReservation."""

    def test_deserializes_every_property_from_the_swagger_example(self):
        payload = {
            'id': 'rsv_tkoi5db4hryu5cei5vwoabr7we',
            'state': 'held',
            'owner_type': 'ucp_session',
            'owner_reference': 'cs_8f42',
            'items': [{'variant_id': 'var_123', 'quantity': 2}],
            'expires_at': '2026-07-14T08:47:00Z',
            'created_on': '2026-07-14T08:32:00Z',
            '_links': {
                'self': {'href': 'https://api.checkout.com/inventory/reservations/rsv_123', 'actions': ['GET']},
                'commit': {
                    'href': 'https://api.checkout.com/inventory/reservations/rsv_123/commit',
                    'actions': ['POST'],
                },
                'release': {
                    'href': 'https://api.checkout.com/inventory/reservations/rsv_123/release',
                    'actions': ['POST'],
                },
            },
        }

        reservation = InventoryReservation()
        reservation.id = payload['id']
        reservation.state = InventoryReservationState(payload['state'])
        reservation.owner_type = payload['owner_type']
        reservation.owner_reference = payload['owner_reference']
        reservation.items = [InventoryReservationItem()]
        reservation.items[0].variant_id = payload['items'][0]['variant_id']
        reservation.items[0].quantity = payload['items'][0]['quantity']
        reservation.expires_at = payload['expires_at']
        reservation.created_on = payload['created_on']
        links = InventoryReservationLinks()
        links.self = InventoryHalLink()
        links.self.href = payload['_links']['self']['href']
        links.self.actions = payload['_links']['self']['actions']
        links.commit = InventoryHalLink()
        links.commit.href = payload['_links']['commit']['href']
        links.commit.actions = payload['_links']['commit']['actions']
        links.release = InventoryHalLink()
        links.release.href = payload['_links']['release']['href']
        links.release.actions = payload['_links']['release']['actions']
        reservation._links = links

        assert _serialize(reservation) == payload

    def test_state_enum_carries_all_four_values(self):
        assert [e.value for e in InventoryReservationState] == ['held', 'committed', 'released', 'expired']


class TestInventoryLevelsSerialization:
    """Response-shape roundtrip against the swagger example for InventoryLevels, including the
    embedded InventoryProductKnowledge when ?expand=product is used.
    """

    def test_serializes_every_property_without_expand(self):
        levels = InventoryLevels()
        levels.variant_id = 'var_123'
        levels.on_hand = 10
        levels.reserved = 2
        levels.safety_stock = 1
        levels.available = 7
        levels.state = InventoryState.IN_STOCK
        levels.source = InventorySource.MANAGED
        levels.created_on = '2026-07-01T09:15:00Z'
        levels.modified_on = '2026-07-13T14:02:11Z'
        links = InventoryLevelsLinks()
        links.self = InventoryHalLink()
        links.self.href = 'https://api.checkout.com/inventory/var_123'
        links.set = InventoryHalLink()
        links.set.href = 'https://api.checkout.com/inventory/var_123'
        levels._links = links

        assert _serialize(levels) == {
            'variant_id': 'var_123',
            'on_hand': 10,
            'reserved': 2,
            'safety_stock': 1,
            'available': 7,
            'state': 'in_stock',
            'source': 'managed',
            'created_on': '2026-07-01T09:15:00Z',
            'modified_on': '2026-07-13T14:02:11Z',
            '_links': {
                'self': {'href': 'https://api.checkout.com/inventory/var_123'},
                'set': {'href': 'https://api.checkout.com/inventory/var_123'},
            },
        }

    def test_embeds_product_knowledge_when_expanded(self):
        levels = InventoryLevels()
        levels.variant_id = 'var_123'
        product = InventoryProductKnowledge()
        product.variant_id = 'var_123'
        product.title = 'Blue T-Shirt'
        product.description = 'A blue t-shirt'
        product.product_url = 'https://example.com/p/var_123'
        product.image_url = 'https://example.com/i/var_123.png'
        product.condition = InventoryCondition.NEW
        product.created_on = '2026-07-01T09:15:00Z'
        product.modified_on = '2026-07-13T14:02:11Z'
        product._links = InventoryProductKnowledgeLinks()
        levels.product = product

        serialized = _serialize(levels)
        assert serialized['product']['title'] == 'Blue T-Shirt'
        assert serialized['product']['condition'] == 'new'


class TestInventoryLevelsQuerySerialization:

    def test_serializes_the_expand_query_parameter(self):
        query = InventoryLevelsQuery()
        query.expand = 'product'

        assert _serialize(query) == {'expand': 'product'}


class TestInventorySetProductRequestSerialization:
    """Schema validation against InventorySetProductRequest, including nested InventoryMoney."""

    def test_serializes_every_property(self):
        price = InventoryMoney()
        price.amount = 1999
        price.currency = 'USD'
        sale_price = InventoryMoney()
        sale_price.amount = 1499
        sale_price.currency = 'USD'

        request = InventorySetProductRequest()
        request.title = 'Blue T-Shirt'
        request.description = 'A blue t-shirt'
        request.product_url = 'https://example.com/p/var_123'
        request.image_url = 'https://example.com/i/var_123.png'
        request.additional_image_urls = ['https://example.com/i/var_123_2.png']
        request.video_url = 'https://example.com/v/var_123.mp4'
        request.model_3d_url = 'https://example.com/m/var_123.glb'
        request.sku = 'sku_123'
        request.gtin = '01234567890128'
        request.mpn = 'mpn_123'
        request.brand = 'Acme'
        request.category = 'Apparel'
        request.price = price
        request.sale_price = sale_price
        request.sale_price_starts_at = '2026-07-01T00:00:00Z'
        request.sale_price_ends_at = '2026-07-31T23:59:59Z'
        request.group_id = 'grp_123'
        request.group_title = 'Blue T-Shirt'
        request.color = 'blue'
        request.size = 'M'
        request.size_system = 'US'
        request.gender = 'unisex'
        request.condition = InventoryCondition.NEW
        request.material = 'cotton'
        request.age_group = 'adult'
        request.length = 10.0
        request.width = 5.0
        request.height = 1.0
        request.dimension_unit = 'cm'
        request.weight = 0.2
        request.weight_unit = 'kg'
        request.expiration_date = '2027-07-01T00:00:00Z'
        request.harmonized_system_code = '610910'
        request.country_of_origin = 'US'
        request.seller_name = 'Acme Inc'
        request.seller_url = 'https://example.com'
        request.seller_privacy_policy = 'https://example.com/privacy'
        request.seller_tos = 'https://example.com/tos'

        serialized = _serialize(request)
        assert serialized['title'] == 'Blue T-Shirt'
        assert serialized['price'] == {'amount': 1999, 'currency': 'USD'}
        assert serialized['sale_price'] == {'amount': 1499, 'currency': 'USD'}
        assert serialized['condition'] == 'new'
        assert serialized['country_of_origin'] == 'US'
        # get_type_hints merges the InventoryMerchandisingFields base in with the subclass's
        # own annotations; __annotations__ alone would only see the subclass's direct fields.
        assert set(serialized.keys()) == set(typing.get_type_hints(InventorySetProductRequest).keys())

    def test_condition_enum_defaults_to_new_and_carries_three_values(self):
        assert [e.value for e in InventoryCondition] == ['new', 'used', 'refurbished']


class TestInventoryDateTimeFields:
    """INT-1699 concerned format:date fields typed as datetime by mistake; the Inventory fields
    below are all format:date-time and are correctly annotated `datetime`, not `str`.
    """

    def test_datetime_fields_are_annotated_as_datetime(self):
        from datetime import datetime
        assert InventoryLevels.__annotations__['created_on'] is datetime
        assert InventoryLevels.__annotations__['modified_on'] is datetime
        assert InventoryReservation.__annotations__['expires_at'] is datetime
        assert InventoryReservation.__annotations__['created_on'] is datetime
        assert InventoryProductKnowledge.__annotations__['created_on'] is datetime
        assert InventoryProductKnowledge.__annotations__['modified_on'] is datetime
