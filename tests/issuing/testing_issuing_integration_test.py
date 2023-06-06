import pytest

from checkout_sdk.common.enums import Currency
from checkout_sdk.issuing.testing import CardSimulation, TransactionSimulation, TransactionType, AuthorizationType, \
    CardAuthorizationRequest, Merchant, SimulationRequest
from tests.checkout_test_utils import assert_response


@pytest.mark.skip("Avoid creating cards all the time")
class TestTestingIssuing:
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
