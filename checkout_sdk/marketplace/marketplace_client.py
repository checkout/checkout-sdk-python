from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.common.enums import Currency
from checkout_sdk.files.files import FileRequest
from checkout_sdk.marketplace.marketplace import OnboardEntityRequest, MarketplacePaymentInstrument, \
    CreateTransferRequest, BalancesQuery, UpdateScheduleRequest


class MarketplaceClient(Client):
    __MARKETPLACE_PATH = 'marketplace'
    __INSTRUMENTS_PATH = 'instruments'
    __ENTITIES_PATH = 'entities'
    __FILES_PATH = 'files'
    __TRANSFERS_PATH = 'transfers'
    __BALANCES_PATH = 'balances'
    __PAYOUT_SCHEDULES_PATH = 'payout-schedules'

    def __init__(self, api_client: ApiClient,
                 files_client: ApiClient,
                 transfers_client: ApiClient,
                 balances_client: ApiClient,
                 configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.OAUTH)
        self.__files_client = files_client
        self.__transfers_client = transfers_client
        self.__balances_client = balances_client

    def create_entity(self, onboard_entity_request: OnboardEntityRequest):
        return self._api_client.post(self.build_path(self.__MARKETPLACE_PATH, self.__ENTITIES_PATH),
                                     self._sdk_authorization(), onboard_entity_request)

    def get_entity(self, entity_id: str):
        return self._api_client.get(self.build_path(self.__MARKETPLACE_PATH, self.__ENTITIES_PATH, entity_id),
                                    self._sdk_authorization())

    def update_entity(self, entity_id: str, onboard_entity_request: OnboardEntityRequest):
        return self._api_client.put(self.build_path(self.__MARKETPLACE_PATH, self.__ENTITIES_PATH, entity_id),
                                    self._sdk_authorization(), onboard_entity_request)

    def create_payment_instrument(self, entity_id: str, marketplace_payment_instrument: MarketplacePaymentInstrument):
        return self._api_client.post(
            self.build_path(self.__MARKETPLACE_PATH, self.__ENTITIES_PATH, entity_id, self.__INSTRUMENTS_PATH),
            self._sdk_authorization(), marketplace_payment_instrument)

    def upload_file(self, file_request: FileRequest):
        return self.__files_client.submit_file(self.__FILES_PATH, self._sdk_authorization(), file_request,
                                               multipart_file='path')

    def initiate_transfer_of_funds(self, create_transfer_request: CreateTransferRequest, idempotency_key: str = None):
        return self.__transfers_client.post(self.__TRANSFERS_PATH, self._sdk_authorization(), create_transfer_request,
                                            idempotency_key)

    def retrieve_entity_balances(self, entity_id: str, balances_query: BalancesQuery):
        return self.__balances_client.get(self.build_path(self.__BALANCES_PATH, entity_id), self._sdk_authorization(),
                                          balances_query)

    def update_payout_schedule(self, entity_id: str, currency: Currency,
                               update_schedule_request: UpdateScheduleRequest):
        return self._api_client.put(
            self.build_path(self.__MARKETPLACE_PATH, self.__ENTITIES_PATH, entity_id, self.__PAYOUT_SCHEDULES_PATH),
            self._sdk_authorization(), {currency: update_schedule_request})

    def retrieve_payout_schedule(self, entity_id: str):
        return self._api_client.get(
            self.build_path(self.__MARKETPLACE_PATH, self.__ENTITIES_PATH, entity_id, self.__PAYOUT_SCHEDULES_PATH),
            self._sdk_authorization())
