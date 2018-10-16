import checkout_sdk as sdk

from checkout_sdk import ApiClient, Utils, HttpMethod
from checkout_sdk.common import DTO
from checkout_sdk.payments import PaymentProcessed, PaymentPending, CaptureResponse, VoidResponse, RefundResponse, PaymentSource, Customer, ThreeDS


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

        Utils.validate_dynamic_attribute(attribute=source, clazz=PaymentSource,
                                         type_err_msg='Invalid payment source.',
                                         missing_value_err_msg='Payment source missing.')
        Utils.validate_transaction(
            amount=amount, currency=currency, payment_type=payment_type, reference=reference)
        Utils.validate_dynamic_attribute(attribute=customer, clazz=Customer,
                                         type_err_msg='Invalid customer.')
        """
        Todo: REINSTATE AFTER 3DS RELEASE
        Utils.validate_dynamic_attribute(
            threeds, clazz=ThreeDS, type_err_msg='Invalid 3DS.')
        """

        request = {
            'source': source.get_dict() if isinstance(source, DTO) else source,
            'amount': amount,
            'currency': currency if not isinstance(currency, sdk.Currency) else currency.value,
            'payment_type': payment_type if not isinstance(payment_type, sdk.PaymentType) else payment_type.value,
            'reference': reference,
            'customer': customer.get_dict() if isinstance(customer, DTO) else customer,
            'capture': capture,
            'capture_on': capture_on,
            '3ds': threeds.get_dict() if isinstance(threeds, DTO) else threeds
        }

        # add remaining properties
        request.update(kwargs)

        http_response = self._send_http_request(
            'payments', HttpMethod.POST, request)

        if Utils.is_pending_flow(http_response):
            return PaymentPending(http_response)
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
            Utils.validate_transaction(amount=value)
            request['value'] = value

        # add remaining properties
        request.update(kwargs)

        return self._send_http_request(
            'charges/{}/{}'.format(id, action), HttpMethod.POST, request)
