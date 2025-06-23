from enum import Enum


class SourceType(str, Enum):
    ID = 'id'
    TOKEN = 'token'


class AbstractSource():
    type: SourceType

    def __init__(self, type_p: SourceType):
        self.type = type_p


class IdSource(AbstractSource):
    id: str
    cvv_token: str

    def __init__(self):
        super().__init__(SourceType.ID)


class TokenSource(AbstractSource):
    token: str

    def __init__(self):
        super().__init__(SourceType.TOKEN)


class SignatureType(str, Enum):
    DLOCAL = 'dlocal'


class AbstractSignature():
    type: SignatureType

    def __init__(self, type_p: SignatureType):
        self.type = type_p


class DlocalParameters:
    secret_key: str


class DlocalSignature(AbstractSignature):
    dlocal_parameters: DlocalParameters

    def __init__(self):
        super().__init__(SignatureType.DLOCAL)


class MethodType(str, Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'
    TRACE = 'TRACE'


class Headers:
    raw: dict
    encrypted: str = None


class DestinationRequest:
    url: str
    method: MethodType
    headers: Headers
    body: str
    signature: DlocalSignature = None


class NetworkToken:
    enabled: bool = None
    request_cryptogram: bool = None


class ForwardRequest:
    source: AbstractSource
    destination_request: DestinationRequest
    reference: str = None
    processing_channel_id: str = None
    network_token: NetworkToken = None
