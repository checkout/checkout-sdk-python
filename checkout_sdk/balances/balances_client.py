from __future__ import absolute_import

from checkout_sdk.api_client import ApiClient
from checkout_sdk.authorization_type import AuthorizationType
from checkout_sdk.balances.balances import BalancesQuery
from checkout_sdk.checkout_configuration import CheckoutConfiguration
from checkout_sdk.client import Client
from checkout_sdk.exception import CheckoutArgumentException


class BalancesClient(Client):
    __BALANCES_PATH = 'balances'
    __ENTITIES_PATH = 'entities'
    __CURRENCY_ACCOUNTS_PATH = 'currency-accounts'
    __TOP_UP_INSTRUCTIONS_PATH = 'top-up-instructions'

    def __init__(self, api_client: ApiClient,
                 configuration: CheckoutConfiguration):
        super().__init__(api_client=api_client,
                         configuration=configuration,
                         authorization_type=AuthorizationType.SECRET_KEY_OR_OAUTH)

    def retrieve_entity_balances(self, entity_id: str, balances_query: BalancesQuery):
        return self._api_client.get(self.build_path(self.__BALANCES_PATH, entity_id), self._sdk_authorization(),
                                    balances_query)

    def retrieve_top_up_instructions(self, entity_id: str, currency_account_id: str):
        """Retrieves the bank details required to top up a sub-account, along with the payment
        reference that attributes an incoming payment to that sub-account.

        Note: The sub-account is referred to as currency account in the API.

        Args:
            entity_id: The ID of the entity that owns the sub-account, or of an entity above it in
                your hierarchy. A platform can use its own entity ID to reach the sub-accounts of
                any entity beneath it.
            currency_account_id: The ID of the sub-account to retrieve top-up instructions for.

        Returns:
            The decoded JSON response. This SDK has no response classes for balances, so the keys
            below are the wire names:

            - currency_account_id  str   [Required] The unique identifier of the sub-account that
                                         the instructions apply to.
            - currency             str   [Required] The currency that funds must be sent in, as a
                                         three-letter ISO 4217 currency code. This is the
                                         sub-account's holding currency, returned as
                                         holding_currency by retrieve_entity_balances.
            - payment_reference    str   [Required] The reference that must be quoted on the
                                         payment. It is how an incoming payment is attributed to
                                         the sub-account. A payment sent without this reference
                                         may not be credited.
            - bank_details         dict  [Required] The bank details for each available funding
                                         rail:
              - domestic           dict  [Optional] Funding details for the domestic rail.
              - international      dict  [Optional] Funding details for the international rail.

            Both rails are optional and their availability depends on the sub-account's holding
            currency, jurisdiction, and banking partner. Do not assume that both rails are always
            available; bank_details may contain neither.

            Each rail, when present, has the following keys. Only beneficiary_account_name and
            bank_name are always returned; the rest vary by rail and the receiving bank's
            jurisdiction, and are omitted when they do not apply.

            - beneficiary_account_name  str  [Required] The name of the account that receives the
                                             funds.
            - beneficiary_address       str  [Optional] The address of the beneficiary, if the rail
                                             requires it.
            - bank_name                 str  [Required] The name of the bank that receives the
                                             funds.
            - bank_address              str  [Optional] The address of the receiving bank, if the
                                             rail requires it.
            - account_number            str  [Optional] The account number of the receiving
                                             account.
            - sort_code                 str  [Optional] The sort code of the receiving bank.
                                             Returned for United Kingdom domestic transfers.
            - routing_number            str  [Optional] The routing number of the receiving bank.
                                             Returned for United States domestic transfers.
            - iban                      str  [Optional] The International Bank Account Number of
                                             the receiving account.
            - swift_code                str  [Optional] The SWIFT or BIC code of the receiving
                                             bank. Returned for international transfers.

        Raises:
            CheckoutArgumentException: If either path parameter is None, empty or blank. Both
                segments are interpolated straight into the request path, so a blank value would
                build a malformed URL and be rejected by the API rather than by the SDK.
        """
        if not entity_id or not entity_id.strip():
            raise CheckoutArgumentException('entity_id cannot be blank')
        if not currency_account_id or not currency_account_id.strip():
            raise CheckoutArgumentException('currency_account_id cannot be blank')

        return self._api_client.get(
            self.build_path(self.__ENTITIES_PATH, entity_id, self.__CURRENCY_ACCOUNTS_PATH, currency_account_id,
                            self.__TOP_UP_INSTRUCTIONS_PATH),
            self._sdk_authorization())
