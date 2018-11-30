from http import HTTPStatus

import checkout_sdk as sdk
from checkout_sdk import ApiClient, HttpMethod, Validator
from checkout_sdk.common import RequestDTO
from checkout_sdk.payments import PaymentSource, Customer, ThreeDS
from checkout_sdk.payments.responses import (
    Payment,
    PaymentProcessed,
    PaymentPending,
    Capture,
    Void,
    Refund
)


class PaymentsClient(ApiClient):
    def request(self,
                # Source
                source,
                # Transaction
                amount=0, currency=sdk.default_currency,
                payment_type=sdk.default_payment_type,
                reference=None,
                # Customer
                customer=None,
                # Capture
                capture=sdk.default_capture,
                capture_on=None,
                # 3DS
                threeds=None,
                # Misc
                **kwargs
                ):

        source_type = source.type if isinstance(
            source, PaymentSource) else source.get('type', 'unknown')

        self._log_info('Auth {} - {}{} - {}'.format(source_type, amount,
                                                    currency, reference if reference else '<no reference>'))

        Validator.validate_dynamic_attribute(attribute=source, clazz=PaymentSource,
                                             type_err_msg='Invalid payment source.',
                                             missing_value_err_msg='Payment source missing.')
        Validator.validate_transaction(
            amount=amount, currency=currency, payment_type=payment_type, reference=reference)
        Validator.validate_dynamic_attribute(attribute=customer, clazz=Customer,
                                             type_err_msg='Invalid customer.')

        threeds = Validator.validate_and_set_boolean_shortcut(
            threeds, ThreeDS, 'Invalid 3DS.')

        request = {
            'source': source.get_dict() if isinstance(source, RequestDTO) else source,
            'amount': amount,
            'currency': currency if not isinstance(currency, sdk.Currency) else currency.value,
            'payment_type': payment_type if not isinstance(payment_type, sdk.PaymentType) else payment_type.value,
            'reference': reference,
            'customer': customer.get_dict() if isinstance(customer, RequestDTO) else customer,
            'capture': capture,
            'capture_on': capture_on,
            '3ds': threeds.get_dict() if isinstance(threeds, RequestDTO) else threeds
        }

        # add remaining properties
        request.update(kwargs)

        http_response = self._send_http_request(
            'payments', HttpMethod.POST, request)

        if http_response.status == HTTPStatus.ACCEPTED:
            return PaymentPending(http_response)
        else:
            return PaymentProcessed(http_response)

    def capture(self, id, value=None, track_id=None, **kwargs):
        return Capture(self._getPaymentActionResponse(id, 'capture', value, track_id, **kwargs))

    def void(self, id, track_id=None, **kwargs):
        return Void(self._getPaymentActionResponse(id, 'void', None, track_id, **kwargs))

    def refund(self, id, value=None, track_id=None, **kwargs):
        return Refund(self._getPaymentActionResponse(id, 'refund', value, track_id, **kwargs))

    def get(self, id):
        self._log_info('Get {}'.format(id))

        Validator.validate_id(id)

        return PaymentProcessed(self._send_http_request('charges/{}'.format(id), HttpMethod.GET))

    def _getPaymentActionResponse(self, id, action, value, track_id, **kwargs):
        self._log_info('{} - {} - {}'.format(action.capitalize(), id,
                                             track_id if track_id else '<no track id>'))

        Validator.validate_id(id)

        request = {
            'trackId': track_id
        }

        if value is not None:
            Validator.validate_transaction(amount=value)
            request['value'] = value

        # add remaining properties
        request.update(kwargs)

        return self._send_http_request(
            'charges/{}/{}'.format(id, action), HttpMethod.POST, request)
