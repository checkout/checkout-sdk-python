from checkout_sdk.common import ApiResponse, Card


class CardResponse(ApiResponse):
    def __init__(self, api_response):
        super().__init__(api_response)
        self._card = Card(api_response.body)

    @property
    def card(self):
        return self._card

    def customer_id(self):
        return self._response.body['customerId']


class CardListResponse(ApiResponse):
    def __init__(self, api_response):
        super().__init__(api_response)
        self._cards = []
        for card_data in api_response.body['data']:
            self._cards.append(Card(card_data))

    @property
    def cards(self):
        return self._cards
