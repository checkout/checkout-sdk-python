import re

from checkout_sdk import errors, constants
from checkout_sdk.enums import Currency

ALPHANUM_REGEX = r'(\w{8})-(\w{4})-(\w{4})-(\w{4})-(\w{12})$'


def get_entity_regex(prefix): return re.compile(
    '^' + prefix + ALPHANUM_REGEX, re.IGNORECASE)


CUSTOMER_ID_REGEX = get_entity_regex('cust_')
CARD_ID_REGEX = get_entity_regex('card_')
TOKEN_REGEX = get_entity_regex('(card_)?tok_')


class Validator:
    @classmethod
    def validate_payment_request(cls, card=None, token=None, currency=None, email=None, customer_id=None):
        error_message = cls.get_error_message(
            card, token, currency, email, customer_id)
        if error_message:
            raise errors.BadRequestError(
                message=error_message, error_code=constants.VALIDATION_ERROR_CODE)

    @classmethod
    def get_error_message(cls, card=None, token=None, currency=None, email=None, customer_id=None):
        if not (card or token):
            return 'Payment source missing. Please specify a valid card or token.'

        if card and not (isinstance(card, dict) or CARD_ID_REGEX.match(card)):
            return 'Invalid card source. Please provide full card details or a valid Card Id.'

        if token and not (TOKEN_REGEX.match(token)):
            return 'Invalid token source.'

        if not Currency.has_value(currency if not isinstance(currency, Currency) else currency.value):
            return 'Invalid currency.'

        if not (email or customer_id):
            return 'Email or Customer Id is required when requesting a payment.'

        if customer_id and not CUSTOMER_ID_REGEX.match(customer_id):
            return 'Invalid Customer Id.'

        # no issues
        return None
