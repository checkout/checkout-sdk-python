from checkout_sdk.checkout_api import CheckoutApi as DefaultApi
from checkout_sdk.four.checkout_api import CheckoutApi as FourApi


def test_should_instantiate_and_retrieve_clients_default(mock_api_client, mock_sdk_configuration):
    api = DefaultApi(mock_api_client, mock_sdk_configuration)

    assert api.tokens is not None
    assert api.sources is not None
    assert api.customers is not None
    assert api.instruments is not None
    assert api.payments is not None
    assert api.disputes is not None
    # APMs
    assert api.ideal is not None
    assert api.klarna is not None
    assert api.sepa is not None


def test_should_instantiate_and_retrieve_clients_four(mock_sdk_configuration):
    api = FourApi(mock_sdk_configuration)

    assert api.tokens is not None
    assert api.customers is not None
    assert api.instruments is not None
    assert api.payments is not None
    assert api.sessions is not None
    assert api.disputes is not None
    assert api.forex is not None
    assert api.accounts is not None
    # APMs
    assert api.ideal is not None
