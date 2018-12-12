try:
    from http import HTTPStatus
except ImportError:
    # Python 3.4
    from checkout_sdk.enums import HTTPStatus

import checkout_sdk as sdk
from checkout_sdk import ApiClient, HTTPMethod, Validator, PaymentStatus
from checkout_sdk.common import ResponseDTO
from checkout_sdk.payments.responses import (
    PaymentProcessed,
    PaymentPending,
    PaymentAction
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

        source_type = source.get(
            'type', 'unknown') if source is not None else 'unknown'

        self._log_info('Auth {} - {}{} - {}'.format(
            source_type,
            amount,
            currency,
            reference if reference is not None else '<no reference>'))

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

    def capture(self, payment_id, amount=None, reference=None, **kwargs):
        return PaymentAction(
            self._get_payment_action_response(payment_id, 'capture',
                                              amount, reference, **kwargs))

    def refund(self, payment_id, amount=None, reference=None, **kwargs):
        return PaymentAction(
            self._get_payment_action_response(payment_id, 'refund',
                                              amount, reference, **kwargs))

    def void(self, payment_id, reference=None, **kwargs):
        return PaymentAction(
            self._get_payment_action_response(payment_id, 'void',
                                              None, reference, **kwargs))

    def get(self, payment_id):
        http_response = self._get_response(payment_id, 'get')

        if http_response.body['status'] == PaymentStatus.Pending:
            return PaymentPending(http_response)
        else:
            return PaymentProcessed(http_response)

    def get_actions(self, payment_id):
        http_response = self._get_response(
            payment_id, 'get actions', '/actions')

        return [ResponseDTO(item) for item in http_response.body]

    def _get_response(self, payment_id, log_title, path=''):
        self._log_info('{} - {}'.format(log_title.capitalize(), payment_id))

        Validator.validate_id(payment_id)

        return self._send_http_request(
            'payments/{}{}'.format(payment_id, path), HTTPMethod.GET)

    def _get_payment_action_response(self, payment_id, action,
                                     amount, reference, **kwargs):
        self._log_info('{} - {} - {}'.format(
            action.capitalize(), payment_id,
            reference if reference is not None else '<no reference>'))

        Validator.validate_id(payment_id)

        request = {
            'reference': reference
        }

        if amount is not None:
            Validator.validate_transaction(amount=amount)
            request['amount'] = amount

        # add remaining properties
        request.update(kwargs)

        return self._send_http_request(
            'payments/{}/{}s'.format(payment_id, action),
            HTTPMethod.POST, request)

    def _set_payment_request_defaults(self, request):
        request['currency'] = request.get(
            'currency', sdk.default_currency)
        request['payment_type'] = request.get(
            'payment_type', sdk.default_payment_type)
        request['capture'] = request.get(
            'capture', sdk.default_capture)

    def _set_payment_request_dynamic_attributes(self, request):
        Validator.validate_complex_attribute(
            arg=request.get('source'),
            type_err_msg='Invalid payment source.',
            missing_arg_err_msg='Payment source missing.'
        )
        request['source'] = Validator.validate_and_set_source_type(
            request.get('source'))
        Validator.validate_complex_attribute(
            arg=request.get('customer'),
            type_err_msg='Invalid customer.')
        # for 3ds, due to Python name limitations,
        # we try both '3ds' and 'threeds' attribute names
        request['3ds'] = Validator.validate_and_set_dynamic_attr(
            arg=request.get(
                'threeds',
                request.get('3ds')), type_err_msg='Invalid 3DS settings.')
        request['risk'] = Validator.validate_and_set_dynamic_attr(
            arg=request.get('risk'), type_err_msg='Invalid risk settings.')
