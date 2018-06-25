import re

from checkout_sdk import errors, constants
from checkout_sdk.enums import Currency, PaymentType

ALPHANUM_REGEX = r'(\w{8})-(\w{4})-(\w{4})-(\w{4})-(\w{12})$'


def get_guid_regex(prefix=None): return re.compile(
    '^' + (prefix if prefix else r'(\w{3,}_)?') + ALPHANUM_REGEX, re.IGNORECASE)


CUSTOMER_ID_REGEX = get_guid_regex('cust_')
CARD_ID_REGEX = get_guid_regex('card_')
TOKEN_REGEX = get_guid_regex('(card_)?tok_')
EMAIL_REGEX = re.compile(r'^.+@.+$', re.IGNORECASE)


class Validator:
    @classmethod
    def validate_payment_source(cls, card=None, token=None):
        if not (card or token):
            cls.throw(
                'Payment source missing. Please specify a valid card or token.')
        if card and not (isinstance(card, dict) or CARD_ID_REGEX.match(card)):
            cls.throw(
                'Invalid card source. Please provide full card details or a valid Card Id.')
        if token and not (TOKEN_REGEX.match(token)):
            cls.throw('Invalid token source.')

    @classmethod
    def validate_transaction(cls, value, currency, payment_type):
        try:
            value = int(value)
        except ValueError:
            value = None
        finally:
            if (value is None or value < 0):
                cls.throw('Transaction value must be equal or greater than zero')
        if not Currency.has_value(currency if not isinstance(currency, Currency) else currency.value):
            cls.throw('Invalid currency.')
        if not PaymentType.has_value(payment_type if not isinstance(payment_type, PaymentType) else payment_type.value):
            cls.throw('Invalid payment type.')

    @classmethod
    def validate_customer(cls, customer):
        if not (customer or CUSTOMER_ID_REGEX.match(customer) or EMAIL_REGEX.match(customer)):
            cls.throw(
                'Email or Customer Id is required when requesting a payment.')

    @classmethod
    def throw(cls, error_message=None):
        raise errors.BadRequestError(
            message=error_message, error_code=constants.VALIDATION_ERROR_CODE)

    @classmethod
    def is_id(cls, property):
        return get_guid_regex().match(property)
