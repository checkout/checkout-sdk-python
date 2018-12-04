try:
    from http import HTTPStatus
except ImportError:
    # Python 3.4
    from checkout_sdk.enums import HTTPStatus

import checkout_sdk as sdk
from checkout_sdk import ApiClient, HTTPMethod, Validator
from checkout_sdk.common import RequestDTO
from checkout_sdk.payments import PaymentSource, Customer
from checkout_sdk.payments.responses import (
    Payment,
    PaymentProcessed,
    PaymentPending,
    Capture,
    Refund,
    Void
)


class PaymentsClient(ApiClient):
    def request(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            # dictionary approach - everything else is ignored
            request = args[0]
        else:
            # parameter approach
            request = kwargs

        # set defaults if attributes are missing
        self._set_payment_request_defaults(request)

        source = request.get('source')
        amount = request.get('amount')
        currency = request.get('currency')
        payment_type = request.get('payment_type')
        reference = request.get('reference')

        source_type = source.type if isinstance(source, PaymentSource) \
            else source.get('type', 'unknown') if source is not None else 'unknown'

        self._log_info('Auth {} - {}{} - {}'.format(source_type,
                                                    amount,
                                                    currency,
                                                    reference if reference is not None
                                                    else '<no reference>'))

        Validator.validate_transaction(
            amount=amount,
            currency=currency,
            payment_type=payment_type,
            reference=reference
        )

        # dynamic attributes
        self._set_payment_request_dynamic_attributes(request)

        http_response = self._send_http_request(
            'payments', HTTPMethod.POST, request)

        if http_response.status == HTTPStatus.ACCEPTED:
            return PaymentPending(http_response)
        else:
            return PaymentProcessed(http_response)

    def capture(self, id, amount=None, reference=None, **kwargs):
        return Capture(self._getPaymentActionResponse(id, 'capture', amount, reference, **kwargs))

    def refund(self, id, amount=None, reference=None, **kwargs):
        return Refund(self._getPaymentActionResponse(id, 'refund', amount, reference, **kwargs))

    def void(self, id, reference=None, **kwargs):
        return Void(self._getPaymentActionResponse(id, 'void', None, reference, **kwargs))

    """
    def get(self, id):
        self._log_info('Get {}'.format(id))

        Validator.validate_id(id)

        return PaymentProcessed(self._send_http_request('charges/{}'.format(id), HTTPMethod.GET))
    """

    def _getPaymentActionResponse(self, id, action, amount, reference, **kwargs):
        self._log_info('{} - {} - {}'.format(action.capitalize(), id,
                                             reference if reference is not None
                                             else '<no reference>'))

        Validator.validate_id(id)

        request = {
            'reference': reference
        }

        if amount is not None:
            Validator.validate_transaction(amount=amount)
            request['amount'] = amount

        # add remaining properties
        request.update(kwargs)

        return self._send_http_request(
            'payments/{}/{}s'.format(id, action), HTTPMethod.POST, request)

    def _set_payment_request_defaults(self, request):
        request['currency'] = request.get(
            'currency', sdk.default_currency)
        request['payment_type'] = request.get(
            'payment_type', sdk.default_payment_type)
        request['capture'] = request.get(
            'capture', sdk.default_capture)

    def _set_payment_request_dynamic_attributes(self, request):
        request['source'] = Validator.validate_and_set_dynamic_class_attribute(
            arg=request.get('source'), clazz=PaymentSource,
            type_err_msg='Invalid payment source.',
            missing_arg_err_msg='Payment source missing.'
        )
        request['customer'] = Validator.validate_and_set_dynamic_class_attribute(
            arg=request.get('customer'), clazz=Customer,
            type_err_msg='Invalid customer.')
        # for 3ds, due to Python name limitations, we try both '3ds' and 'threeds' attribute names
        request['3ds'] = Validator.validate_and_set_dynamic_boolean_attribute(
            arg=request.get('threeds', request.get('3ds')), type_err_msg='Invalid 3DS settings.')
        request['risk'] = Validator.validate_and_set_dynamic_boolean_attribute(
            arg=request.get('risk'), type_err_msg='Invalid risk settings.')
