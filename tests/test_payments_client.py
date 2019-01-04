import checkout_sdk as sdk
from checkout_sdk import HTTPClient, Config
from checkout_sdk.payments import PaymentsClient
from checkout_sdk.payments.responses import (
    Payment,
    PaymentPending,
    PaymentProcessed
)

from tests.base import CheckoutSdkTestCase


class PaymentsClientTests(CheckoutSdkTestCase):
    REFERENCE = 'REF_01'
    SUB_REFERENCE = 'SUB_REF'
    AMOUNT = 1000
    CURRENCY = sdk.Currency.EUR
    CUSTOMER_EMAIL = 'test@user.com'
    CUSTOMER_NAME = 'Test User'
    CARD_NUMBER = '4242424242424242'
    CARD_EXPIRY_MONTH = 9
    CARD_EXPIRY_YEAR = 2025
    CARD_CVV = '100'
    BILLING_LINE_1 = '1 New Street'
    BILLING_CITY = 'London'
    BILLING_ZIP = 'W1'
    BILLING_COUNTRY = 'GB'
    PHONE_COUNTRY_CODE = '+44'
    PHONE_NUMBER = '02999999999'

    def setUp(self):
        super().setUp()
        self.http_client = HTTPClient(Config())
        self.client = PaymentsClient(self.http_client)

    def tearDown(self):
        super().tearDown()
        self.http_client.close_session()

    def test_bad_payment_response_init(self):
        with self.assertRaises(TypeError):
            Payment(None, None)

    def test_payments_client_full_card_non_3ds_auth_request_with_kwargs(self):
        payment = self._auth_card()
        self._assert_payment_response_is_valid(
            payment, PaymentProcessed, False)
        self.assertTrue(isinstance(payment.approved, bool))
        self._assert_customer_is_valid(payment.customer)
        self._assert_source_is_valid(payment.source)
        self.assertIsNotNone(payment.actions_link)
        self.assertTrue(payment.can_capture
                        == (payment.capture_link is not None))
        self.assertTrue(payment.can_refund
                        == (payment.refund_link is not None))
        self.assertTrue(payment.can_void == (payment.void_link is not None))

    def test_payments_client_full_card_3ds_auth_request_with_kwargs(self):
        self._assert_payment_pending_response_is_valid(
            self._auth_card(True, False))

    def test_payments_client_full_card_3ds_auth_request_with_dictionary(self):
        self._assert_payment_pending_response_is_valid(
            self._auth_card(True, True))

    def test_payments_client_void_request(self):
        payment = self._auth_card()
        # void the previous auth request
        void = self.client.void(payment.id, reference=self.SUB_REFERENCE)
        self.assertIsNotNone(void.action_id)
        self.assertEqual(void.reference, self.SUB_REFERENCE)

    def test_payments_client_capture_full_amount_request(self):
        payment = self._auth_card()
        # capture the previous auth request
        capture = self.client.capture(payment.id,
                                      reference=self.SUB_REFERENCE)
        self.assertIsNotNone(capture.action_id)
        self.assertEqual(capture.reference, self.SUB_REFERENCE)

    def test_payments_client_capture_partial_amount_request(self):
        partial_amount = int(self.AMOUNT / 2)
        payment = self._auth_card()
        # capture the previous auth request
        capture = self.client.capture(payment.id,
                                      reference=self.SUB_REFERENCE,
                                      amount=partial_amount)
        self.assertIsNotNone(capture.action_id)
        self.assertEqual(capture.reference, self.SUB_REFERENCE)

    def test_payments_client_refund_full_amount_request(self):
        payment = self._auth_card()
        # capture the previous auth request
        self.client.capture(payment.id)
        # refund the capture
        refund = self.client.refund(payment.id,
                                    reference=self.SUB_REFERENCE)
        self.assertIsNotNone(refund.action_id)
        self.assertEqual(refund.reference, self.SUB_REFERENCE)

    def test_payments_client_refund_partial_amount_request(self):
        partial_amount = int(self.AMOUNT / 2)
        payment = self._auth_card()
        # capture the previous auth request
        self.client.capture(payment.id)
        # refund the capture
        refund = self.client.refund(payment.id,
                                    reference=self.SUB_REFERENCE,
                                    amount=partial_amount)
        self.assertIsNotNone(refund.action_id)
        self.assertEqual(refund.reference, self.SUB_REFERENCE)

    def test_payments_client_non_3ds_auth_request_with_card_source_id(self):
        payment = self._auth_card()
        payment2 = self._auth_source({
            'id': payment.source.id,
            'cvv': self.CARD_CVV
        })

        self._assert_payment_response_is_valid(
            payment2, PaymentProcessed, False)
        self.assertEqual(payment.source.id, payment2.source.id)

    def test_payments_client_non_3ds_auth_request_with_customer_source_id(self):
        payment = self._auth_card()
        payment2 = self._auth_source({
            'id': payment.customer.id
        })

        self._assert_payment_response_is_valid(
            payment2, PaymentProcessed, False)
        self.assertEqual(payment.customer.id, payment2.customer.id)

    def test_payments_client_payment_actions_request(self):
        payment = self._auth_card()
        # capture the previous auth request
        self.client.capture(payment.id)
        # get all actions
        actions = self.client.get_actions(payment.id)
        self.assertTrue(len(actions) > 0)
        self.assertIsNotNone(actions[0].id)

    def test_payments_client_non_3ds_get_request(self):
        payment = self._auth_card()
        # capture the previous auth request
        self.client.capture(payment.id)
        # get payment
        payment2 = self.client.get(payment.id)
        self._assert_payment_response_is_valid(
            payment2, PaymentProcessed, False)

    def test_payments_client_3ds_get_request(self):
        payment = self._auth_card(threeds=True)
        # get payment
        payment2 = self.client.get(payment.id)
        self._assert_payment_pending_response_is_valid(payment2)

    def test_payments_client_apm_auth_request(self):
        payment = self._auth_source({
            'type': 'ideal',
            'issuer_id': 'INGBNL2A'
        })
        self._assert_payment_pending_response_is_valid(payment)

    def _auth_card(self, threeds=False, dict_format=False, amount=None):
        if amount is None:
            amount = self.AMOUNT

        if dict_format:
            return self.client.request({
                'source': self._get_card_source(),
                'amount': amount,
                'currency': self.CURRENCY,
                'reference': self.REFERENCE,
                'customer': {
                    'email': self.CUSTOMER_EMAIL,
                    'name': self.CUSTOMER_NAME
                },
                '3ds': {
                    'enabled': threeds
                },
                'capture': False
            })
        else:
            return self.client.request(
                source=self._get_card_source(),
                amount=amount,
                currency=self.CURRENCY,
                reference=self.REFERENCE,
                customer={
                    'email': self.CUSTOMER_EMAIL,
                    'name': self.CUSTOMER_NAME
                },
                threeds=threeds,
                capture=False
            )

    def _auth_source(self, source):
        return self.client.request({
            'source': source,
            'amount': self.AMOUNT,
            'currency': self.CURRENCY,
            'reference': self.REFERENCE,
            'customer': {
                'email': self.CUSTOMER_EMAIL,
                'name': self.CUSTOMER_NAME
            }
        })

    def _get_card_source(self):
        return {
            'number': self.CARD_NUMBER,
            'expiry_month': self.CARD_EXPIRY_MONTH,
            'expiry_year': self.CARD_EXPIRY_YEAR,
            'cvv': self.CARD_CVV,
            'billing_address': {
                'address_line1': self.BILLING_LINE_1,
                'city': self.BILLING_CITY,
                'zip': self.BILLING_ZIP,
                'country': self.BILLING_COUNTRY
            },
            'phone': {
                'country_code': self.PHONE_COUNTRY_CODE,
                'number': self.PHONE_NUMBER
            }
        }

    def _assert_payment_pending_response_is_valid(self, payment):
        self._assert_payment_response_is_valid(payment, PaymentPending, True)
        self._assert_customer_is_valid(payment.customer)
        # 3DS / APM
        self.assertTrue(payment.requires_redirect)
        self.assertTrue(payment.redirect_link is not None)

    def _assert_payment_response_is_valid(self, payment, clazz=Payment, is_pending=False):
        self.assertTrue(isinstance(payment, clazz))
        # Resource
        self.assertIsNotNone(payment.api_version)
        self.assertIsNotNone(payment.request_id)
        self.assertTrue(
            payment.links is not None and len(payment.links) > 0)
        # PaymentResponse
        self.assertIsNotNone(payment.id)
        self.assertIsNotNone(payment.status)
        self.assertEqual(payment.reference, self.REFERENCE)
        self.assertTrue(payment.is_pending == is_pending)

    def _assert_customer_is_valid(self, customer):
        self.assertIsNotNone(customer.id)
        self.assertTrue(self.CUSTOMER_NAME == self.CUSTOMER_NAME)
        self.assertTrue(self.CUSTOMER_EMAIL == self.CUSTOMER_EMAIL)

    def _assert_source_is_valid(self, source):
        self.assertIsNotNone(source.id)
        self.assertIsNotNone(source.type)
