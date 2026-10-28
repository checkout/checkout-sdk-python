from datetime import datetime
from enum import Enum

from checkout_sdk.common.enums import AccountHolderIdentificationType, AccountHolderType, Country, AccountType


class Address:
    address_line1: str
    address_line2: str
    city: str
    state: str
    zip: str
    country: Country


class Phone:
    country_code: str
    number: str


class CustomerRequest:
    id: str
    email: str
    name: str
    phone: Phone
    default: str
    metadata: dict
    tax_number: str


class CustomerRetry:
    max_attempts: int


class ResidentialStatusType(str, Enum):
    RESIDENT = 'resident'
    NON_RESIDENT = 'non_resident'


class AccountHolderIdentification:
    """The account holder's or the sender's identification.

    Shared by several positions. In the card payout and unreferenced refund destinations, providing
    identification details for the recipient increases the likelihood of a successful payout. In the
    card payout sender, it is required if the card's issuer_country is one of AR, BR, CO or PE. In the
    bank payout destination it is the account holder's government document identification, for
    example the social security number (SSN). Other positions (payment sources, instruments, accounts)
    follow their own schemas.
    """
    # The type of identification.
    # [Required] for card payouts and unreferenced refunds, [Optional] for bank payouts and regular
    # payments
    # Enum: "passport" "driving_license" "national_id" "company_registration" "tax_id" for card payouts
    # and unreferenced refunds; "passport" "driving_licence" "national_id" for the bank payout and
    # regular payment sender; free text (for example SSN) for the bank payout destination
    type: AccountHolderIdentificationType
    # The identification number.
    # [Required] for card payouts and unreferenced refunds, [Optional] for bank payouts and regular
    # payments
    # max 25 characters for the card payout and unreferenced refund destinations
    number: str
    # If applicable, the country that issued the identification, as a two-letter ISO country code.
    # Providing it increases the likelihood of a successful identity verification.
    # [Optional]
    # min 2 characters for card payouts and unreferenced refunds
    # max 2 characters for card payouts and unreferenced refunds
    issuing_country: Country
    # If applicable, the expiration date of the identification, in the format YYYY-MM-DD. Card
    # payouts and unreferenced refunds only.
    # [Optional]
    # min 10 characters
    # max 10 characters
    date_of_expiry: str


class AccountHolder:
    """The account holder details.

    Shared by the card payout destinations (card, network_token, id, token), the unreferenced refund
    destinations (card, network_token, id, token), the bank payout bank_account destination, and by
    payment sources, instruments and payment contexts, whose own schemas decide which properties
    apply. The tags below describe the payout and unreferenced refund positions. The card payout id
    and token destinations accept only type and the name properties.
    """
    # The type of account holder.
    # [Required] for card payouts, bank payouts and the unreferenced refund card and network_token
    # destinations, [Optional] for the unreferenced refund id and token destinations
    # Enum: "individual" "corporate" "government"
    type: AccountHolderType
    # The account holder's full name.
    # [Optional]
    # Deprecated: not in the request schema of any account holder; the Klarna payment source
    # account_holder had it until the API removed it. Still returned in the PayPal payment details
    # source account_holder. Retained for backwards compatibility. Will be removed in the next major
    # version. There is no replacement.
    full_name: str
    # The account holder's first name (individual). For card payouts, the combination of
    # first_name, middle_name and last_name should exceed 3 letters in length. This must be a valid
    # legal name.
    # [Required] for individual account holders in card payouts, bank payouts and the unreferenced
    # refund card and network_token destinations, [Optional] for the unreferenced refund id and token
    # destinations
    # max 50 characters for card payouts and unreferenced refunds
    first_name: str
    # The account holder's middle name (individual). Card payouts and unreferenced refunds only.
    # [Optional]
    # max 50 characters
    middle_name: str
    # The account holder's last name (individual). For card payouts, the combination of first_name,
    # middle_name and last_name should exceed 3 letters in length. This must be a valid legal name.
    # [Required] for individual account holders in card payouts, bank payouts and the unreferenced
    # refund card and network_token destinations, [Optional] for the unreferenced refund id and token
    # destinations
    # max 50 characters for card payouts and unreferenced refunds
    last_name: str
    # The account holder's email address. Card payouts and unreferenced refunds only.
    # [Optional]
    # max 255 characters
    email: str
    # The account holder's gender.
    # [Optional]
    # Deprecated: not in the request schema of any account holder; the Klarna payment source
    # account_holder had it until the API removed it. Still returned in the Klarna payment details
    # source account_holder. Retained for backwards compatibility. Will be removed in the next major
    # version. There is no replacement.
    gender: str
    # The account holder's company name (corporate, government). This must be a valid legal name.
    # For bank payouts, the full legal name of a registered company that holds the account.
    # [Required] for corporate and government account holders
    # max 50 characters for card payouts and unreferenced refunds
    company_name: str
    # The legal account holder's tax number or reference. Bank payouts only.
    # [Optional]
    tax_id: str
    # The account holder's date of birth, in the format YYYY-MM-DD (individual). Strongly
    # recommended where available for bank payouts.
    # [Optional]
    # min 10 characters for card payouts and unreferenced refunds
    # max 10 characters for card payouts and unreferenced refunds
    date_of_birth: str
    # The account holder's country of birth, as a two-letter ISO country code (individual).
    # [Optional]
    # min 2 characters for card payouts and unreferenced refunds
    # max 2 characters for card payouts and unreferenced refunds
    country_of_birth: Country
    # The account holder's residential status (individual). Bank payouts only.
    # [Optional]
    # Enum: "resident" "non_resident"
    residential_status: ResidentialStatusType
    # The account holder's billing address. For card payouts and unreferenced refunds, required if
    # your company is incorporated in the United States. For bank payouts, the current billing
    # address associated with the destination account.
    # [Required] for individual account holders in bank payouts, [Optional] otherwise
    billing_address: Address
    # The account holder's phone number. When set, country_code (min 1, max 7 characters) and
    # number (min 6, max 25 characters) are required for card payouts and unreferenced refunds.
    # [Optional]
    phone: Phone
    # The account holder's identification.
    # [Optional]
    identification: AccountHolderIdentification
    # Whether the ANI (account name inquiry) check should be performed with the scheme (Visa or
    # Mastercard). Used by payment sources; not part of the payout or unreferenced refund positions.
    # [Optional]
    account_name_inquiry: bool


class BankDetails:
    name: str
    branch: str
    address: Address


class UpdateCustomerRequest:
    id: str
    default: bool


class MarketplaceCommission:
    amount: int
    percentage: float


class MarketplaceDataSubEntity:
    id: str
    amount: int
    reference: str
    commission: MarketplaceCommission


class MarketplaceData:
    sub_entity_id: str
    sub_entities: list  # MarketplaceDataSubEntity


class Product:
    name: str
    quantity: int
    price: int


class Commission:
    amount: int
    percentage: float


class AmountAllocations:
    id: str
    amount: int
    reference: str
    commission: Commission


class ShippingInfo:
    shipping_company: str
    shipping_method: str
    tracking_number: str
    tracking_uri: str
    return_shipping_company: str
    return_tracking_number: str
    return_tracking_uri: str


class QueryFilterDateRange:
    from_: datetime
    to: datetime


class Destination:
    account_type: AccountType
    account_number: str
    bank_code: str
    branch_code: str
    iban: str
    bban: str
    swift_bic: str
    country: Country
    account_holder: AccountHolder
    bank: BankDetails
