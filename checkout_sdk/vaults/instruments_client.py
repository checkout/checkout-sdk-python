try:
    from http import HTTPStatus
except ImportError:
    # Python 3.4
    from checkout_sdk.enums import HTTPStatus

import checkout_sdk as sdk
from checkout_sdk import ApiClient, HTTPMethod, Validator, PaymentStatus
from checkout_sdk.common import ResponseDTO


class InstrumentsClient(ApiClient):
    pass
