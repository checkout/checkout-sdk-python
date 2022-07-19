from __future__ import absolute_import

from checkout_sdk.accounts.accounts import OnboardEntityRequest, UpdateScheduleRequest, AccountsPaymentInstrument
from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.common.enums import Currency
from checkout_sdk.files.files import FileRequest


class AccountsClient(Client):
    __ACCOUNTS_PATH = 'accounts'
    __INSTRUMENTS_PATH = 'instruments'
    __ENTITIES_PATH = 'entities'
    __FILES_PATH = 'files'
    __PAYOUT_SCHEDULES_PATH = 'payout-schedules'

    def __init__(self, api_client: ApiClient,
                 files_client: ApiClient,
                 configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.OAUTH)
        self.__files_client = files_client

    def create_entity(self, onboard_entity_request: OnboardEntityRequest):
        return self._api_client.post(self.build_path(self.__ACCOUNTS_PATH, self.__ENTITIES_PATH),
                                     self._sdk_authorization(), onboard_entity_request)

    def get_entity(self, entity_id: str):
        return self._api_client.get(self.build_path(self.__ACCOUNTS_PATH, self.__ENTITIES_PATH, entity_id),
                                    self._sdk_authorization())

    def update_entity(self, entity_id: str, onboard_entity_request: OnboardEntityRequest):
        return self._api_client.put(self.build_path(self.__ACCOUNTS_PATH, self.__ENTITIES_PATH, entity_id),
                                    self._sdk_authorization(), onboard_entity_request)

    def create_payment_instrument(self, entity_id: str, accounts_payment_instrument: AccountsPaymentInstrument):
        return self._api_client.post(
            self.build_path(self.__ACCOUNTS_PATH, self.__ENTITIES_PATH, entity_id, self.__INSTRUMENTS_PATH),
            self._sdk_authorization(), accounts_payment_instrument)

    def upload_file(self, file_request: FileRequest):
        return self.__files_client.submit_file(self.__FILES_PATH, self._sdk_authorization(), file_request,
                                               multipart_file='path')

    def update_payout_schedule(self, entity_id: str, currency: Currency,
                               update_schedule_request: UpdateScheduleRequest):
        return self._api_client.put(
            self.build_path(self.__ACCOUNTS_PATH, self.__ENTITIES_PATH, entity_id, self.__PAYOUT_SCHEDULES_PATH),
            self._sdk_authorization(), {currency: update_schedule_request})

    def retrieve_payout_schedule(self, entity_id: str):
        return self._api_client.get(
            self.build_path(self.__ACCOUNTS_PATH, self.__ENTITIES_PATH, entity_id, self.__PAYOUT_SCHEDULES_PATH),
            self._sdk_authorization())
