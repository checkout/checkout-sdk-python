import checkout_sdk as sdk
from checkout_sdk import ApiClient, Validator, HttpMethod
from checkout_sdk.payments import PaymentProcessed, CaptureResponse, VoidResponse, RefundResponse

"""
TODO List

Get Payment

Logging
"""


class PaymentsClient(ApiClient):
    def request(self,
                card=None, token=None,
                value=0, currency=sdk.default_currency,
                payment_type=sdk.default_payment_type,
                customer=None, track_id=None,
                auto_capture=sdk.default_auto_capture,
                auto_capture_delay=sdk.default_auto_capture_delay,
                **kwargs):

        # card can be a dictionary and need the JSON case converted, if needed, before being validated
        if isinstance(card, dict):
            card = self._convert_json_case(card)

        Validator.validate_payment_source(card=card, token=token)
        Validator.validate_transaction(
            value=value, currency=currency, payment_type=payment_type)
        Validator.validate_customer(customer=customer)

        request = {
            'value': value,
            'currency': currency if not isinstance(currency, sdk.Currency) else currency.value,
            'trackId': track_id,
            'transactionIndicator': payment_type if not isinstance(payment_type, sdk.PaymentType) else payment_type.value,
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

        if Validator.is_id(customer):
            request['customerId'] = customer
        else:
            request['email'] = customer

        # add remaining properties
        request.update(kwargs)

        return PaymentProcessed(
            self._send_http_request('charges/card' if card is not None else 'charges/token',
                                    HttpMethod.POST, request))

    def capture(self, id, value=None, track_id=None, **kwargs):
        return CaptureResponse(self._getPaymentActionResponse(id, 'capture', value, track_id, **kwargs))

    def void(self, id, track_id=None, **kwargs):
        return VoidResponse(self._getPaymentActionResponse(id, 'void', None, track_id, **kwargs))

    def refund(self, id, value=None, track_id=None, **kwargs):
        return RefundResponse(self._getPaymentActionResponse(id, 'refund', value, track_id, **kwargs))

    def get(self, id):
        Validator.validate_payment_id(id)

        return PaymentProcessed(self._send_http_request('charges/{}'.format(id), HttpMethod.GET))

    def _getPaymentActionResponse(self, id, action, value, track_id, **kwargs):
        Validator.validate_payment_id(id)

        request = {
            'trackId': track_id
        }

        if value is not None:
            Validator.validate_transaction(value=value)
            request['value'] = value

        # add remaining properties
        request.update(kwargs)

        return self._send_http_request('charges/{}/{}'.format(id, action), HttpMethod.POST, request)
