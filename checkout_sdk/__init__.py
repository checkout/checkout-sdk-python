import logging
import os
import sys

name = "checkout_sdk"

from checkout_sdk.enums import Currency, HTTPMethod, PaymentType, PaymentStatus

# defaults
default_currency = None
default_capture = True
default_payment_type = PaymentType.Regular
default_response_immutable = True

# logging
logger = logging.getLogger('cko')
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

LOGGING_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO
}
env_logging_level = str(os.environ.get('CKO_LOGGING', None)).lower()
if env_logging_level in LOGGING_LEVELS.keys():
    logger.setLevel(LOGGING_LEVELS[env_logging_level])

# class imports (order matters!)

from checkout_sdk import constants
from checkout_sdk.config import Config
from checkout_sdk.validator import Validator

from checkout_sdk.http_client import HTTPClient
from checkout_sdk.api_client import ApiClient
from checkout_sdk.checkout_api import CheckoutApi


def get_api(secret_key=None, sandbox=None,
            timeout=constants.DEFAULT_TIMEOUT, api_base_url=None):
    return CheckoutApi(**locals())
