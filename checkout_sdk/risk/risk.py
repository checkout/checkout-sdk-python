from datetime import datetime

from checkout_sdk.common.common import Address, Phone, CustomerRequest
from checkout_sdk.common.enums import PaymentSourceType, Currency


class RiskPayment:
    psp: str
    id: str


class RiskShippingDetails:
    address: Address


class Location:
    latitude: str
    longitude: str


class Device:
    ip: str
    location: Location
    os: str
    type: str
    model: str
    date: datetime
    user_agent: str
    fingerprint: str


class AuthenticationResult:
    attempted: bool
    challenged: bool
    succeeded: bool
    liability_shifted: bool
    method: str
    version: str


class AuthorizationResult:
    avs_code: str
    cvv_result: str


class RiskPaymentRequestSource:
    type: PaymentSourceType

    def __init__(self, type_p: PaymentSourceType):
        self.type = type_p


class RiskRequestTokenSource(RiskPaymentRequestSource):
    token: str
    billing_address: Address
    phone: Phone

    def __init__(self):
        super().__init__(PaymentSourceType.TOKEN)


class IdSourcePrism(RiskPaymentRequestSource):
    id: str
    cvv: str

    def __init__(self):
        super().__init__(PaymentSourceType.ID)


class CardSourcePrism(RiskPaymentRequestSource):
    number: str
    expiry_month: int
    expiry_year: int
    name: str
    billing_address: Address
    phone: Phone

    def __init__(self):
        super().__init__(PaymentSourceType.CARD)


class CustomerSourcePrism(RiskPaymentRequestSource):
    id: str

    def __init__(self):
        super().__init__(PaymentSourceType.CUSTOMER)


class PreAuthenticationAssessmentRequest:
    date: datetime
    source: RiskPaymentRequestSource
    customer: CustomerRequest
    payment: RiskPayment
    shipping: RiskShippingDetails
    reference: str
    description: str
    amount: int
    currency: Currency
    device: Device
    metadata: dict


class PreCaptureAssessmentRequest:
    assessment_id: str
    date: datetime
    source: RiskPaymentRequestSource
    customer: CustomerRequest
    amount: int
    currency: Currency
    payment: RiskPayment
    shipping: RiskShippingDetails
    device: Device
    metadata: dict
    authentication_result: AuthenticationResult
    authorization_result: AuthorizationResult
