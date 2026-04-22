from __future__ import absolute_import


class CardDetailsRequest:
    number: str
    expiry_month: int
    expiry_year: int


class InstrumentReference:
    id: str


class SourceOptions:
    card: CardDetailsRequest
    instrument: InstrumentReference


class GetUpdatedCardCredentialsRequest:
    source_options: SourceOptions
