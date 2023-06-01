import pytest

from checkout_sdk.issuing.cards import PasswordEnrollmentRequest, SecurityPair, UpdateThreeDsEnrollmentRequest, \
    CardCredentialsQuery, RevokeRequest, RevokeReason, SuspendRequest, SuspendReason
from tests.checkout_test_utils import assert_response, phone


@pytest.mark.skip("Avoid creating cards all the time")
@pytest.mark.usefixtures("card")
class TestCardsIssuing:
    def test_should_create_card(self, card):
        assert_response(card,
                        'id',
                        'display_name',
                        'last_four',
                        'expiry_month',
                        'expiry_year',
                        'billing_currency',
                        'issuing_country',
                        'reference')

        assert card.display_name == 'JOHN KENNEDY'
        assert card.reference == 'X-123456-N11'

    def test_should_get_card_details(self, issuing_checkout_api, cardholder, card):
        response = issuing_checkout_api.issuing.get_card_details(card.id)

        assert_response(response,
                        'id',
                        'cardholder_id',
                        'card_product_id',
                        'display_name',
                        'last_four',
                        'expiry_month',
                        'expiry_year',
                        'billing_currency',
                        'issuing_country',
                        'reference',
                        'status',
                        'type')

        assert response.id == card.id
        assert response.cardholder_id == cardholder.id
        assert response.card_product_id == 'pro_3fn6pv2ikshurn36dbd3iysyha'
        assert response.reference == 'X-123456-N11'

    def test_should_enroll_into_three_ds(self, issuing_checkout_api, card):
        request = PasswordEnrollmentRequest()
        request.password = 'Xtui43FvfiZ'
        request.locale = 'en-US'
        request.phone_number = phone()

        response = issuing_checkout_api.issuing.enroll_three_ds(card.id, request)

        assert_response(response)

        assert response.http_metadata.status_code == 202

    def test_should_update_three_ds_enrollment(self, issuing_checkout_api, card):
        security_pair = SecurityPair()
        security_pair.question = 'Who are you?'
        security_pair.answer = 'Bond. James Bond.'

        request = UpdateThreeDsEnrollmentRequest()
        request.password = 'Xtui43FvfiZ'
        request.security_pair = security_pair
        request.locale = 'en-US'
        request.phone_number = phone()

        response = issuing_checkout_api.issuing.update_three_ds_enrollment(card.id, request)

        assert_response(response)

        assert response.http_metadata.status_code == 202

    def test_should_get_three_ds_details(self, issuing_checkout_api, card):
        response = issuing_checkout_api.issuing.get_three_ds_details(card.id)

        assert_response(response,
                        'locale',
                        'phone_number')

    def test_should_activate_card(self, issuing_checkout_api, card):
        response = issuing_checkout_api.issuing.activate_card(card.id)

        assert_response(response)
        assert response.http_metadata.status_code == 200

        card_response = issuing_checkout_api.issuing.get_card_details(card.id)

        assert_response(card_response,
                        'id',
                        'status')

        assert card_response.id == card.id
        assert card_response.status == 'active'

    def test_get_card_credentials(self, issuing_checkout_api, card):
        query = CardCredentialsQuery()
        query.credentials = 'number, cvc2'

        response = issuing_checkout_api.issuing.get_card_credentials(card.id, query)

        assert_response(response,
                        'number',
                        'cvc2')

    def test_should_revoke_card(self, issuing_checkout_api, active_card):
        request = RevokeRequest()
        request.reason = RevokeReason.REPORTED_STOLEN

        response = issuing_checkout_api.issuing.revoke_card(active_card.id, request)

        assert_response(response)
        assert response.http_metadata.status_code == 200

        card_response = issuing_checkout_api.issuing.get_card_details(active_card.id)

        assert_response(card_response,
                        'id',
                        'status')

        assert card_response.id == active_card.id
        assert card_response.status == 'revoked'

    def test_should_suspend_card(self, issuing_checkout_api, active_card):
        request = SuspendRequest()
        request.reason = SuspendReason.SUSPECTED_STOLEN

        response = issuing_checkout_api.issuing.suspend_card(active_card.id, request)

        assert_response(response)
        assert response.http_metadata.status_code == 200

        card_response = issuing_checkout_api.issuing.get_card_details(active_card.id)

        assert_response(card_response,
                        'id',
                        'status')

        assert card_response.id == active_card.id
        assert card_response.status == 'suspended'
