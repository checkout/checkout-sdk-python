import checkout_sdk as sdk
from checkout_sdk import ApiClient, Validator


class PaymentsClient(ApiClient):
    def request(self,
                card=None, token=None,
                value=0, currency=sdk.default_currency,
                email=None, customer_id=None,
                track_id=None, metadata={},
                auto_capture=sdk.default_auto_capture,
                auto_capture_delay=sdk.default_auto_capture_delay,
                **kwargs):

        Validator.validate_payment_request(
            card=card, token=token, currency=currency, email=email, customer_id=customer_id)

        request = {
            'value': value,
            'currency': currency if not isinstance(currency, sdk.Currency) else currency.value,
            'autoCapture': 'Y' if auto_capture else 'N',
            'autoCapTime': auto_capture_delay,
            'trackId': track_id if track_id else '',
            'metadata': metadata
        }

        if card:
            if isinstance(card, dict):
                request['card'] = card
            else:
                request['cardId'] = card
        else:
            request['cardToken'] = token

        if email:
            request['email'] = email
        else:
            request['customerId'] = customer_id

        return self.build_api_response(*self._http_client.post('charges/card', request))
