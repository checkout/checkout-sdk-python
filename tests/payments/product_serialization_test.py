import json

import pytest

from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.payments.payments import Product, ProductSubType, ItemType


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


class TestProductSerialization:

    def test_sub_type_serializes_as_lowercase(self):
        p = Product()
        p.sub_type = ProductSubType.BLOCKCHAIN
        assert _serialize(p)['sub_type'] == 'blockchain'

    def test_all_sub_type_values_serialize_lowercase(self):
        expected = {
            ProductSubType.BLOCKCHAIN: 'blockchain',
            ProductSubType.CBDC: 'cbdc',
            ProductSubType.CRYPTOCURRENCY: 'cryptocurrency',
            ProductSubType.NFT: 'nft',
            ProductSubType.STABLECOIN: 'stablecoin',
        }
        for enum_val, expected_str in expected.items():
            p = Product()
            p.sub_type = enum_val
            assert _serialize(p)['sub_type'] == expected_str

    def test_all_type_values_serialize_lowercase(self):
        expected = {
            ItemType.DIGITAL: 'digital',
            ItemType.DISCOUNT: 'discount',
            ItemType.PHYSICAL: 'physical',
        }
        for enum_val, expected_str in expected.items():
            p = Product()
            p.type = enum_val
            assert _serialize(p)['type'] == expected_str

    def test_unset_type_and_sub_type_serialize_as_null(self):
        # With = None class-level defaults, unset fields serialize as null (not omitted)
        p = Product()
        p.name = 'Gold Necklace'
        p.quantity = 1
        result = _serialize(p)
        assert result['type'] is None
        assert result['sub_type'] is None

    def test_type_and_sub_type_accept_none(self):
        # Explicitly assigning None is valid and serializes as null
        p = Product()
        p.type = None
        p.sub_type = None
        p.name = 'Widget'
        result = _serialize(p)
        assert result.get('type') is None
        assert result.get('sub_type') is None

    def test_type_and_sub_type_round_trip(self):
        p = Product()
        p.type = ItemType.DIGITAL
        p.sub_type = ProductSubType.STABLECOIN
        p.name = 'USDC'
        p.quantity = 1
        p.unit_price = 10000
        p.reference = '858818ac'
        p.commodity_code = 'DEF123'
        p.unit_of_measure = 'units'
        p.total_amount = 10000
        p.tax_amount = 1000
        p.tax_rate = 2000
        p.discount_amount = 500
        p.wxpay_goods_id = '1001'
        p.image_url = 'https://example.com/image.jpg'
        p.url = 'https://example.com/product'
        p.sku = 'SKU-001'

        result = _serialize(p)

        assert result['type'] == 'digital'
        assert result['sub_type'] == 'stablecoin'
        assert result['name'] == 'USDC'
        assert result['quantity'] == 1
        assert result['unit_price'] == 10000
        assert result['reference'] == '858818ac'
        assert result['commodity_code'] == 'DEF123'
        assert result['unit_of_measure'] == 'units'
        assert result['total_amount'] == 10000
        assert result['tax_amount'] == 1000
        assert result['tax_rate'] == 2000
        assert result['discount_amount'] == 500
        assert result['wxpay_goods_id'] == '1001'
        assert result['image_url'] == 'https://example.com/image.jpg'
        assert result['url'] == 'https://example.com/product'
        assert result['sku'] == 'SKU-001'
