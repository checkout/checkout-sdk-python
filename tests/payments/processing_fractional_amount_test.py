import json

from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.payments.payments import ProcessingSettings


# The swagger types tax_amount, discount_amount, shipping_amount, shipping_tax_amount,
# duty_amount and original_order_amount as `number`, not `integer`, and the live API honours that:
# POST /payments with "tax_amount": 10.5 returns 201 and GET /payments/{id} echoes 10.5 back.
# Python has no runtime type enforcement, so the annotations saying `int` never broke anything,
# but they were the documented contract and told merchants a fractional amount was invalid.
# Java threw and Go failed the whole response on the same data; see those SDKs' tests.
def test_serializes_fractional_processing_amounts():
    settings = ProcessingSettings()
    settings.tax_amount = 10.5
    settings.discount_amount = 0.25
    settings.shipping_amount = 3.75
    settings.shipping_tax_amount = 1.5
    settings.duty_amount = 2.05
    settings.original_order_amount = 99.99

    body = json.loads(json.dumps(settings, cls=JsonSerializer))

    assert body['tax_amount'] == 10.5
    assert body['discount_amount'] == 0.25
    assert body['shipping_amount'] == 3.75
    assert body['shipping_tax_amount'] == 1.5
    assert body['duty_amount'] == 2.05
    assert body['original_order_amount'] == 99.99


def test_serializes_whole_processing_amounts_unchanged():
    settings = ProcessingSettings()
    settings.tax_amount = 3000

    body = json.loads(json.dumps(settings, cls=JsonSerializer))

    assert body['tax_amount'] == 3000


def test_annotations_declare_float_not_int():
    # Pins the annotation itself, because it is the merchant-visible contract and an `int` here
    # is what every other SDK in the family encoded as a hard type before this fix.
    import typing
    hints = typing.get_type_hints(ProcessingSettings)
    for field in ('tax_amount', 'discount_amount', 'shipping_amount',
                  'shipping_tax_amount', 'duty_amount', 'original_order_amount'):
        assert hints[field] is float, f'{field} should be annotated float, got {hints[field]}'
