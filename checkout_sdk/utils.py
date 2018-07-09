import re
import datetime
import checkout_sdk
import pprint

from checkout_sdk import errors, constants
from checkout_sdk.enums import Currency, PaymentType

SHORT_ID_REGEX = r'(\w{20})$'
LONG_ID_REGEX = r'(\w{8})-(\w{4})-(\w{4})-(\w{4})-(\w{12})$'


def get_guid_regex(prefix=None, short_id=False): return re.compile(
    '^' + (prefix+'_' if prefix else r'(\w{3,}_(test_)?)?') + (SHORT_ID_REGEX if short_id else LONG_ID_REGEX), re.IGNORECASE)


CUSTOMER_ID_REGEX = get_guid_regex('cust')
CARD_ID_REGEX = get_guid_regex('card')
TOKEN_REGEX = get_guid_regex('(card_)?tok')
EMAIL_REGEX = re.compile(r'^.+@.+$', re.IGNORECASE)


class Utils:
    @classmethod
    def validate_payment_id(cls, id):
        """Validates the payment id."""
        if not Utils.is_id(id, short_id=True):
            cls.throw('Invalid Payment/Charge Id')

    @classmethod
    def validate_payment_source(cls, card=None, token=None):
        """Validates card and token payment sources."""
        if not (card or token):
            cls.throw(
                'Payment source missing. Please specify a valid card or token.')
        if isinstance(card, dict) and \
            not (cls.validate_luhn(card.get('number')) and
                 # not smart on month for current year - API handles this
                 cls.is_number(card.get('expiryMonth'), 1, 12) and
                 cls.is_number(card.get('expiryYear'), datetime.datetime.now().year) and
                 cls.is_number(card.get('cvv', 0))):
            cls.throw('Invalid card data.')
        if type(card) is str and not CARD_ID_REGEX.match(card):
            cls.throw(
                'Invalid card source. Please provide a valid Card Id.')
        if token and not (TOKEN_REGEX.match(token)):
            cls.throw('Invalid token source.')

    @classmethod
    def validate_transaction(cls, value, currency=None, payment_type=None):
        if not cls.is_number(value, 0):
            cls.throw('Transaction value must be equal or greater than zero')
        if currency and not Currency.has_value(currency if not isinstance(currency, Currency) else currency.value):
            cls.throw('Invalid currency.')
        if payment_type and not PaymentType.has_value(payment_type if not isinstance(payment_type, PaymentType) else payment_type.value):
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
    def is_id(cls, property, prefix=None, short_id=False):
        return get_guid_regex(prefix, short_id).match(property) is not None

    @classmethod
    def is_number(cls, num, min=None, max=None):
        try:
            num = int(num)
        except ValueError:
            num = None
        finally:
            return num is not None and (min is None or num >= min) and (max is None or num <= max)

    @classmethod
    def validate_luhn(cls, pan):
        if pan is None:
            return False

        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(pan)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        return (checksum % 10) == 0

    @classmethod
    def mask_pan(cls, pan):
        left, right = (6, 4)
        return pan[0:left].ljust(len(pan)-right, '*')+pan[-right:]

    @classmethod
    def pretty_print_dict(dict):
        pprint.pprint(dict)
