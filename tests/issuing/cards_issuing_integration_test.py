from datetime import datetime, timedelta

import pytest

from checkout_sdk.issuing.cards import PasswordEnrollmentRequest, SecurityPair, UpdateThreeDsEnrollmentRequest, \
    CardCredentialsQuery, RevokeRequest, RevokeReason, SuspendRequest, SuspendReason, UpdateCardRequest, CardMetadata, \
    VirtualCardRenewRequest, ScheduleCardRevocationRequest
from tests.checkout_test_utils import assert_response, phone


@pytest.mark.skip("Avoid creating cards all the time")
@pytest.mark.usefixtures("card")
class TestCardsIssuing:
    # tests

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

    def test_should_update_card(self, issuing_checkout_api, card):
        request = build_update_card_request()

        response = issuing_checkout_api.issuing.update_card(card.id, request)

        assert_response(response)
        assert response.http_metadata.status_code == 200

    def test_should_renew_card(self, issuing_checkout_api, card):
        request = VirtualCardRenewRequest()
        request.reference = 'RENEW-REF-123'

        response = issuing_checkout_api.issuing.renew_card(card.id, request)

        assert_response(response, 'id')
        assert response.http_metadata.status_code == 201

    def test_should_schedule_card_revocation(self, issuing_checkout_api, active_card):
        request = ScheduleCardRevocationRequest()
        request.revocation_date = (datetime.utcnow() + timedelta(days=7)).strftime('%Y-%m-%d')

        response = issuing_checkout_api.issuing.schedule_card_revocation(active_card.id, request)

        assert_response(response)
        assert response.http_metadata.status_code == 200

    def test_should_delete_card_revocation(self, issuing_checkout_api, active_card):
        request = ScheduleCardRevocationRequest()
        request.revocation_date = (datetime.utcnow() + timedelta(days=7)).strftime('%Y-%m-%d')
        issuing_checkout_api.issuing.schedule_card_revocation(active_card.id, request)

        response = issuing_checkout_api.issuing.delete_card_revocation(active_card.id)

        assert_response(response)
        assert response.http_metadata.status_code == 200

    def test_should_get_digital_card(self, issuing_checkout_api):
        digital_card_id = 'dcr_5ngxzsynm2me3oxf73esbhda6q'

        response = issuing_checkout_api.issuing.get_digital_card(digital_card_id)

        assert_response(response,
                        'id',
                        'card_id',
                        'last_four',
                        'status')
        assert response.id == digital_card_id

    def test_should_enroll_into_three_ds(self, issuing_checkout_api, card):
        request = PasswordEnrollmentRequest()
        request.password = self.__get_pass()
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
        request.password = self.__get_pass()
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

    def __get_pass(self):
        return 'Xtui43FvfiZ'


# common methods

def build_update_card_request() -> UpdateCardRequest:
    metadata = CardMetadata()
    metadata.udf1 = 'UDF1'
    metadata.udf2 = 'UDF2'
    metadata.udf3 = 'UDF3'
    metadata.udf4 = 'UDF4'
    metadata.udf5 = 'UDF5'

    request = UpdateCardRequest()
    request.reference = 'UPDATED-REF-123'
    request.metadata = metadata
    request.expiry_month = 12
    request.expiry_year = 2030
    return request
