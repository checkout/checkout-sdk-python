try:
    from http import HTTPStatus
except ImportError:
    # Python 3.4
    from checkout_sdk.enums import HTTPStatus

import checkout_sdk as sdk
from checkout_sdk import ApiClient, HTTPMethod, Validator, PaymentStatus
from checkout_sdk.common import ResponseDTO
from checkout_sdk.vaults.responses import Exchange


class ExchangeClient(ApiClient):
    def request(self, path='payments', *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            # dictionary approach - everything else is ignored
            request = args[0]
        else:
            # parameter approach
            request = kwargs
        # parameter approach

        headers = request.get('headers')
        request.pop('headers', None)

        http_response = self._send_http_request(
            'exchange/{}'.format(path), HTTPMethod.POST, request, headers)

        return Exchange(http_response)
