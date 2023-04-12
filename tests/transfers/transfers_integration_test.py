from __future__ import absolute_import

from checkout_sdk.exception import CheckoutApiException
from checkout_sdk.transfers.transfers import CreateTransferRequest, TransferDestination, TransferSource, TransferType
from tests.checkout_test_utils import assert_response, new_idempotency_key


def test_should_initiate_transfer_of_funds_idempotently(oauth_api):
    transfer_source = TransferSource()
    transfer_source.id = 'ent_kidtcgc3ge5unf4a5i6enhnr5m'
    transfer_source.amount = 100

    transfer_destination = TransferDestination()
    transfer_destination.id = 'ent_w4jelhppmfiufdnatam37wrfc4'

    transfer_request = CreateTransferRequest()
    transfer_request.transfer_type = TransferType.COMMISSION
    transfer_request.source = transfer_source
    transfer_request.destination = transfer_destination

    idempotency_key = new_idempotency_key()

    response = oauth_api.transfers.initiate_transfer_of_funds(transfer_request, idempotency_key)
    assert_response(response, 'id', 'status')

    try:
        oauth_api.transfers.initiate_transfer_of_funds(transfer_request, idempotency_key)
    except CheckoutApiException as err:
        assert err.args[0] == 'The API response status code (409) does not indicate success.'
