from __future__ import absolute_import

from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.payments import PayoutRequest, PaymentRequestCardDestination
from tests.checkout_test_utils import VisaCard, phone, LAST_NAME, FIRST_NAME, new_uuid, assert_response, retriable


def test_should_request_payout(default_api):
    destination = PaymentRequestCardDestination()
    destination.name = VisaCard.name
    destination.number = VisaCard.number
    destination.first_name = FIRST_NAME
    destination.last_name = LAST_NAME
    destination.expiry_year = VisaCard.expiry_year
    destination.expiry_month = VisaCard.expiry_month
    destination.billing_address = phone()
    destination.phone = phone()

    payout_request = PayoutRequest()
    payout_request.destination = destination
    payout_request.capture = False
    payout_request.reference = new_uuid()
    payout_request.amount = 5
    payout_request.currency = Currency.GBP
    payout_request.reference = new_uuid()

    payout_response = default_api.payments.request_payout(payout_request)

    assert_response(payout_response,
                    'id',
                    'reference',
                    'status',
                    'customer',
                    'customer.id')

    payment = retriable(callback=default_api.payments.get_payment_details,
                        payment_id=payout_response.id)

    assert_response(payment,
                    'destination',
                    'destination.bin',
                    # 'destination.card_category',
                    # 'destination.card_type',
                    # 'destination.issuer',
                    # 'destination.issuer_country',
                    # 'destination.product_id',
                    # 'destination.product_type'
                    'destination.expiry_month',
                    'destination.expiry_year',
                    'destination.last4',
                    'destination.fingerprint',
                    'destination.name')
