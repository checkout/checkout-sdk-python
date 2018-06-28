import checkout_sdk as sdk
from checkout_sdk import ApiClient, Validator, HttpMethod
from checkout_sdk.payments import PaymentProcessed

"""
TODO List

Get Payment

Capture
Refund
Void
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

        # card can be a dictionary and need the JSON converted, if needed, before being validated
        if isinstance(card, dict):
            card = self._convert_json(card)

        Validator.validate_payment_source(card=card, token=token)
        Validator.validate_transaction(
            value=value, currency=currency, payment_type=payment_type)
        Validator.validate_customer(customer=customer)

        request = {
            'value': value,
            'currency': currency if not isinstance(currency, sdk.Currency) else currency.value,
            'trackId': track_id if track_id else '',
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

        return PaymentProcessed(self._send_http_request('charges/card', HttpMethod.POST, request))
