from enum import Enum


class CardMetadataSourceType(str, Enum):
    BIN = 'bin'
    CARD = 'card'
    ID = 'id'
    TOKEN = 'token'


class CardMetadataFormatType(str, Enum):
    BASIC = 'basic'
    CARD_PAYOUTS = 'card_payouts'


class CardMetadataRequestSource:
    type: CardMetadataSourceType

    def __init__(self, type_p: CardMetadataSourceType):
        self.type = type_p


class CardMetadataBinSource(CardMetadataRequestSource):
    bin: str

    def __init__(self):
        super().__init__(CardMetadataSourceType.BIN)


class CardMetadataCardSource(CardMetadataRequestSource):
    number: str

    def __init__(self):
        super().__init__(CardMetadataSourceType.CARD)


class CardMetadataIdSource(CardMetadataRequestSource):
    id: str

    def __init__(self):
        super().__init__(CardMetadataSourceType.ID)


class CardMetadataTokenSource(CardMetadataRequestSource):
    token: str

    def __init__(self):
        super().__init__(CardMetadataSourceType.TOKEN)


class CardMetadataRequest:
    source: CardMetadataRequestSource
    format: CardMetadataFormatType
