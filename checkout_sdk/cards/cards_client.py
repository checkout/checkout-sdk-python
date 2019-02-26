import checkout_sdk as sdk

from checkout_sdk import ApiClient, HttpMethod
from checkout_sdk.cards import CardResponse, CardListResponse
from checkout_sdk.common import ApiResponse


class CardsClient(ApiClient):

    def get_cards(self, customer_id):
        self._log_info('Get cards for {}'.format(customer_id))
        http_response = self._send_http_request(
            f'customers/{customer_id}/cards/', sdk.HttpMethod.GET)
        return CardListResponse(http_response)

    def get_card(self, customer_id, card_id):
        self._log_info('Get card {}{}'.format(customer_id, card_id))
        http_response = self._send_http_request(
            f'customers/{customer_id}/cards/{card_id}', sdk.HttpMethod.GET)
        return CardResponse(http_response)

    def remove_card(self, customer_id, card_id):
        self._log_info('Remove card {}{}'.format(customer_id, card_id))
        http_response = self._send_http_request(
            f'customers/{customer_id}/cards/{card_id}',
            HttpMethod.DELETE
        )
        return ApiResponse(http_response)
