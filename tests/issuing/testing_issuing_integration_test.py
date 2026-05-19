import pytest

from checkout_sdk.common.enums import Currency
from checkout_sdk.issuing.testing import CardSimulation, TransactionSimulation, TransactionType, AuthorizationType, \
    CardAuthorizationRequest, Merchant, SimulationRequest, CardRefundAuthorizationRequest, \
    SimulateOobAuthenticationRequest, OobSimulateTransactionDetails
from tests.checkout_test_utils import assert_response


@pytest.mark.skip("Avoid creating cards all the time")
class TestTestingIssuing:
    # tests

    def test_should_simulate_authorization(self, issuing_checkout_api, active_card):
        card_simulation = CardSimulation()
        card_simulation.id = active_card.id
        card_simulation.expiry_month = active_card.expiry_month
        card_simulation.expiry_year = active_card.expiry_year

        merchant = Merchant()
        merchant.category_code = '7399'

        transaction_simulation = TransactionSimulation()
        transaction_simulation.type = TransactionType.PURCHASE
        transaction_simulation.amount = 10
        transaction_simulation.currency = Currency.GBP
        transaction_simulation.merchant = merchant
        transaction_simulation.authorization_type = AuthorizationType.AUTHORIZATION

        request = CardAuthorizationRequest()
        request.card = card_simulation
        request.transaction = transaction_simulation

        response = issuing_checkout_api.issuing.simulate_authorization(request)

        assert_response(response,
                        'id',
                        'status')

        assert response.status == 'Authorized'

    def test_should_simulate_increment(self, issuing_checkout_api, transaction):
        request = SimulationRequest()
        request.amount = 1000

        response = issuing_checkout_api.issuing.simulate_increment(transaction.id, request)

        assert_response(response,
                        'status')

        assert response.status == 'Authorized'

    def test_should_simulate_clearing(self, issuing_checkout_api, transaction):
        request = SimulationRequest()
        request.amount = 100

        response = issuing_checkout_api.issuing.simulate_clearing(transaction.id, request)

        assert_response(response)

    def test_should_simulate_reversal(self, issuing_checkout_api, transaction):
        request = SimulationRequest()
        request.amount = 100

        response = issuing_checkout_api.issuing.simulate_reversal(transaction.id, request)

        assert_response(response,
                        'status')

        assert response.status == 'Reversed'

    def test_should_simulate_refund(self, issuing_checkout_api, transaction):
        request = CardRefundAuthorizationRequest()
        request.amount = 100

        response = issuing_checkout_api.issuing.simulate_refund(transaction.id, request)

        assert_response(response)
        assert response.http_metadata.status_code == 200

    def test_should_simulate_oob_authentication(self, issuing_checkout_api, active_card):
        request = build_oob_authentication_request(active_card.id)

        response = issuing_checkout_api.issuing.simulate_oob_authentication(request)

        assert_response(response)
        assert response.http_metadata.status_code == 200


# common methods

def build_oob_authentication_request(card_id: str) -> SimulateOobAuthenticationRequest:
    details = OobSimulateTransactionDetails()
    details.merchant_name = 'Acme Ltd'
    details.purchase_amount = 100
    details.purchase_currency = Currency.GBP

    request = SimulateOobAuthenticationRequest()
    request.card_id = card_id
    request.transaction_details = details
    return request
