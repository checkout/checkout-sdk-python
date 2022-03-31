from checkout_sdk.common.enums import Country, Currency, ChallengeIndicator
from checkout_sdk.sessions.sessions import BrowserSession, ThreeDsMethodCompletion, SessionAddress, \
    SessionMarketplaceData, \
    SessionsBillingDescriptor, NonHostedCompletionInfo, SessionRequest, ChannelData, \
    TransactionType, AppSession, SdkEphemeralPublicKey, SdkInterfaceType, UIElements, HostedCompletionInfo, \
    AuthenticationType, Category, SessionCardSource
from tests.checkout_test_utils import VisaCard, random_email, phone


def get_browser_session():
    browser_session = BrowserSession()
    browser_session.accept_header = 'Accept:  *.*, q=0.1'
    browser_session.java_enabled = True
    browser_session.language = 'FR-fr'
    browser_session.color_depth = '16'
    browser_session.screen_width = '1920'
    browser_session.screen_height = '1080'
    browser_session.timezone = '60'
    browser_session.user_agent = 'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                 'Chrome/69.0.3497.100 Safari/537.36 '
    browser_session.three_ds_method_completion = ThreeDsMethodCompletion.Y
    browser_session.ip_address = '1.12.123.255'

    return browser_session


def get_app_session():
    sdk_ephemeral_public_key = SdkEphemeralPublicKey()
    sdk_ephemeral_public_key.kty = 'EC'
    sdk_ephemeral_public_key.crv = 'P-256'
    sdk_ephemeral_public_key.x = 'f83OJ3D2xF1Bg8vub9tLe1gHMzV76e8Tus9uPHvRVEU'
    sdk_ephemeral_public_key.y = 'x_FEzRu9m36HLN_tue659LNpXW6pCyStikYjKIWI5a0'

    app_session = AppSession()
    app_session.sdk_app_id = 'dbd64fcb-c19a-4728-8849-e3d50bfdde39'
    app_session.sdk_max_timeout = 5
    app_session.sdk_encrypted_data = '{}'
    app_session.sdk_ephem_pub_key = sdk_ephemeral_public_key
    app_session.sdk_reference_number = '3DS_LOA_SDK_PPFU_020100_00007'
    app_session.sdk_transaction_id = 'b2385523-a66c-4907-ac3c-91848e8c0067'
    app_session.sdk_interface_type = SdkInterfaceType.BOTH
    app_session.sdk_ui_elements = [UIElements.SINGLE_SELECT, UIElements.HTML_OTHER]

    return app_session


def get_non_hosted_session(channel_data: ChannelData,
                           authentication_category: Category,
                           challenge_indicator_type: ChallengeIndicator,
                           transaction_type: TransactionType):
    billing_address = SessionAddress()
    billing_address.address_line1 = 'CheckoutSdk.com'
    billing_address.address_line2 = '90 Tottenham Court Road'
    billing_address.city = 'London'
    billing_address.state = 'ENG'
    billing_address.country = Country.GB

    session_card_source = SessionCardSource()
    session_card_source.billing_address = billing_address
    session_card_source.number = VisaCard.number
    session_card_source.expiry_month = VisaCard.expiry_month
    session_card_source.expiry_year = VisaCard.expiry_year
    session_card_source.name = 'John Doe'
    session_card_source.email = random_email()
    session_card_source.home_phone = phone()
    session_card_source.work_phone = phone()
    session_card_source.mobile_phone = phone()

    shipping_address = SessionAddress()
    shipping_address.address_line1 = 'CheckoutSdk.com'
    shipping_address.address_line2 = 'ABC building'
    shipping_address.address_line3 = '14 Wells Mews'
    shipping_address.city = 'London'
    shipping_address.state = 'ENG'
    shipping_address.zip = 'W1T 4TJ'
    shipping_address.country = Country.GB

    marketplace_data = SessionMarketplaceData()
    marketplace_data.sub_entity_id = 'ent_ocw5i74vowfg2edpy66izhts2u'

    billing_descriptor = SessionsBillingDescriptor()
    billing_descriptor.name = 'SUPERHEROES.COM'

    non_hosted_completion_info = NonHostedCompletionInfo()
    non_hosted_completion_info.callback_url = 'https://merchant.com/callback'

    session_request = SessionRequest()
    session_request.source = session_card_source
    session_request.amount = 6540
    session_request.currency = Currency.USD
    session_request.processing_channel_id = 'pc_5jp2az55l3cuths25t5p3xhwru'
    session_request.marketplace = marketplace_data
    session_request.authentication_category = authentication_category
    session_request.challenge_indicator = challenge_indicator_type
    session_request.billing_descriptor = billing_descriptor
    session_request.reference = 'ORD-5023-4E89'
    session_request.transaction_type = transaction_type
    session_request.shipping_address = shipping_address
    session_request.completion = non_hosted_completion_info
    session_request.channel_data = channel_data

    return session_request


def get_hosted_session():
    shipping_address = SessionAddress()
    shipping_address.address_line1 = 'CheckoutSdk.com'
    shipping_address.address_line2 = '90 Tottenham Court Road'
    shipping_address.city = 'London'
    shipping_address.state = 'ENG'
    shipping_address.zip = 'W1T 4TJ'
    shipping_address.country = Country.GB

    session_card_source = SessionCardSource()
    session_card_source.number = '4485040371536584'
    session_card_source.expiry_month = 1
    session_card_source.expiry_year = 2030

    hosted_completion_info = HostedCompletionInfo()
    hosted_completion_info.failure_url = 'https://example.com/sessions/fail'
    hosted_completion_info.success_url = 'https://example.com/sessions/success'

    session_request = SessionRequest()
    session_request.source = session_card_source
    session_request.amount = 100
    session_request.currency = Currency.USD
    session_request.processing_channel_id = 'pc_5jp2az55l3cuths25t5p3xhwru'
    session_request.authentication_type = AuthenticationType.REGULAR
    session_request.authentication_category = Category.PAYMENT
    session_request.challenge_indicator = ChallengeIndicator.NO_PREFERENCE
    session_request.reference = 'ORD-5023-4E89'
    session_request.transaction_type = TransactionType.GOODS_SERVICE
    session_request.shipping_address = shipping_address
    session_request.completion = hosted_completion_info

    return session_request
