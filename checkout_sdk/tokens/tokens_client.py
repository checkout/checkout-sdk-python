import checkout_sdk as sdk

from checkout_sdk import ApiClient, Utils, HttpMethod
from checkout_sdk.tokens import PaymentTokenResponse


class TokensClient(ApiClient):
    def request_payment_token(self,
                              # Transaction
                              value=0, currency=sdk.default_currency,
                              track_id=None,
                              # Auto Capture
                              auto_capture=sdk.default_auto_capture,
                              auto_capture_delay=sdk.default_auto_capture_delay,
                              # Urls
                              success_url=None,
                              fail_url=None,
                              **kwargs):

        self._log_info(
            'Payment token {}{} - {}'.format(value, currency, track_id if track_id else '<no track id>'))

        Utils.validate_transaction(value=value, currency=currency)

        request = {
            'value': value,
            'currency': currency if not isinstance(currency, sdk.Currency) else currency.value,
            'trackId': track_id,
            'chargeMode': sdk.ChargeMode.APM.value,  # pylint: disable = no-member
            'autoCapture': 'Y' if auto_capture else 'N',
            'autoCapTime': auto_capture_delay,
            'successUrl': success_url,
            'failUrl': fail_url
        }

        # add remaining properties
        request.update(kwargs)

        http_response = self._send_http_request('tokens/payment',
                                                HttpMethod.POST, request)

        return PaymentTokenResponse(http_response)
