try:
    from http import HTTPStatus
except ImportError:
    # Python 3.4
    from checkout_sdk.enums import HTTPStatus

import checkout_sdk as sdk
from checkout_sdk import ApiClient, HTTPMethod, Validator, PaymentStatus
from checkout_sdk.common import ResponseDTO
from checkout_sdk.vaults.responses import Token


class TokensClient(ApiClient):
    def request(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            # dictionary approach - everything else is ignored
            request = args[0]
        else:
            # parameter approach
            request = kwargs
 
        source_type = request.get('type')
        if(source_type == 'card'):
            number = request.get('number')
            last4 = number[-4:]
            expiry_month = request.get('expiry_month')
            expiry_year = request.get('expiry_year')
            # todo: insert validation here for cards
            self._log_debug('Token src:{} - {} {}/{}'.format(
                source_type,
                last4,
                expiry_month,
                expiry_year
            ))
        elif(source_type == 'applepay' or source_type == 'googlepay'):
            token_data = request.get('token_data')
            self._log_debug('Token src:{} - {}'.format(
                source_type,
                token_data
            ))
        

        http_response = self._send_http_request(
            'tokens', HTTPMethod.POST, request)

        return Token(http_response)