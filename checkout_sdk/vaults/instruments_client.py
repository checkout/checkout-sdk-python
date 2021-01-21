try:
    from http import HTTPStatus
except ImportError:
    # Python 3.4
    from checkout_sdk.enums import HTTPStatus

import checkout_sdk as sdk
from checkout_sdk import ApiClient, HTTPMethod, Validator, PaymentStatus
from checkout_sdk.common import ResponseDTO
from checkout_sdk.vaults.responses import (
    Instrument
)


class InstrumentsClient(ApiClient):
    def create(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            # dictionary approach - everything else is ignored
            request = args[0]
        else:
            # parameter approach
            request = kwargs

        token = request['token']

        self._log_info('Instrument Create Token:{}'.format(
            token
        ))

        http_response = self._send_http_request(
            'instruments', HTTPMethod.POST, request)

        return Instrument(http_response)

    def get(self, source_id):
        self._log_info('{} - {}'.format('get'.capitalize(), source_id))

        Validator.validate_id(source_id)

        http_response = self._send_http_request(
            'instruments/{}'.format(source_id), HTTPMethod.GET)

        return Instrument(http_response)

    def update(self, source_id, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            # dictionary approach - everything else is ignored
            request = args[0]
        else:
            # parameter approach
            request = kwargs

        Validator.validate_id(source_id)

        http_response = self._send_http_request(
            'instruments/{}'.format(source_id), HTTPMethod.PATCH, request)

        return Instrument(http_response)
