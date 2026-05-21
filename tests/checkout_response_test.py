from checkout_sdk.checkout_response import ResponseWrapper


def test_serialize_atomic_types():
    unwrapped_data = {
        'str_attr': 'attr-value',
        'int_attr': 1234,
        'float_attr': 56.78,
        'bool_attr': True,
        'none_attr': None,
    }

    wrapped_data = ResponseWrapper(data=unwrapped_data)

    assert wrapped_data.dict() == unwrapped_data


def test_serialize_object():
    class ObjAttr:
        str_attr_2 = 'attr-value-2'
        int_attr = 1234
        float_attr = 56.78
        bool_attr = True
        none_attr = None

        def callable_attr(self):
            pass

    wrapped_data = ResponseWrapper(
        data={
            'str_attr_1': 'attr-value-1',
            'obj_attr': ObjAttr(),
        }
    )

    assert isinstance(wrapped_data.obj_attr, ObjAttr)

    assert wrapped_data.dict() == {
        'str_attr_1': 'attr-value-1',
        'obj_attr': {
            'str_attr_2': 'attr-value-2',
            'int_attr': 1234,
            'float_attr': 56.78,
            'bool_attr': True,
            'none_attr': None,
        },
    }


def test_serialize_nested_objects():
    unwrapped_data = {
        'str_attr_1': 'attr-value-1',
        'int_attr_1': 123,
        'float_attr_1': 89.1,

        'obj_attr_1': {
            'str_attr_2': 'attr-value-2',
            'int_attr_2': 456,
            'float_attr_2': 91.2,

            'obj_attr_2': {
                'str_attr_3': 'attr-value-3',
                'int_attr_3': 789,
                'float_attr_3': 12.3,
            }
        }
    }

    wrapped_data = ResponseWrapper(data=unwrapped_data)

    assert isinstance(wrapped_data.obj_attr_1, ResponseWrapper)
    assert isinstance(wrapped_data.obj_attr_1.obj_attr_2, ResponseWrapper)

    assert wrapped_data.dict() == unwrapped_data


def test_serialize_mapping():
    unwrapped_data = {
        'str_attr_1': 'attr-value-1',
        'int_attr_1': 123,
        'float_attr_1': 45.6,

        'mapping_attr': {
            'str_attr_2': 'attr-value-2',
            'obj_attr': {
                'str_attr_3': 'attr-value-3'
            },
        },
    }

    wrapped_data = ResponseWrapper(data=unwrapped_data)

    assert isinstance(wrapped_data.mapping_attr.obj_attr, ResponseWrapper)

    mapping = unwrapped_data['mapping_attr'].copy()
    mapping['obj_attr'] = wrapped_data.mapping_attr.obj_attr
    mapping['callable_attr'] = lambda: None
    wrapped_data.mapping_attr = mapping

    assert wrapped_data.dict() == unwrapped_data


def test_serialize_iterable():
    unwrapped_data = {
        'str_attr_1': 'attr-value-1',
        'int_attr_1': 123,
        'float_attr_1': 45.6,

        'iterable_attr': [
            'list-item-1',
            {
                'str_attr_2': 'attr-value-2'
            },
        ],
    }

    wrapped_data = ResponseWrapper(data=unwrapped_data)

    assert isinstance(wrapped_data.iterable_attr, list)
    assert isinstance(wrapped_data.iterable_attr[1], ResponseWrapper)

    wrapped_data.iterable_attr.append(lambda: None)

    assert wrapped_data.dict() == unwrapped_data


def test_serialize_list_from_any_iterables():
    unwrapped_data = {
        'tuple_attr': (
            'tuple-item-1',
            'tuple-item-2',
            12.34,
        ),
        'set_attr': {
            'set-item-1',
            'set-item-2',
            56.78,
        },
    }

    wrapped_data = ResponseWrapper(data=unwrapped_data)

    assert isinstance(wrapped_data.tuple_attr, tuple)
    assert isinstance(wrapped_data.set_attr, set)

    serialized_data = wrapped_data.dict()

    assert isinstance(serialized_data['tuple_attr'], list)
    assert isinstance(serialized_data['set_attr'], list)

    assert tuple(serialized_data['tuple_attr']) == unwrapped_data['tuple_attr']
    assert set(serialized_data['set_attr']) == unwrapped_data['set_attr']


def test_serialize_circular_references():
    unwrapped_data = {
        'str_attr': 'attr-value',
        'iterable_attr_1': [
            0,
            1,
            2,
            {
                'obj_attr': {
                    'iterable_attr_2': [3, 4],
                },
            },
        ],
        'iterable_attr_3': [5, 6],
        'iterable_attr_4': [7, 8],
        'iterable_attr_5': [9, 0],
    }
    unwrapped_data['iterable_attr_1'][3]['obj_attr']['circular_ref'] = \
        unwrapped_data['iterable_attr_1']

    unwrapped_data['iterable_attr_1'][3]['obj_attr']['forward_ref'] = \
        unwrapped_data['iterable_attr_3']

    unwrapped_data['iterable_attr_1'][3]['obj_attr']['iterable_attr_2'][1] = \
        unwrapped_data['iterable_attr_1'][3]

    unwrapped_data['iterable_attr_4'][0] = unwrapped_data['iterable_attr_5']
    unwrapped_data['iterable_attr_5'][1] = unwrapped_data['iterable_attr_4']

    wrapped_data = ResponseWrapper(http_metadata=unwrapped_data)

    assert wrapped_data.dict() == {
        'http_metadata': {
            'str_attr': 'attr-value',
            'iterable_attr_1': [
                0,
                1,
                2,
                {
                    'obj_attr': {
                        'iterable_attr_2': [
                            3,
                            {'$ref': '#/http_metadata/iterable_attr_1/3'}
                        ],
                        'circular_ref': {'$ref': '#/http_metadata/iterable_attr_1'},
                        'forward_ref': [5, 6],
                    },
                },
            ],
            'iterable_attr_3': [5, 6],
            'iterable_attr_4': [
                [9, {'$ref': '#/http_metadata/iterable_attr_4'}],
                8,
            ],
            'iterable_attr_5': [
                9,
                [{'$ref': '#/http_metadata/iterable_attr_5'}, 8],
            ],
        },
    }
