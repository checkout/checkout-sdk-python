import checkout_sdk as sdk
from checkout_sdk import ApiClient, Validator, HttpMethod
from checkout_sdk.payments import PaymentProcessed, VoidResponse

"""
TODO List

Capture
Refund
Void

Get Payment

Logging
"""


class PaymentsClient(ApiClient):
    def request(self,
                card=None, token=None,
                value=0, currency=sdk.default_currency,
                payment_type=sdk.PaymentType.Regular,
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

    def void(self, id, track_id=None, description=None, **kwargs):
        Validator.validate_payment_id(id)

        request = {
            'trackId': track_id,
            'description': description
        }

        # add remaining properties
        request.update(kwargs)

        return VoidResponse(self._send_http_request('charges/{}/void'.format(id), HttpMethod.POST, request))
