import checkout_sdk as sdk
from checkout_sdk import ApiClient, Validator

"""
TODO List

Get Payment

Capture
Refund
Void

Payment Response
        Id
        Processed On
        Approved
        Response Code
        Status
        Auth Code
        Currency
        Value
        TrackId
        Customer
            Id
            Email
            Name
        Source
            Card Id
            BillingAddress
            Phone
            ExpiryMonth
            ExpiryYear
            Name
            Scheme
            Last4
            Fingerprint
            Bin
            CardType
            CardCategory
            Issuer
            IssuerCountry
            ProductId
            ProductType
            AvsCheck
            CvvCheck
"""


class PaymentsClient(ApiClient):
    def request(self,
                card=None, token=None,
                value=0, currency=sdk.default_currency,
                payment_type=sdk.enums.PaymentType.Regular,
                customer=None, track_id=None,
                auto_capture=sdk.default_auto_capture,
                auto_capture_delay=sdk.default_auto_capture_delay,
                metadata={},
                **kwargs):

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
            'autoCapTime': auto_capture_delay,
            'metadata': metadata
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

        return self._build_api_response(*self._http_client.post('charges/card', request))
