import checkout_sdk as sdk

from checkout_sdk import ApiClient, Utils, HttpMethod
from checkout_sdk.payments import PaymentProcessed, ThreeDSResponse, CaptureResponse, VoidResponse, RefundResponse


class PaymentsClient(ApiClient):
    def request(self,
                # Source
                card=None, token=None,
                # Transaction
                value=0, currency=sdk.default_currency,
                payment_type=sdk.default_payment_type,
                customer=None, track_id=None,
                # Auto Capture
                auto_capture=sdk.default_auto_capture,
                auto_capture_delay=sdk.default_auto_capture_delay,
                # 3D
                charge_mode=sdk.ChargeMode.NonThreeD,
                attempt_n3d=False,
                **kwargs):

        payment_source = card or token

        # card can be a dictionary and need the JSON case converted, if needed, before being validated
        if isinstance(card, dict):
            card = self._convert_json_case(card)
            # change payment source to a masked PAN
            payment_source = Utils.mask_pan(card['number'])

        self._log_info(
            'Auth {} - {}{} - {}'.format(payment_source, value, currency, track_id if track_id else '<no track id>'))

        Utils.validate_payment_source(card=card, token=token)
        Utils.validate_transaction(
            value=value, currency=currency, payment_type=payment_type, charge_mode=charge_mode)
        Utils.validate_customer(customer=customer)

        request = {
            'value': value,
            'currency': currency if not isinstance(currency, sdk.Currency) else currency.value,
            'trackId': track_id,
            'transactionIndicator': payment_type if not isinstance(payment_type, sdk.PaymentType) else payment_type.value,
            'chargeMode': charge_mode if not isinstance(charge_mode, sdk.ChargeMode) else charge_mode.value,
            'attemptN3D': attempt_n3d,
            'autoCapture': 'Y' if auto_capture else 'N',
            'autoCapTime': auto_capture_delay
        }

        if card:
            if isinstance(card, dict):
                request['card'] = card
            else:
                request['cardId'] = card
        else:
            request['cardToken'] = token

        if Utils.is_email(customer):
            request['email'] = customer
        else:
            request['customerId'] = customer

        # add remaining properties
        request.update(kwargs)

        http_response = self._send_http_request('charges/card' if card is not None else 'charges/token',
                                                HttpMethod.POST, request)

        if Utils.verify_redirect_flow(http_response):
            return ThreeDSResponse(http_response)
        else:
            return PaymentProcessed(http_response)

    def capture(self, id, value=None, track_id=None, **kwargs):
        return CaptureResponse(self._getPaymentActionResponse(id, 'capture', value, track_id, **kwargs))

    def void(self, id, track_id=None, **kwargs):
        return VoidResponse(self._getPaymentActionResponse(id, 'void', None, track_id, **kwargs))

    def refund(self, id, value=None, track_id=None, **kwargs):
        return RefundResponse(self._getPaymentActionResponse(id, 'refund', value, track_id, **kwargs))

    def get(self, id):
        self._log_info('Get {}'.format(id))

        Utils.validate_id(id)

        return PaymentProcessed(self._send_http_request('charges/{}'.format(id), HttpMethod.GET))

    def _getPaymentActionResponse(self, id, action, value, track_id, **kwargs):
        self._log_info('{} - {} - {}'.format(action.capitalize(), id,
                                             track_id if track_id else '<no track id>'))

        Utils.validate_id(id)

        request = {
            'trackId': track_id
        }

        if value is not None:
            Utils.validate_transaction(value=value)
            request['value'] = value

        # add remaining properties
        request.update(kwargs)

        return self._send_http_request(
            'charges/{}/{}'.format(id, action), HttpMethod.POST, request)
