from checkout_sdk import Currency, PaymentType


class Validator:
    @classmethod
    def validate_id(cls, val):
        if val is None:
            raise ValueError('Invalid Id.')
        if not isinstance(val, str):
            raise TypeError('Id should be of string type.')

    @classmethod
    def validate_transaction(cls, amount, currency=None,
                             payment_type=None, reference=None):
        if amount is None or (isinstance(amount, int) and amount < 0):
            raise ValueError('Amount must be greater or equal to zero.')
        if not isinstance(amount, int):
            raise TypeError('Amount must be an integer.')
        if currency is not None and isinstance(currency, str) \
                and not Currency.has_value(currency):
            raise ValueError('Invalid currency.')
        if currency is not None and not isinstance(currency, str):
            raise TypeError('Currency should be a string.')
        if payment_type is not None and isinstance(payment_type, str) \
                and not PaymentType.has_value(payment_type):
            raise ValueError('Invalid payment type.')
        if payment_type is not None and not isinstance(payment_type, str):
            raise TypeError('Payment type should be a string.')
        if reference is not None and not isinstance(reference, str):
            raise TypeError('Reference must be a string.')

    @classmethod
    def validate_complex_attribute(cls, arg,
                                   type_err_msg, missing_arg_err_msg=None):
        if arg is None and missing_arg_err_msg is not None:
            raise ValueError(missing_arg_err_msg)

        if not(arg is None or isinstance(arg, dict)):
            raise TypeError(
                '{} Please provide a dictionary.'
                .format(type_err_msg))

    @classmethod
    def validate_and_set_dynamic_attr(cls, arg, type_err_msg,
                                      missing_arg_err_msg=None):
        if arg is None and missing_arg_err_msg is not None:
            raise ValueError(missing_arg_err_msg)

        if arg is None or isinstance(arg, dict):
            return arg
        elif isinstance(arg, bool):
            return {'enabled': arg}
        else:
            raise TypeError(
                '{} Please provide a dictionary or a boolean value.'
                .format(type_err_msg))

    @classmethod
    def validate_and_set_source_type(cls, source):
        source_type_switch = {
            'card': lambda: 'number' in source,
            'customer':
                lambda: 'email' in source or ('id' in source and isinstance(
                    source['id'], str) and source['id'].startswith('cus_')),
            'token': lambda: 'token' in source,
            'id':
                lambda: 'id' in source and isinstance(
                    source['id'], str) and source['id'].startswith('src_')
        }
        source_type = source.get('type', None)
        if source_type is None:
            for key in source_type_switch:
                if source_type_switch[key]():
                    # we have a match - we now set the type accordingly
                    source['type'] = key
                    return source
        else:
            return source

        # if we got here, no match found
        raise ValueError(
            'Invalid source data. Cannot determine source `type`.')
