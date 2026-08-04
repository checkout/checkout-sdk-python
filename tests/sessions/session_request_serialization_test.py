import json

from checkout_sdk.common.enums import Currency, Country
from checkout_sdk.json_serializer import JsonSerializer
from checkout_sdk.sessions.sessions import (
    AuthenticationType,
    BrowserSession,
    CardholderAccountInfo,
    Category,
    DeviceInformation,
    GoogleSpa,
    InitialTransaction,
    Installment,
    MerchantRiskInfo,
    NonHostedCompletionInfo,
    Optimization,
    Recurring,
    SessionAddress,
    SessionCardSource,
    SessionChallengeIndicator,
    SessionMarketplaceData,
    SessionRequest,
    SessionsBillingDescriptor,
    ThreeDsMethodCompletion,
    TransactionType,
)

# The 24 properties of the SessionRequest schema in the Checkout.com API Reference.
EXPECTED_ATTRIBUTES = [
    'source',
    'amount',
    'currency',
    'processing_channel_id',
    'marketplace',
    'authentication_type',
    'authentication_category',
    'account_info',
    'challenge_indicator',
    'billing_descriptor',
    'reference',
    'merchant_risk_info',
    'transaction_type',
    'shipping_address',
    'shipping_address_matches_billing',
    'completion',
    'channel_data',
    'recurring',
    'installment',
    'optimization',
    'initial_transaction',
    'device_information',
    'google_spa',
    'preferred_experiences',
]


def _serialize(obj):
    return json.loads(json.dumps(obj, cls=JsonSerializer))


def _fully_populated():
    source = SessionCardSource()
    source.number = '4485040371536584'
    source.expiry_month = 1
    source.expiry_year = 2030
    source.name = 'Bruce Wayne'

    billing_address = SessionAddress()
    billing_address.address_line1 = 'Checkout.com'
    billing_address.city = 'London'
    billing_address.zip = 'W1T 4TJ'
    billing_address.country = Country.GB
    source.billing_address = billing_address

    shipping_address = SessionAddress()
    shipping_address.address_line1 = 'Checkout.com'
    shipping_address.address_line2 = '90 Tottenham Court Road'
    shipping_address.city = 'London'
    shipping_address.state = 'ENG'
    shipping_address.zip = 'W1T 4TJ'
    shipping_address.country = Country.GB

    marketplace = SessionMarketplaceData()
    marketplace.sub_entity_id = 'ent_ocw5i74vowfg2edpy66izhts2u'

    account_info = CardholderAccountInfo()
    account_info.purchase_count = 10
    account_info.add_card_attempts = 5

    billing_descriptor = SessionsBillingDescriptor()
    billing_descriptor.name = 'SUPERHEROES.COM'

    merchant_risk_info = MerchantRiskInfo()
    merchant_risk_info.delivery_email = 'bruce@wayne-enterprises.com'
    merchant_risk_info.is_preorder = False
    merchant_risk_info.is_reorder = False

    completion = NonHostedCompletionInfo()
    completion.callback_url = 'https://merchant.com/callback'

    channel_data = BrowserSession()
    channel_data.accept_header = 'Accept:  *.*, q=0.1'
    channel_data.java_enabled = True
    channel_data.language = 'FR-fr'
    channel_data.three_ds_method_completion = ThreeDsMethodCompletion.Y
    channel_data.ip_address = '1.12.123.255'

    recurring = Recurring()
    recurring.days_between_payments = 30
    recurring.expiry = '99991231'

    installment = Installment()
    installment.number_of_payments = 3
    installment.days_between_payments = 30
    installment.expiry = '99991231'

    optimization = Optimization()
    optimization.optimized = True
    optimization.framework = 'acceptance_rates'

    initial_transaction = InitialTransaction()
    initial_transaction.acs_transaction_id = 'acs-txn-id'

    google_spa = GoogleSpa()
    google_spa.continue_url = 'https://merchant.com/continue'

    device_information = DeviceInformation()
    device_information.device_id = 'device-id'
    device_information.device_session_id = 'device-session'

    request = SessionRequest()
    request.source = source
    request.amount = 6540
    request.currency = Currency.USD
    request.processing_channel_id = 'pc_5jp2az55l3cuths25t5p3xhwru'
    request.marketplace = marketplace
    request.authentication_type = AuthenticationType.REGULAR
    request.authentication_category = Category.PAYMENT
    request.account_info = account_info
    request.challenge_indicator = SessionChallengeIndicator.TRUSTED_LISTING_PROMPT
    request.billing_descriptor = billing_descriptor
    request.reference = 'ORD-5023-4E89'
    request.merchant_risk_info = merchant_risk_info
    request.transaction_type = TransactionType.GOODS_SERVICE
    request.shipping_address = shipping_address
    request.shipping_address_matches_billing = True
    request.completion = completion
    request.channel_data = channel_data
    request.recurring = recurring
    request.installment = installment
    request.optimization = optimization
    request.initial_transaction = initial_transaction
    request.device_information = device_information
    request.google_spa = google_spa
    request.preferred_experiences = ['3ds', 'google_spa']

    return request


class TestSessionRequestSerialization:
    """Full-property serialization coverage for the POST /sessions request body.

    Every declared attribute is populated and asserted on the emitted payload, so adding an
    attribute without extending the fixture fails the test.
    """

    def test_declared_attributes_match_the_spec_property_set(self):
        """Guards both directions: a spec property missing from the SDK, and an attribute the SDK
        declares that the API Reference does not define.
        """
        declared = [
            name for name in SessionRequest.__annotations__
            if not name.startswith('_')
        ]

        assert sorted(declared) == sorted(EXPECTED_ATTRIBUTES)
        assert len(declared) == 24
        assert 'prior_transaction_reference' not in declared

    def test_serializes_every_declared_attribute(self):
        payload = _serialize(_fully_populated())

        for name in EXPECTED_ATTRIBUTES:
            assert name in payload, f'attribute {name} is missing from the serialized payload'

    def test_serializes_defaults_only(self):
        payload = _serialize(SessionRequest())

        assert payload['authentication_type'] == 'regular'
        assert payload['authentication_category'] == 'payment'
        assert payload['challenge_indicator'] == 'no_preference'
        assert payload['transaction_type'] == 'goods_service'

    def test_serializes_scalars_and_enums(self):
        payload = _serialize(_fully_populated())

        assert payload['amount'] == 6540
        assert payload['currency'] == 'USD'
        assert payload['processing_channel_id'] == 'pc_5jp2az55l3cuths25t5p3xhwru'
        assert payload['authentication_type'] == 'regular'
        assert payload['authentication_category'] == 'payment'
        assert payload['challenge_indicator'] == 'trusted_listing_prompt'
        assert payload['reference'] == 'ORD-5023-4E89'
        assert payload['transaction_type'] == 'goods_service'
        assert payload['shipping_address_matches_billing'] is True
        assert payload['preferred_experiences'] == ['3ds', 'google_spa']

    def test_serializes_nested_object_contents(self):
        payload = _serialize(_fully_populated())

        assert payload['source']['number'] == '4485040371536584'
        assert payload['source']['billing_address']['country'] == 'GB'
        assert payload['marketplace']['sub_entity_id'] == 'ent_ocw5i74vowfg2edpy66izhts2u'
        assert payload['account_info']['purchase_count'] == 10
        assert payload['billing_descriptor']['name'] == 'SUPERHEROES.COM'
        assert payload['merchant_risk_info']['delivery_email'] == 'bruce@wayne-enterprises.com'
        assert payload['shipping_address']['state'] == 'ENG'
        assert payload['completion']['callback_url'] == 'https://merchant.com/callback'
        assert payload['recurring']['days_between_payments'] == 30
        assert payload['installment']['number_of_payments'] == 3
        assert payload['optimization']['framework'] == 'acceptance_rates'
        assert payload['initial_transaction']['acs_transaction_id'] == 'acs-txn-id'
        assert payload['google_spa']['continue_url'] == 'https://merchant.com/continue'
        assert payload['device_information']['device_session_id'] == 'device-session'
