name = "checkout_sdk"

# defaults

default_currency = None
default_auto_capture = True
default_auto_capture_delay = 0  # valid: 0 - 168 (hours)

# class imports (order matters!)

from checkout_sdk import constants
from checkout_sdk.config import Config
from checkout_sdk.validator import Validator
from checkout_sdk.enums import Currency

from checkout_sdk.http_client import HttpClient
from checkout_sdk.api_response import ApiResponse
from checkout_sdk.api_client import ApiClient
from checkout_sdk.checkout_api import CheckoutApi

# TODO: use logger
# debug/info
log = None


def get_api(secret_key=None, sandbox=None, timeout=constants.DEFAULT_TIMEOUT, api_base_url=None):
    return CheckoutApi(**locals())
