import logging
import os
import sys

name = "checkout_sdk"

# defaults

from checkout_sdk.enums import Currency, ChargeMode, HttpMethod, PaymentType

default_currency = None
default_auto_capture = True
default_auto_capture_delay = 0  # valid: 0 - 168 (hours)
default_payment_type = PaymentType.Regular

# logging
logger = logging.getLogger('cko')
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

logging_levels = {
    'debug': logging.DEBUG,
    'info': logging.INFO
}
env_logging_level = str(os.environ.get('CKO_LOGGING', None)).lower()
if env_logging_level in logging_levels.keys():
    logger.setLevel(logging_levels[env_logging_level])

# class imports (order matters!)

from checkout_sdk import constants
from checkout_sdk.config import Config
from checkout_sdk.utils import Utils

from checkout_sdk.http_response import HttpResponse
from checkout_sdk.http_client import HttpClient
from checkout_sdk.api_client import ApiClient
from checkout_sdk.checkout_api import CheckoutApi


def get_api(secret_key=None, sandbox=None, timeout=constants.DEFAULT_TIMEOUT, api_base_url=None):
    return CheckoutApi(**locals())
